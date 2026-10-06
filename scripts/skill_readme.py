#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""skill_readme.py —— 由仓库里的 skill 生成 / 刷新 README.md 的技能列表。

规则：
  * 技能表放在 `<!-- SKILLS:START -->` 与 `<!-- SKILLS:END -->` 之间，标记之外的手写内容永远保留。
  * 简介取自每个 `<skill>/SKILL.md` frontmatter 的 `description`，**完整展示、不做截断**。
  * 输出按 skill 名称排序，保证幂等（内容没变就不算变更）。
  * `non_chinese()` 列出简介不含中文的 skill，便于保持全中文简介。
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

START_MARK = "<!-- SKILLS:START -->"
END_MARK = "<!-- SKILLS:END -->"
DEFAULT_URL = "https://github.com/BUGLAN/skills.git"
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

SKIP_DIRS = {".git", ".github", "scripts", "node_modules", "__pycache__", ".idea", ".vscode"}

INTRO = """# Skills

我的跨设备 agent skills 中央仓库：本机 skills 由 `/push_skills` 汇入并推送到 GitHub，
新设备用 `/pull_skills` 拉取安装（优先软链接），`/delete_skills` 按自然语言从仓库移除 skill。

## 用法

| 命令 | 作用 |
| --- | --- |
| `/push_skills` | 本机 skills → 仓库 → `origin master`；新增与更新自动纳入，README 自动刷新 |
| `/pull_skills` | 远端 → 仓库 → 本机；工作区有未提交改动时立即停止并告知，优先软链接安装（Windows 回落 junction） |
| `/delete_skills` | 用自然语言指定一个或多个 skill，从仓库删除并推送，README 同步刷新 |

引擎是 [`scripts/skill_sync.py`](scripts/skill_sync.py)，只依赖 Python 3 标准库。

```bash
git clone {url}
python3 scripts/skill_sync.py pull      # 新设备：装好本机缺失的 skill
python3 scripts/skill_sync.py push      # 本机有新增/更新：同步回仓库并推送
python3 scripts/skill_sync.py status    # 只读诊断
python3 scripts/skill_sync.py readme    # 按仓库当前内容重新生成技能列表
```

## 技能列表

"""


# --------------------------------------------------------------------------- #
# frontmatter / 简介
# --------------------------------------------------------------------------- #
def _frontmatter(text: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            return "\n".join(lines[1:i])
    return ""


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def read_description(skill_dir: Path) -> str:
    """取 SKILL.md frontmatter 里的 description（支持单行、引号、块标量）。"""
    skill_md = None
    try:
        for entry in sorted(skill_dir.iterdir(), key=lambda p: p.name):
            if entry.name.lower() == "skill.md" and entry.is_file():
                skill_md = entry
                break
    except OSError:
        return ""
    if skill_md is None:
        return ""
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""

    lines = _frontmatter(text).splitlines()
    for i, line in enumerate(lines):
        match = re.match(r"^description:\s*(.*)$", line)
        if not match:
            continue
        value = match.group(1).strip()
        if value in ("|", ">", "|-", ">-", "|+", ">+"):
            block = []
            for nxt in lines[i + 1:]:
                if not nxt.strip():
                    block.append("")
                    continue
                if not nxt.startswith((" ", "\t")):
                    break
                block.append(nxt.strip())
            return " ".join(part for part in block if part).strip()
        return _unquote(value).strip()
    return ""


def flatten(text: str) -> str:
    """把 description 压成单行（保留全部内容，不截断）。"""
    return " ".join(text.split())


def has_chinese(text: str) -> bool:
    return bool(CJK_RE.search(text))


def non_chinese(repo: Path):
    """返回简介不含中文的 skill 名列表（用于提醒补中文简介）。"""
    return [name for name, desc, _ in collect(repo) if not has_chinese(desc)]


def _escape_cell(text: str) -> str:
    return text.replace("\\", "\\\\").replace("|", "\\|")


# --------------------------------------------------------------------------- #
# 收集与渲染
# --------------------------------------------------------------------------- #
def is_skill_dir(path: Path) -> bool:
    if not path.is_dir():
        return False
    try:
        return any(e.lower() == "skill.md" for e in (entry.name for entry in path.iterdir()))
    except OSError:
        return False


def collect(repo: Path):
    """返回按名称排序的 [(name, description, skill_dir)]。"""
    found = []
    try:
        entries = sorted(repo.iterdir(), key=lambda p: p.name.lower())
    except OSError:
        return found
    for entry in entries:
        if entry.name.startswith(".") or entry.name in SKIP_DIRS:
            continue
        if is_skill_dir(entry):
            found.append((entry.name, read_description(entry), entry))
    return found


def render_section(repo: Path) -> str:
    skills = collect(repo)
    lines = [START_MARK, ""]
    if not skills:
        lines.append("（仓库里还没有 skill）")
    else:
        lines.append("共 %d 个 skill，按名称排序。" % len(skills))
        lines.append("")
        lines.append("| skill | 简介 |")
        lines.append("| --- | --- |")
        for name, desc, _ in skills:
            cell = _escape_cell(flatten(desc)) if desc else "（SKILL.md 未写 description）"
            lines.append("| [%s](%s/) | %s |" % (name, name, cell))
    lines.append("")
    lines.append(END_MARK)
    return "\n".join(lines)


def _normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"


def origin_url(repo: Path) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), "remote", "get-url", "origin"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode == 0:
            url = proc.stdout.decode("utf-8", "replace").strip()
            if url:
                return url
    except OSError:
        pass
    return DEFAULT_URL


def compose(repo: Path, existing: str | None = None):
    """返回 (是否与现有 README 不同, 新 README 全文)。"""
    readme = repo / "README.md"
    if existing is None:
        existing = readme.read_text(encoding="utf-8", errors="replace") if readme.exists() else None

    section = render_section(repo)
    if existing and START_MARK in existing and END_MARK in existing:
        head = existing[: existing.index(START_MARK)]
        tail = existing[existing.index(END_MARK) + len(END_MARK):]
        new_text = head + section + tail
    elif existing and existing.strip():
        new_text = existing.rstrip("\n") + "\n\n## 技能列表\n\n" + section + "\n"
    else:
        new_text = INTRO.format(url=origin_url(repo)) + section + "\n"

    new_text = _normalize(new_text)
    current = _normalize(existing) if existing else ""
    return new_text != current, new_text


def is_stale(repo: Path) -> bool:
    changed, _ = compose(repo)
    return changed


def write(repo: Path) -> bool:
    """写入 README.md，返回是否真的发生了变化。"""
    changed, text = compose(repo)
    if changed:
        (repo / "README.md").write_text(text, encoding="utf-8", newline="\n")
    return changed


if __name__ == "__main__":
    import sys

    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    changed, rendered = compose(root)
    sys.stdout.write(rendered)
    sys.stderr.write("README 需要更新\n" if changed else "README 已是最新\n")
