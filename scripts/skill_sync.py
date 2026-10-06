#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""skill_sync.py —— skills 仓库同步引擎（仅依赖 Python 标准库）

用法：
  python3 scripts/skill_sync.py push [选项]    本机 skills → 仓库 → 远端
  python3 scripts/skill_sync.py pull [选项]    远端 → 仓库 → 本机
  python3 scripts/skill_sync.py status         只读诊断，不做任何修改

退出码：
  0  成功（或本来就没有变更）
  1  执行错误（git 失败、路径不存在、软链接创建失败等）
  2  需要用户决策，已停止（内容冲突 / 工作区脏 / 本机 skill 与仓库不一致）

设计约定（与 /push_skills、/pull_skills 两个 skill 的说明保持一致）：
  * 本机 skills 目录只取其一，优先级 dsh > claude > codex。
  * 本机有、仓库没有的 skill：pull 时一律不动；push 时默认作为“新增”同步进仓库，
    可用 --only-tracked 改为只更新仓库已有的 skill。
  * 仓库有、本机没有的 skill：push 时不动（绝不删除仓库内容）。
  * 同名且内容不同：默认停下提示（--on-conflict=ask），不静默覆盖。
  * 安装方式默认软链接（Windows 用 junction 回退），必须显式 --copy 才复制文件。
"""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_readme  # noqa: E402  —— 同目录的 README 生成模块

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_BLOCKED = 2

BRANCH_DEFAULT = "master"
REMOTE_DEFAULT = "origin"

IGNORE_NAMES = {".git", ".DS_Store", "Thumbs.db", "__pycache__", ".idea"}
IGNORE_SUFFIX = (".pyc", ".pyo")

HOME = Path.home()


# --------------------------------------------------------------------------- #
# 基础工具
# --------------------------------------------------------------------------- #
def _init_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except Exception:
            pass


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def git(repo: Path, *args: str):
    """执行 git 并返回 (returncode, stdout, stderr)。"""
    cmd = ["git", "-c", "core.quotepath=false", "-C", str(repo), *args]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return (
        proc.returncode,
        proc.stdout.decode("utf-8", "replace"),
        proc.stderr.decode("utf-8", "replace"),
    )


def git_ok(repo: Path, *args: str) -> str:
    code, out, err = git(repo, *args)
    if code != 0:
        raise RuntimeError("git %s 失败：%s" % (" ".join(args), (err or out).strip()))
    return out


def fetch_state(repo: Path, remote: str, branch: str):
    """返回 (fetch 是否成功, 远端领先的提交数或 None 表示未知)。"""
    code, out, err = git(repo, "fetch", remote)
    if code != 0:
        return False, None
    ref = "%s/%s" % (remote, branch)
    code, out, _ = git(repo, "rev-list", "--count", "HEAD..%s" % ref)
    if code != 0:
        return True, None
    try:
        return True, int(out.strip())
    except ValueError:
        return True, None


def is_link_like(path: Path) -> bool:
    """真实软链接，或 Windows 上的 junction。"""
    try:
        st = os.lstat(path)
    except OSError:
        return False
    if stat.S_ISLNK(st.st_mode):
        return True
    attrs = getattr(st, "st_file_attributes", 0)
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    if attrs & reparse and stat.S_ISDIR(st.st_mode):
        return True
    return False


def link_target(path: Path) -> Path:
    """解析链接（含 junction）指向的真实路径。"""
    try:
        return Path(os.path.realpath(str(path)))
    except OSError:
        return path


def remove_path(path: Path) -> None:
    """删除文件/目录/链接；删除链接时绝不触碰目标内容。"""
    if not path.exists() and not is_link_like(path):
        return
    if is_link_like(path):
        if os.path.isdir(path) and not os.path.islink(path):
            os.rmdir(path)  # junction
        else:
            os.unlink(path)
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def copy_tree(src: Path, dst: Path) -> None:
    """把 src 整树复制到 dst（dst 先清空），跳过 VCS/缓存垃圾。"""
    dst.mkdir(parents=True, exist_ok=True)
    for entry in sorted(src.iterdir(), key=lambda p: p.name):
        if entry.name in IGNORE_NAMES or entry.name.endswith(IGNORE_SUFFIX):
            continue
        target = dst / entry.name
        if entry.is_dir() and not is_link_like(entry):
            copy_tree(entry, target)
        else:
            if is_link_like(entry):
                # 链接本身复制过去没有意义，按内容复制
                if entry.is_dir():
                    copy_tree(entry, target)
                else:
                    shutil.copy2(entry, target)
            else:
                shutil.copy2(entry, target)


def replace_tree(src: Path, dst: Path) -> None:
    if dst.exists() or is_link_like(dst):
        remove_path(dst)
    copy_tree(src, dst)


def make_link(target: Path, link: Path) -> str:
    """优先软链接；Windows 上退化为 junction；返回实际使用的方式。"""
    link.parent.mkdir(parents=True, exist_ok=True)
    target = target.resolve()
    if os.name == "nt":
        try:
            os.symlink(str(target), str(link), target_is_directory=True)
            return "symlink"
        except OSError:
            proc = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(target)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if proc.returncode != 0:
                raise OSError(
                    "Windows 上创建软链接与 junction 都失败（可能需要开发者模式或管理员权限）：%s"
                    % proc.stderr.decode("utf-8", "replace").strip()
                )
            return "junction"
    os.symlink(str(target), str(link))
    return "symlink"


# --------------------------------------------------------------------------- #
# skill 发现与比较
# --------------------------------------------------------------------------- #
def has_skill_md(path: Path) -> bool:
    try:
        return any(e.lower() == "skill.md" for e in os.listdir(path))
    except OSError:
        return False


def scan_skills(root: Path) -> dict:
    """root 下所有“目录且含 SKILL.md”的条目 —— 即 skill。"""
    found = {}
    if not root.is_dir():
        return found
    for entry in sorted(root.iterdir(), key=lambda p: p.name):
        if entry.name.startswith(".") or entry.name in IGNORE_NAMES:
            continue
        try:
            if not entry.is_dir():
                continue
        except OSError:
            continue
        if has_skill_md(entry):
            found[entry.name] = entry
    return found


def tree_digest(root: Path):
    """目录内容指纹（相对路径 + 文件内容），返回 (sha256, 文件数)。"""
    digest = hashlib.sha256()
    count = 0
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORE_NAMES)
        for name in sorted(filenames):
            if name in IGNORE_NAMES or name.endswith(IGNORE_SUFFIX):
                continue
            path = Path(dirpath) / name
            rel = path.relative_to(root).as_posix()
            digest.update(rel.encode("utf-8", "replace"))
            try:
                with open(path, "rb") as fh:
                    while True:
                        chunk = fh.read(1 << 20)
                        if not chunk:
                            break
                        digest.update(chunk)
            except OSError:
                digest.update(b"<unreadable>")
            count += 1
    return digest.hexdigest(), count


def tree_diff(left: Path, right: Path):
    """返回 (added, removed, modified)，均为相对路径列表。"""

    def collect(root: Path) -> dict:
        files = {}
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            dirnames[:] = [d for d in dirnames if d not in IGNORE_NAMES]
            for name in filenames:
                if name in IGNORE_NAMES or name.endswith(IGNORE_SUFFIX):
                    continue
                path = Path(dirpath) / name
                files[path.relative_to(root).as_posix()] = path
        return files

    a, b = collect(left), collect(right)
    added = sorted(set(a) - set(b))
    removed = sorted(set(b) - set(a))
    modified = [
        rel
        for rel in sorted(set(a) & set(b))
        if not filecmp.cmp(a[rel], b[rel], shallow=False)
    ]
    return added, removed, modified


def human_diff(added, removed, modified, limit: int = 8) -> str:
    parts = []

    def fmt(label: str, items):
        if not items:
            return
        shown = "、".join(items[:limit])
        more = "" if len(items) <= limit else " 等 %d 项" % len(items)
        parts.append("%s %d 个：%s%s" % (label, len(items), shown, more))

    fmt("新增文件", added)
    fmt("删除文件", removed)
    fmt("修改文件", modified)
    return "；".join(parts) if parts else "内容一致"


# --------------------------------------------------------------------------- #
# 路径解析
# --------------------------------------------------------------------------- #
def default_repo() -> Path | None:
    """本脚本位于 <repo>/scripts/skill_sync.py，据此推断仓库根。"""
    here = Path(__file__).resolve()
    candidate = here.parent.parent
    if (candidate / ".git").exists():
        return candidate
    return None


def resolve_repo(args) -> Path:
    if args.repo:
        repo = Path(args.repo).expanduser().resolve()
        if not (repo / ".git").exists():
            raise RuntimeError("--repo 指向的不是 git 仓库：%s" % repo)
        return repo
    for env in ("SKILLS_REPO", "SKILL_SYNC_REPO"):
        value = os.environ.get(env)
        if value:
            repo = Path(value).expanduser().resolve()
            if (repo / ".git").exists():
                return repo
    repo = default_repo()
    if repo:
        return repo
    code, out, _ = git(Path.cwd(), "rev-parse", "--show-toplevel")
    if code == 0 and out.strip():
        return Path(out.strip()).resolve()
    raise RuntimeError("无法确定 skills 仓库位置，请用 --repo 指定，或设置 SKILLS_REPO")


def local_candidates() -> list:
    """(组名, 路径, 说明) —— 按 dsh > claude > codex 排列。"""
    dsh_home = Path(os.environ.get("DSH_HOME", str(HOME / ".dsh")))
    agents_home = Path(os.environ.get("AGENTS_HOME", str(HOME / ".agents")))
    claude_home = Path(os.environ.get("CLAUDE_HOME", str(HOME / ".claude")))
    codex_home = Path(os.environ.get("CODEX_HOME", str(HOME / ".codex")))
    return [
        ("dsh", dsh_home / "skills", "DSH 专属用户目录(rank 400)"),
        ("dsh", agents_home / "skills", "共享 agents 目录(DSH rank 500)"),
        ("claude", claude_home / "skills", "Claude Code 用户目录"),
        ("codex", codex_home / "skills", "Codex 用户目录"),
    ]


def resolve_local_dir(args):
    """返回 (path, 组名, 说明, 候选报告)。只取其一。"""
    if args.dir:
        path = Path(args.dir).expanduser().resolve()
        return path, "custom", "--dir 指定", []

    candidates = local_candidates()
    report = []
    for group, raw, note in candidates:
        path = raw.expanduser().resolve()
        count = len(scan_skills(path)) if path.is_dir() else 0
        report.append(
            {"group": group, "path": str(path), "exists": path.is_dir(), "skills": count, "note": note}
        )

    if args.agent:
        group_cands = [c for c in candidates if c[0] == args.agent]
        if not group_cands:
            raise RuntimeError("未知的 --agent：%s" % args.agent)
        for group, raw, note in group_cands:
            path = raw.expanduser().resolve()
            if path.is_dir():
                return path, group, note, report
        # 组内目录都不存在：用该组第一项，后续按需创建
        group, raw, note = group_cands[0]
        return raw.expanduser().resolve(), group, note + "（待创建）", report

    non_empty = [
        (g, p.expanduser().resolve(), n)
        for g, p, n in candidates
        if p.expanduser().resolve().is_dir() and scan_skills(p.expanduser().resolve())
    ]
    if non_empty:
        group, path, note = non_empty[0]
        return path, group, note, report

    existing = [(g, p.expanduser().resolve(), n) for g, p, n in candidates if p.expanduser().resolve().is_dir()]
    if existing:
        group, path, note = existing[0]
        return path, group, note + "（目录为空）", report

    # 全都没有：默认共享 agents 目录，由安装步骤创建
    group, raw, note = candidates[1]
    return raw.expanduser().resolve(), group, note + "（待创建）", report


# --------------------------------------------------------------------------- #
# 输出
# --------------------------------------------------------------------------- #
class Report:
    def __init__(self, command: str):
        self.data = {
            "command": command,
            "repo": None,
            "branch": None,
            "remote": None,
            "local_dir": None,
            "local_group": None,
            "local_candidates": [],
            "items": [],
            "actions": [],
            "attention": [],
            "blocked": False,
            "summary": "",
        }

    def say(self, text: str) -> None:
        if not self.data["_json"]:
            print(text)

    def section(self, title: str) -> None:
        self.say("")
        self.say("== %s ==" % title)

    def finish(self, code: int, summary: str) -> int:
        self.data["summary"] = summary
        self.data["exit_code"] = code
        self.data["blocked"] = code == EXIT_BLOCKED
        payload = dict(self.data)
        payload.pop("_json", None)
        if self.data["_json"]:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            self.section("结果")
            self.say(summary)
            if code == EXIT_BLOCKED:
                self.say("（已停止，未做任何覆盖性操作。按上面的提示处理后重新运行。）")
        return code


def new_report(args, command: str) -> Report:
    report = Report(command)
    report.data["_json"] = bool(getattr(args, "json", False))
    return report


def table(rows, headers) -> str:
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    lines = ["  " + "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))]
    for row in rows:
        lines.append("  " + "  ".join(str(c).ljust(widths[i]) for i, c in enumerate(row)))
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# push：本机 → 仓库 → 远端
# --------------------------------------------------------------------------- #
def cmd_push(args) -> int:
    report = new_report(args, "push")
    repo = resolve_repo(args)
    branch = args.branch
    remote = args.remote

    report.data["repo"] = str(repo)
    report.data["branch"] = branch
    report.data["remote"] = remote

    report.say("仓库：%s" % repo)
    cur = git_ok(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    report.say("当前分支：%s（目标分支：%s）" % (cur, branch))
    if cur != branch:
        report.data["attention"].append("当前分支 %s 与目标分支 %s 不一致" % (cur, branch))
        return report.finish(
            EXIT_BLOCKED,
            "已停止：当前分支是 %s，但要求推到 %s。请先切换到 %s，或用 --branch 指定正确分支。"
            % (cur, branch, branch),
        )

    code, out, _ = git(repo, "remote")
    if remote not in out.split():
        report.data["attention"].append("远端 %s 不存在" % remote)
        return report.finish(EXIT_BLOCKED, "已停止：仓库没有远端 %s，请先配置。" % remote)

    fetch_ok, behind = fetch_state(repo, remote, branch)
    report.data["fetch_ok"] = fetch_ok
    report.data["remote_ahead"] = behind
    if fetch_ok:
        if behind:
            report.say("远端 %s/%s 领先本地 %d 个提交。" % (remote, branch, behind))
        else:
            report.say("已 fetch：远端没有本地缺少的提交。")
    else:
        report.say("提示：git fetch %s 失败（可能离线），无法确认远端是否领先。" % remote)
    # 「远端不领先且 fetch 成功」才算已验证；--allow-behind 表示用户显式承担风险
    verified = bool(args.allow_behind or (fetch_ok and not behind))

    dirty = [line for line in git_ok(repo, "status", "--porcelain").splitlines() if line.strip()]
    if dirty:
        report.say("")
        report.say("提示：仓库工作区当前已有 %d 项未提交改动，本次只会提交被同步的 skill 路径，"
                   "不会把它们一起提交。" % len(dirty))
        for line in dirty[:10]:
            report.say("  %s" % line)
        if len(dirty) > 10:
            report.say("  ... 其余 %d 项省略" % (len(dirty) - 10))

    local_dir, group, note, candidates = resolve_local_dir(args)
    report.data["local_dir"] = str(local_dir)
    report.data["local_group"] = group
    report.data["local_candidates"] = candidates

    report.say("")
    report.say("本机 skills 目录：%s（%s：%s）" % (local_dir, group, note))
    if candidates:
        rows = [
            (c["group"], "存在" if c["exists"] else "-", c["skills"], c["path"])
            for c in candidates
        ]
        report.say(table(rows, ["组", "状态", "skill 数", "路径"]))
        report.say("（同名目录同时存在时只取其一，优先级 dsh > claude > codex）")

    if not local_dir.is_dir():
        return report.finish(EXIT_ERROR, "错误：本机 skills 目录不存在：%s" % local_dir)

    local_skills = scan_skills(local_dir)
    repo_skills = scan_skills(repo)
    if not local_skills:
        return report.finish(EXIT_OK, "本机 skills 目录里没有找到任何 skill（含 SKILL.md 的目录），无事可做。")

    new_items, changed_items, same_items, ignored_items = [], [], [], []

    for name in sorted(local_skills):
        local_path = local_skills[name]
        repo_path = repo / name

        if name not in repo_skills:
            if args.only_tracked:
                ignored_items.append((name, "本机独有（--only-tracked 已跳过）"))
            else:
                new_items.append(name)
            continue

        local_real = link_target(local_path)
        repo_real = link_target(repo_path)
        if local_real == repo_real:
            same_items.append((name, "已链接到仓库，内容天然一致"))
            continue

        l_digest, l_count = tree_digest(local_path)
        r_digest, r_count = tree_digest(repo_path)
        if l_digest == r_digest:
            same_items.append((name, "内容一致（%d 个文件）" % l_count))
            continue

        changed_items.append((name, local_path, repo_path, l_count, r_count))

    report.data["items"] = (
        [{"name": n, "state": "new"} for n in new_items]
        + [{"name": c[0], "state": "changed"} for c in changed_items]
        + [{"name": n, "state": "same", "note": m} for n, m in same_items]
        + [{"name": n, "state": "ignored", "note": m} for n, m in ignored_items]
    )

    report.section("比对结果")
    if new_items:
        report.say("新增（本机有、仓库没有）：%s" % "、".join(new_items))
    if changed_items:
        report.say("同名但内容不同：%s" % "、".join(c[0] for c in changed_items))
    if same_items:
        report.say("无需改动：%s" % "、".join(n for n, _ in same_items))
    if ignored_items:
        report.say("已跳过：%s" % "、".join("%s(%s)" % (n, m) for n, m in ignored_items))
    repo_only = sorted(set(repo_skills) - set(local_skills))
    if repo_only:
        report.say("仓库有、本机没有（不改动、不删除）：%s" % "、".join(repo_only))

    if changed_items:
        report.say("")
        for name, local_path, repo_path, l_count, r_count in changed_items:
            added, removed, modified = tree_diff(local_path, repo_path)
            report.say("  · %s：%s" % (name, human_diff(added, removed, modified)))
            for rel in added[:5]:
                report.say("      + %s" % rel)
            for rel in modified[:5]:
                report.say("      M %s" % rel)
            for rel in removed[:5]:
                report.say("      - %s" % rel)

        if args.on_conflict == "ask":
            report.data["attention"].append("存在 %d 个同名内容不同的 skill" % len(changed_items))
            return report.finish(
                EXIT_BLOCKED,
                "已停止：%d 个 skill 与本机内容不同（见上）。请向用户确认后用 "
                "--on-conflict=overwrite 用本机版本覆盖仓库，或用 --on-conflict=skip 只同步新增。"
                % len(changed_items),
            )
        if args.on_conflict == "skip":
            report.say("按 --on-conflict=skip：这些 skill 保持仓库版本，不覆盖。")
        if args.on_conflict == "auto" and not verified:
            reason = (
                "远端 %s/%s 领先本地 %d 个提交" % (remote, branch, behind)
                if behind
                else "git fetch %s 失败，无法确认远端状态" % remote
            )
            report.data["attention"].append("本机有更新，但%s" % reason)
            return report.finish(
                EXIT_BLOCKED,
                "已停止：本机有 %d 个 skill 内容更新，但%s。先执行 /pull_skills 拉平远端再 push，"
                "避免把别的设备的改动顶掉；确实要用本机版本覆盖仓库时改用 --on-conflict=overwrite。"
                % (len(changed_items), reason),
            )

    plan = list(new_items)
    if changed_items and (args.on_conflict == "overwrite" or (args.on_conflict == "auto" and verified)):
        plan += [c[0] for c in changed_items]
        report.say(
            "本机更新过的 skill 将覆盖仓库版本：%s" % "、".join(c[0] for c in changed_items)
        )

    readme_stale = (not args.no_readme) and skill_readme.is_stale(repo)

    if not plan and not readme_stale:
        return report.finish(EXIT_OK, "没有需要同步的变更（新增 0、更新 0、README 已最新）。")

    if args.dry_run:
        report.data["actions"] = [{"action": "copy", "name": n, "dry_run": True} for n in plan]
        if not args.no_readme:
            report.data["actions"].append({"action": "readme", "dry_run": True})
        return report.finish(
            EXIT_OK,
            "dry-run：将同步 %d 个 skill%s，并刷新 README.md；未做任何写入。"
            % (len(plan), ("（%s）" % "、".join(plan)) if plan else ""),
        )

    if behind and not args.allow_behind:
        report.data["attention"].append("远端领先本地 %d 个提交" % behind)
        return report.finish(
            EXIT_BLOCKED,
            "已停止：远端 %s/%s 领先本地 %d 个提交，此时提交会造成分叉或顶掉别的设备的改动。"
            "请先执行 /pull_skills 拉平远端，再重新 push。" % (remote, branch, behind),
        )

    report.section("同步到仓库")
    staged_paths = []
    for name in plan:
        src = local_skills[name]
        dst = repo / name
        replace_tree(src, dst)
        staged_paths.append(str(dst))
        state = "新增" if name in new_items else "覆盖"
        report.say("  %s %s" % (state, name))
        report.data["actions"].append({"action": "copy", "name": name, "state": state})

    readme_changed = False
    if not args.no_readme:
        readme_changed = skill_readme.write(repo)
        if readme_changed:
            report.say("  刷新 README.md 技能列表")
            staged_paths.append(str(repo / "README.md"))
            report.data["actions"].append({"action": "readme", "state": "updated"})
    report.data["readme_changed"] = readme_changed

    if args.no_commit:
        return report.finish(
            EXIT_OK,
            "已同步 %d 个 skill%s到仓库工作区，按 --no-commit 未提交。"
            % (len(plan), "与 README.md " if readme_changed else " "),
        )

    git_ok(repo, "add", "--", *staged_paths)
    staged = [ln for ln in git_ok(repo, "diff", "--cached", "--name-only").splitlines() if ln.strip()]
    if not staged:
        return report.finish(EXIT_OK, "同步后没有产生可提交的变更（内容本来就一致）。")

    added = [n for n in plan if n in new_items]
    updated = [n for n in plan if n not in new_items]
    if added:
        subject = "feat(skills): 同步本机 skills（新增 %s）" % "、".join(added)
        if len(subject) > 72:
            subject = "feat(skills): 同步本机 skills（新增 %d 个）" % len(added)
    elif updated:
        subject = "chore(skills): 同步本机 skills 更新（%s）" % "、".join(updated)
        if len(subject) > 72:
            subject = "chore(skills): 同步本机 skills 更新（%d 个）" % len(updated)
    else:
        subject = "docs(readme): 更新 skills 列表"
    body_lines = []
    if added:
        body_lines.append("新增：%s" % "、".join(added))
    if updated:
        body_lines.append("更新：%s" % "、".join(updated))
    if readme_changed:
        body_lines.append("文档：刷新 README.md 技能列表")
    message = subject + "\n\n" + "\n".join(body_lines) + "\n" if body_lines else subject + "\n"

    import tempfile

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as fh:
        fh.write(message)
        msg_file = fh.name
    try:
        git_ok(repo, "commit", "-F", msg_file)
    finally:
        try:
            os.unlink(msg_file)
        except OSError:
            pass

    commit = git_ok(repo, "rev-parse", "--short", "HEAD").strip()
    report.say("")
    report.say("已提交：%s（%s）" % (subject, commit))
    report.data["actions"].append({"action": "commit", "subject": subject, "commit": commit})

    if args.no_push:
        return report.finish(EXIT_OK, "已提交 %s；按 --no-push 未推送。" % commit)

    code, out, err = git(repo, "push", remote, branch)
    if code != 0:
        report.say("")
        report.say((err or out).strip())
        report.data["attention"].append("推送失败")
        return report.finish(
            EXIT_ERROR,
            "提交已在本地完成（%s），但推送到 %s/%s 失败。本地提交没有丢失；"
            "排查网络/凭据后可重新执行 git push %s %s。" % (commit, remote, branch, remote, branch),
        )

    report.data["actions"].append({"action": "push", "remote": remote, "branch": branch})
    return report.finish(
        EXIT_OK,
        "完成：同步 %d 个 skill（新增 %d、更新 %d）%s并已推送到 %s/%s，提交 %s。"
        % (
            len(plan),
            len(added),
            len(updated),
            "、刷新 README.md " if readme_changed else " ",
            remote,
            branch,
            commit,
        ),
    )


# --------------------------------------------------------------------------- #
# pull：远端 → 仓库 → 本机
# --------------------------------------------------------------------------- #
def cmd_pull(args) -> int:
    report = new_report(args, "pull")
    repo = resolve_repo(args)
    branch = args.branch
    remote = args.remote

    report.data["repo"] = str(repo)
    report.data["branch"] = branch
    report.data["remote"] = remote
    report.say("仓库：%s" % repo)

    cur = git_ok(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    report.say("当前分支：%s（目标分支：%s）" % (cur, branch))
    if cur != branch:
        report.data["attention"].append("当前分支 %s 与目标分支 %s 不一致" % (cur, branch))
        return report.finish(
            EXIT_BLOCKED,
            "已停止：当前分支是 %s，但要求拉取 %s。请先切回 %s 再重试，或用 --branch 指定正确分支。"
            % (cur, branch, branch),
        )

    dirty = [ln for ln in git_ok(repo, "status", "--porcelain").splitlines() if ln.strip()]
    if dirty and not args.allow_dirty:
        report.section("检测到未提交改动（uncommitted）")
        for line in dirty[:20]:
            report.say("  %s" % line)
        if len(dirty) > 20:
            report.say("  ... 其余 %d 项省略" % (len(dirty) - 20))
        report.data["attention"].append("仓库工作区有 %d 项未提交改动" % len(dirty))
        return report.finish(
            EXIT_BLOCKED,
            "已停止：仓库工作区有 %d 项未提交改动，未执行 pull，也未改动本机 skills。"
            "请先用 /push_skills 提交推送，或先 git stash / 手动处理，然后重试。" % len(dirty),
        )

    if args.no_pull or args.dry_run:
        if args.dry_run:
            report.say("dry-run：不访问远端、不执行 pull、不写入，仅按当前仓库内容给出安装计划。")
        else:
            report.say("按 --no-pull：跳过 fetch/pull，只用当前仓库内容同步本机。")
    else:
        code, out, err = git(repo, "fetch", remote)
        if code != 0:
            report.say((err or out).strip())
            report.data["attention"].append("fetch 失败")
            return report.finish(EXIT_ERROR, "错误：git fetch %s 失败，未改动本机 skills。" % remote)

        code, out, err = git(repo, "pull", "--ff-only", remote, branch)
        if code != 0:
            report.say((err or out).strip())
            report.data["attention"].append("pull 失败")
            return report.finish(
                EXIT_ERROR,
                "错误：git pull --ff-only %s %s 失败（可能是分叉或无凭据），未改动本机 skills。"
                "请先处理仓库分叉再重试。" % (remote, branch),
            )
        report.say("已更新仓库：%s" % (out.strip().splitlines()[-1] if out.strip() else "已是最新"))
        head = git_ok(repo, "log", "-1", "--pretty=%h %s").strip()
        report.say("当前 HEAD：%s" % head)
        report.data["actions"].append({"action": "pull", "head": head})

    repo_skills = scan_skills(repo)
    local_dir, group, note, candidates = resolve_local_dir(args)
    report.data["local_dir"] = str(local_dir)
    report.data["local_group"] = group
    report.data["local_candidates"] = candidates

    report.say("")
    report.say("本机 skills 目录：%s（%s：%s）" % (local_dir, group, note))
    if candidates:
        rows = [(c["group"], "存在" if c["exists"] else "-", c["skills"], c["path"]) for c in candidates]
        report.say(table(rows, ["组", "状态", "skill 数", "路径"]))
        report.say("（同名目录同时存在时只取其一，优先级 dsh > claude > codex）")

    if not repo_skills:
        return report.finish(EXIT_OK, "仓库里没有找到任何 skill，无事可做。")

    def classify(name: str):
        repo_path = repo / name
        local_path = local_dir / name
        if not local_path.exists() and not is_link_like(local_path):
            return "missing", local_path, repo_path, None
        real_local = link_target(local_path)
        real_repo = link_target(repo_path)
        linked = is_link_like(local_path)
        if real_local == real_repo:
            return ("linked" if linked else "same"), local_path, repo_path, None
        l_digest, _ = tree_digest(local_path)
        r_digest, _ = tree_digest(repo_path)
        if l_digest == r_digest:
            return "same", local_path, repo_path, None
        return "drift", local_path, repo_path, (linked, tree_diff(local_path, repo_path))

    states = {}
    for name in sorted(repo_skills):
        states[name] = classify(name)

    report.section("本机状态")
    rows = []
    for name, (state, _, _, _) in states.items():
        label = {
            "missing": "未安装",
            "linked": "已链接到仓库",
            "same": "内容一致（实体目录）",
            "drift": "与仓库不一致",
        }[state]
        rows.append((name, label))
    report.say(table(rows, ["skill", "状态"]))

    local_only = sorted(set(scan_skills(local_dir)) - set(repo_skills))
    if local_only:
        report.say("")
        report.say("本机有、仓库没有（一律不动）：%s" % "、".join(local_only))

    to_install = [n for n, s in states.items() if s[0] == "missing"]
    drifted = [n for n, s in states.items() if s[0] == "drift"]

    report.data["items"] = [
        {"name": n, "state": s[0], "local": str(s[1]), "repo": str(s[2])} for n, s in states.items()
    ]

    if drifted:
        report.say("")
        for name in drifted:
            linked, (added, removed, modified) = states[name][3]
            report.say("  · %s：%s" % (name, human_diff(added, removed, modified)))
        if not args.force:
            for name in drifted:
                report.data["attention"].append("本机 %s 与仓库不一致" % name)
        else:
            report.say("按 --force：将用仓库版本覆盖这些 skill。")

    if args.dry_run:
        planned = [
            {"action": ("copy" if args.copy else "link"), "name": n, "dry_run": True}
            for n in to_install
        ]
        if args.force:
            planned += [{"action": "overwrite", "name": n, "dry_run": True} for n in drifted]
        report.data["actions"] = planned
        return report.finish(
            EXIT_OK,
            "dry-run：将安装 %d 个 skill%s，未做任何写入。"
            % (len(to_install), ("，并覆盖 %d 个不一致的 skill" % len(drifted)) if args.force else ""),
        )

    mode = "复制" if args.copy else "软链接"
    if to_install or (drifted and args.force):
        local_dir.mkdir(parents=True, exist_ok=True)
        report.section("同步到本机（%s）" % mode)

    installed, overwritten, failed = [], [], []

    for name in to_install:
        repo_path = repo / name
        local_path = local_dir / name
        try:
            if args.copy:
                replace_tree(repo_path, local_path)
                how = "copy"
            else:
                remove_path(local_path)
                how = make_link(repo_path, local_path)
        except OSError as exc:
            failed.append((name, str(exc)))
            report.say("  失败 %s：%s" % (name, exc))
            continue
        installed.append(name)
        report.say("  安装 %s（%s）" % (name, "复制" if how == "copy" else how))
        report.data["actions"].append({"action": "install", "name": name, "how": how})

    if drifted and args.force:
        for name in drifted:
            repo_path = repo / name
            local_path = local_dir / name
            try:
                if args.copy:
                    replace_tree(repo_path, local_path)
                    how = "copy"
                else:
                    remove_path(local_path)
                    how = make_link(repo_path, local_path)
            except OSError as exc:
                failed.append((name, str(exc)))
                report.say("  失败 %s：%s" % (name, exc))
                continue
            overwritten.append(name)
            report.say("  覆盖 %s（%s）" % (name, "复制" if how == "copy" else how))
            report.data["actions"].append({"action": "overwrite", "name": name, "how": how})

    if failed:
        report.data["attention"].extend("%s 安装失败：%s" % (n, m) for n, m in failed)
        detail = "；".join("%s：%s" % (n, m) for n, m in failed[:3])
        hint = ""
        if not args.copy:
            hint = " 若本机文件系统不支持软链接（例如外接盘/exFAT、Windows 未开开发者模式），请显式用 --copy 复制安装。"
        return report.finish(
            EXIT_ERROR,
            "错误：%d 个 skill 安装失败（%s）。%s" % (len(failed), detail, hint),
        )

    if drifted and not args.force:
        report.data["attention"].extend("本机 %s 与仓库不一致，未覆盖" % n for n in drifted)
        return report.finish(
            EXIT_BLOCKED,
            "部分完成：已安装 %d 个 skill（%s）；但 %d 个已存在的 skill 与本机内容不同，未做覆盖：%s。"
            "请确认这些本地改动是否需要保留：需要保留就先 /push_skills，需要丢弃就用 --force 覆盖。"
            % (
                len(installed),
                "、".join(installed) if installed else "无",
                len(drifted),
                "、".join(drifted),
            ),
        )

    if not to_install and not overwritten:
        return report.finish(EXIT_OK, "本机已是最新：仓库 %d 个 skill 全部就位，无需安装。" % len(repo_skills))

    return report.finish(
        EXIT_OK,
        "完成：新安装 %d 个 skill（%s）%s。本机有、仓库没有的 skill 未做任何处理。"
        % (
            len(installed),
            "、".join(installed) if installed else "无",
            ("，覆盖 %d 个（%s）" % (len(overwritten), "、".join(overwritten))) if overwritten else "",
        ),
    )


# --------------------------------------------------------------------------- #
# delete：从仓库删除 skill 并推送
# --------------------------------------------------------------------------- #
def _commit(repo: Path, subject: str, body_lines) -> str:
    """按中文 Conventional Commits 提交，返回短 SHA。"""
    import tempfile

    message = subject + "\n"
    if body_lines:
        message += "\n" + "\n".join(body_lines) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as fh:
        fh.write(message)
        msg_file = fh.name
    try:
        git_ok(repo, "commit", "-F", msg_file)
    finally:
        try:
            os.unlink(msg_file)
        except OSError:
            pass
    return git_ok(repo, "rev-parse", "--short", "HEAD").strip()


def cmd_delete(args) -> int:
    report = new_report(args, "delete")
    repo = resolve_repo(args)
    branch = args.branch
    remote = args.remote

    report.data["repo"] = str(repo)
    report.data["branch"] = branch
    report.data["remote"] = remote
    report.say("仓库：%s" % repo)

    cur = git_ok(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    report.say("当前分支：%s（目标分支：%s）" % (cur, branch))
    if cur != branch:
        report.data["attention"].append("当前分支 %s 与目标分支 %s 不一致" % (cur, branch))
        return report.finish(
            EXIT_BLOCKED, "已停止：当前分支是 %s，但要求提交到 %s。" % (cur, branch)
        )

    code, out, _ = git(repo, "remote")
    if remote not in out.split():
        return report.finish(EXIT_BLOCKED, "已停止：仓库没有远端 %s。" % remote)

    fetch_ok, behind = fetch_state(repo, remote, branch)
    report.data["fetch_ok"] = fetch_ok
    report.data["remote_ahead"] = behind
    if fetch_ok:
        report.say("已 fetch：远端 %s/%s 领先本地 %d 个提交。" % (remote, branch, behind or 0))
    else:
        report.say("提示：git fetch %s 失败，无法确认远端是否领先。" % remote)
    if behind and not args.allow_behind:
        report.data["attention"].append("远端领先本地 %d 个提交" % behind)
        return report.finish(
            EXIT_BLOCKED,
            "已停止：远端 %s/%s 领先本地 %d 个提交。请先 /pull_skills 拉平远端再删除，避免造成分叉。"
            % (remote, branch, behind),
        )

    names, seen = [], set()
    for raw in args.names:
        name = raw.strip().strip("/\\")
        if name and name not in seen:
            seen.add(name)
            names.append(name)
    if not names:
        return report.finish(EXIT_ERROR, "错误：没有指定要删除的 skill。")

    invalid = [n for n in names if not skill_readme.is_skill_dir(repo / n)]
    if invalid:
        existing = "、".join(n for n, _, _ in skill_readme.collect(repo)) or "（仓库里没有 skill）"
        report.data["attention"].append("这些名字不是仓库里的 skill：%s" % "、".join(invalid))
        return report.finish(
            EXIT_ERROR,
            "错误：未删除任何东西——以下名字不是仓库里的 skill：%s。仓库现有 skill：%s"
            % ("、".join(invalid), existing),
        )

    local_dir, group, note, _ = resolve_local_dir(args)
    report.data["local_dir"] = str(local_dir)
    report.data["local_group"] = group
    report.say("")
    report.say("本机 skills 目录：%s（%s：%s）" % (local_dir, group, note))

    report.section("将删除")
    report.say(table([(n,) for n in names], ["skill"]))
    report.data["items"] = [{"name": n, "state": "delete"} for n in names]

    if args.dry_run:
        return report.finish(
            EXIT_OK,
            "dry-run：将从仓库删除 %d 个 skill（%s）并%s，未做任何写入。"
            % (
                len(names),
                "、".join(names),
                "刷新 README.md" if not args.no_readme else "不刷新 README",
            ),
        )

    for name in names:
        remove_path(repo / name)
        report.say("  已从仓库删除 %s" % name)
        report.data["actions"].append({"action": "delete-repo", "name": name})

    kept_local, cleaned_links, removed_local = [], [], []
    for name in names:
        local_path = local_dir / name
        if is_link_like(local_path):
            remove_path(local_path)
            cleaned_links.append(name)
            report.say("  已清理本机链接 %s" % name)
        elif local_path.exists():
            if args.also_local:
                remove_path(local_path)
                removed_local.append(name)
                report.say("  已删除本机目录 %s" % name)
            else:
                kept_local.append(name)

    if kept_local:
        report.say("")
        report.say("注意：本机实体目录仍保留：%s" % "、".join(kept_local))
        report.say("      它们仍会出现在本机 skill 列表里，且下次 /push_skills 会把它们重新带回仓库；")
        report.say("      要一起删干净，请加 --also-local 重跑，或手动删除本机目录。")
    report.data["actions"].extend({"action": "unlink-local", "name": n} for n in cleaned_links)
    report.data["actions"].extend({"action": "delete-local", "name": n} for n in removed_local)
    report.data["kept_local"] = kept_local

    readme_changed = False
    if not args.no_readme:
        readme_changed = skill_readme.write(repo)
        if readme_changed:
            report.say("  刷新 README.md 技能列表")

    staged_paths = [str(repo / n) for n in names]
    if readme_changed:
        staged_paths.append(str(repo / "README.md"))
    git_ok(repo, "add", "-A", "--", *staged_paths)
    staged = [ln for ln in git_ok(repo, "diff", "--cached", "--name-only").splitlines() if ln.strip()]
    if not staged:
        return report.finish(EXIT_OK, "仓库里没有产生可提交的变更。")
    if args.no_commit:
        return report.finish(
            EXIT_OK, "已在仓库工作区删除 %d 个 skill，按 --no-commit 未提交。" % len(names)
        )

    subject = "chore(skills): 删除 skills（%s）" % "、".join(names)
    if len(subject) > 72:
        subject = "chore(skills): 删除 %d 个 skills" % len(names)
    body_lines = ["删除：%s" % "、".join(names)]
    if readme_changed:
        body_lines.append("文档：刷新 README.md 技能列表")
    commit = _commit(repo, subject, body_lines)
    report.say("")
    report.say("已提交：%s（%s）" % (subject, commit))
    report.data["actions"].append({"action": "commit", "subject": subject, "commit": commit})

    if args.no_push:
        return report.finish(EXIT_OK, "已提交 %s；按 --no-push 未推送。" % commit)

    code, out, err = git(repo, "push", remote, branch)
    if code != 0:
        report.say("")
        report.say((err or out).strip())
        report.data["attention"].append("推送失败")
        return report.finish(
            EXIT_ERROR,
            "删除已在本地提交（%s），但推送到 %s/%s 失败。可排除故障后重新执行 git push %s %s。"
            % (commit, remote, branch, remote, branch),
        )

    report.data["actions"].append({"action": "push", "remote": remote, "branch": branch})
    extra = ""
    if kept_local:
        extra = "（本机实体目录 %s 未删除，下次 push 会重新带回仓库）" % "、".join(kept_local)
    return report.finish(
        EXIT_OK,
        "完成：仓库删除 %d 个 skill（%s）%s并已推送到 %s/%s，提交 %s。%s"
        % (
            len(names),
            "、".join(names),
            "、刷新 README.md " if readme_changed else " ",
            remote,
            branch,
            commit,
            extra,
        ),
    )


# --------------------------------------------------------------------------- #
# readme：生成 / 校验 README.md 技能列表
# --------------------------------------------------------------------------- #
def cmd_readme(args) -> int:
    report = new_report(args, "readme")
    repo = resolve_repo(args)
    report.data["repo"] = str(repo)

    skills = skill_readme.collect(repo)
    changed, text = skill_readme.compose(repo)
    report.data["items"] = [
        {"name": n, "description": skill_readme.shorten(d)} for n, d, _ in skills
    ]
    report.say("仓库：%s" % repo)
    report.say("技能数：%d" % len(skills))

    if args.check:
        if changed:
            report.data["attention"].append("README.md 与仓库内容不一致")
            return report.finish(
                EXIT_BLOCKED,
                "README.md 需要更新（或尚未生成）。运行 `skill_sync.py readme` 即可刷新。",
            )
        return report.finish(EXIT_OK, "README.md 已是最新。")

    if args.dry_run:
        report.say("")
        report.say(text)
        return report.finish(
            EXIT_OK, "dry-run：README.md %s，未做任何写入。" % ("需要更新" if changed else "已是最新")
        )

    if not changed:
        return report.finish(EXIT_OK, "README.md 已是最新，无需改动。")
    (repo / "README.md").write_text(text, encoding="utf-8", newline="\n")
    report.data["actions"].append({"action": "readme", "state": "updated"})
    return report.finish(EXIT_OK, "已刷新 README.md（收录 %d 个 skill）。" % len(skills))


# --------------------------------------------------------------------------- #
# status：只读诊断
# --------------------------------------------------------------------------- #
def cmd_status(args) -> int:
    report = new_report(args, "status")
    repo = resolve_repo(args)
    branch = args.branch
    local_dir, group, note, candidates = resolve_local_dir(args)

    report.data["repo"] = str(repo)
    report.data["branch"] = branch
    report.data["local_dir"] = str(local_dir)
    report.data["local_group"] = group
    report.data["local_candidates"] = candidates

    report.say("仓库：%s" % repo)
    cur = git_ok(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    report.say("当前分支：%s（目标：%s / %s）" % (cur, args.remote, branch))
    report.say("HEAD：%s" % git_ok(repo, "log", "-1", "--pretty=%h %s").strip())
    dirty = [ln for ln in git_ok(repo, "status", "--porcelain").splitlines() if ln.strip()]
    report.say("未提交改动：%d 项" % len(dirty))
    for line in dirty[:10]:
        report.say("  %s" % line)

    report.say("")
    report.say("本机 skills 目录：%s（%s：%s）" % (local_dir, group, note))
    rows = [(c["group"], "存在" if c["exists"] else "-", c["skills"], c["path"]) for c in candidates]
    report.say(table(rows, ["组", "状态", "skill 数", "路径"]))

    repo_skills = scan_skills(repo)
    local_skills = scan_skills(local_dir)
    report.say("")
    report.say("仓库 skill：%d 个" % len(repo_skills))
    report.say("本机 skill：%d 个" % len(local_skills))

    missing, same, drift, linked = [], [], [], []
    for name in sorted(repo_skills):
        local_path = local_dir / name
        if not local_path.exists() and not is_link_like(local_path):
            missing.append(name)
            continue
        if link_target(local_path) == link_target(repo / name):
            linked.append(name)
            continue
        if tree_digest(local_path)[0] == tree_digest(repo / name)[0]:
            same.append(name)
        else:
            drift.append(name)

    local_only = sorted(set(local_skills) - set(repo_skills))
    report.say("已有链接：%s" % ("、".join(linked) if linked else "无"))
    report.say("实体目录但一致：%s" % ("、".join(same) if same else "无"))
    report.say("未安装：%s" % ("、".join(missing) if missing else "无"))
    report.say("与仓库不一致：%s" % ("、".join(drift) if drift else "无"))
    report.say("本机独有（不处理）：%s" % ("、".join(local_only) if local_only else "无"))

    report.data["items"] = (
        [{"name": n, "state": "linked"} for n in linked]
        + [{"name": n, "state": "same"} for n in same]
        + [{"name": n, "state": "missing"} for n in missing]
        + [{"name": n, "state": "drift"} for n in drift]
        + [{"name": n, "state": "local-only"} for n in local_only]
    )
    return report.finish(EXIT_OK, "只读诊断完成，未做任何修改。")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skill_sync.py",
        description="skills 仓库同步引擎：push（本机→仓库→远端）/ pull（远端→仓库→本机）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subs = parser.add_subparsers(dest="command", required=True)

    def common(p):
        p.add_argument("--repo", help="skills 仓库路径（默认自动从脚本位置或 SKILLS_REPO 推断）")
        p.add_argument("--dir", help="本机 skills 目录（覆盖自动探测）")
        p.add_argument("--agent", choices=["dsh", "claude", "codex"], help="只在这组目录里选一个")
        p.add_argument("--remote", default=REMOTE_DEFAULT, help="远端名，默认 origin")
        p.add_argument("--branch", default=BRANCH_DEFAULT, help="分支，默认 master")
        p.add_argument("--json", action="store_true", help="以 JSON 输出结果")
        p.add_argument("--dry-run", action="store_true", help="只展示将要做什么，不写入")

    p_push = subs.add_parser("push", help="本机 skills → 仓库 → 远端")
    common(p_push)
    p_push.add_argument(
        "--on-conflict",
        choices=["auto", "ask", "skip", "overwrite"],
        default="auto",
        help="同名内容不同时：auto=先 fetch 确认远端没领先就自动用本机更新覆盖仓库（默认），"
        "ask=停下提示，skip=保留仓库版本，overwrite=无条件用本机覆盖仓库",
    )
    p_push.add_argument("--only-tracked", action="store_true", help="只更新仓库已有的 skill，忽略本机独有")
    p_push.add_argument("--no-readme", action="store_true", help="不刷新 README.md")
    p_push.add_argument("--allow-behind", action="store_true", help="远端领先时也继续提交（危险）")
    p_push.add_argument("--no-commit", action="store_true", help="只同步到仓库工作区，不提交")
    p_push.add_argument("--no-push", action="store_true", help="提交但不推送")
    p_push.set_defaults(func=cmd_push)

    p_pull = subs.add_parser("pull", help="远端 → 仓库 → 本机")
    common(p_pull)
    p_pull.add_argument("--copy", action="store_true", help="用复制安装，而不是软链接")
    p_pull.add_argument("--force", action="store_true", help="用仓库版本覆盖本机不一致的 skill")
    p_pull.add_argument("--no-pull", action="store_true", help="不访问远端，只用当前仓库内容同步本机")
    p_pull.add_argument("--allow-dirty", action="store_true", help="允许在仓库有未提交改动时继续（危险）")
    p_pull.set_defaults(func=cmd_pull)

    p_status = subs.add_parser("status", help="只读诊断")
    common(p_status)
    p_status.set_defaults(func=cmd_status)

    p_delete = subs.add_parser("delete", help="按名称从仓库删除 skill，刷新 README 并推送")
    common(p_delete)
    p_delete.add_argument("names", nargs="+", help="要删除的 skill 目录名（可多个）")
    p_delete.add_argument(
        "--also-local", action="store_true", help="同时删除本机 skills 目录里的对应内容（危险）"
    )
    p_delete.add_argument("--no-readme", action="store_true", help="不刷新 README.md")
    p_delete.add_argument("--allow-behind", action="store_true", help="远端领先时也继续（危险）")
    p_delete.add_argument("--no-commit", action="store_true", help="只从工作区删除，不提交")
    p_delete.add_argument("--no-push", action="store_true", help="提交但不推送")
    p_delete.set_defaults(func=cmd_delete)

    p_readme = subs.add_parser("readme", help="按仓库当前内容生成或校验 README.md 技能列表")
    common(p_readme)
    p_readme.add_argument("--check", action="store_true", help="只检查是否需要更新（需更新时退出码 2）")
    p_readme.set_defaults(func=cmd_readme)

    return parser


def main(argv=None) -> int:
    _init_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except RuntimeError as exc:
        eprint("错误：%s" % exc)
        return EXIT_ERROR
    except KeyboardInterrupt:
        eprint("已中断。")
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
