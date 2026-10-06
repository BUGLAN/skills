---
name: push-skills
description: 把本机 skills 目录中的 skill 同步进 skills 仓库，并自动提交、推送到远端（默认 origin master）。用于用户要求「把本机 skills 同步/推送上去」「推送到 GitHub」或提到 `/push_skills`（skill 名为 `push-skills`）时。支持：(1) 只处理含 SKILL.md 的 skill 目录，本机其它内容不关心；(2) 本机独有 skill 默认作为「新增」同步进仓库，也可用 --only-tracked 只更新仓库已有的；(3) 同名但内容不同时先停下提示、不静默覆盖；(4) 中文 Conventional Commits 提交；(5) 推送失败时保留本地提交并如实汇报。
---

# /push_skills —— 本机 skills → 仓库 → 远端

## 何时使用

- 用户说「把本机 skills 同步到仓库 / 推到 GitHub」「更新我的 skills 仓库」。
- 用户输入 `/push_skills`。
- 本机新增或改动了 skill，想让其它设备也能拿到。

如果用户要的是相反方向（远端 → 本机），用 `/pull_skills`。

## 前置条件

- 本机存在 skills 仓库的 git 克隆，且远端已配置（默认 `origin`、分支 `master`）。新设备上先克隆本仓库（`https://github.com/BUGLAN/skills.git`）。
- 本 skill 依赖仓库内的引擎脚本 `<仓库根>/scripts/skill_sync.py`（仅需 Python 3，标准库）。

## 核心行为（必须遵守，不要自行发挥）

1. **本机 skills 目录只取其一**，优先级：`dsh` > `claude` > `codex`。
   - dsh 组按顺序看 `~/.dsh/skills`（DSH rank 400）与 `~/.agents/skills`（DSH rank 500，共享目录）；
   - 组内优先「存在且非空」的那个；整组都不存在时按优先级落到下一组。
   - 脚本会把选中目录和全部候选一起打印出来，**留在汇报里，不要省略**。
2. **只处理 skill**：目录下含 `SKILL.md` 的才算是 skill。本机 skills 目录里的其它文件/目录（非 skill 内容、其它工具的东西）一律不关心、不动。
3. **本机独有 skill 默认作为「新增」同步进仓库**。若用户明确表示「只更新仓库里已有的、不要加新的」，用 `--only-tracked`。
4. **仓库有、本机没有的 skill 一律不动**，绝不删除仓库内容。
5. **同名但内容不同 → 先提示、不覆盖**：引擎默认以退出码 2 停下并列出差异。此时必须把差异原样汇报给用户，得到明确同意后才能加 `--on-conflict=overwrite` 重跑。
6. **提交信息用中文 Conventional Commits，提交后自动 push**（`origin master`）。不要改动 git 配置。
7. 推送失败时本地提交不丢，如实汇报失败原因和建议的重试命令，**不要** force push。

## 执行步骤

### 1. 定位仓库根与引擎

按顺序确定仓库根：

1. 环境变量 `SKILLS_REPO`；
2. 本 skill 的安装位置：若 skills 目录里的 `push_skills` 是指向仓库的软链/junction，对其取真实路径（realpath）后上溯到含 `.git` 的目录；
3. 都没有就问用户仓库路径。

引擎路径为 `<仓库根>/scripts/skill_sync.py`。`python3` 不存在时用 `python`（Windows 常见）。

定位仓库的具体办法（本 skill 通常以软链接安装，解析软链即可）：

```powershell
# Windows / PowerShell：<skill 目录> 指加载到的 SKILL.md 所在目录
(Get-Item -LiteralPath '<skill 目录>').Target        # 例如 E:\repo\skills\push_skills，其父目录即仓库根
```

```bash
# macOS / Linux
readlink -f '<skill 目录>'                            # 其父目录即仓库根
```

三种都拿不到时，直接问用户仓库克隆在哪个路径，或用 `--repo` 显式传入。

### 2. 先看将要发生什么

```bash
python3 <仓库根>/scripts/skill_sync.py push --dry-run
```

把「本机 skills 目录（哪一个、为什么）」「新增」「同名不同」「无需改动」「仓库独有（不动）」念给用户。

### 3. 正式同步

```bash
python3 <仓库根>/scripts/skill_sync.py push
```

成功时汇报：新增/覆盖了哪些 skill、提交号与提交信息、推送到的远端与分支。

### 4. 退出码 2：停下来问人

引擎会打印每个冲突 skill 的具体差异（新增/修改/删除的文件）。**不要自作主张覆盖**，把差异汇报给用户并给出两个选项：

```bash
# 用户确认用本机版本覆盖仓库
python3 <仓库根>/scripts/skill_sync.py push --on-conflict=overwrite

# 用户只想同步新增、冲突的先不动
python3 <仓库根>/scripts/skill_sync.py push --on-conflict=skip
```

### 5. 汇报模板

- 选中的本机目录 + 为什么选它（同时候选列表）；
- 新增 N 个 / 覆盖 N 个 / 一致 N 个 / 跳过 N 个；
- 提交：`<短 SHA> <提交标题>`；推送：`origin master` 成功或失败原因。

## 参数速查

| 参数 | 作用 |
|---|---|
| `--dry-run` | 只展示计划，不写入 |
| `--on-conflict=ask\|skip\|overwrite` | 同名内容不同时：停下提示（默认）/ 保留仓库版 / 用本机覆盖 |
| `--only-tracked` | 只更新仓库已有的 skill，忽略本机独有 |
| `--dir PATH` | 手动指定本机 skills 目录 |
| `--agent dsh\|claude\|codex` | 只在指定组里挑目录 |
| `--repo PATH` | 手动指定仓库路径 |
| `--remote` / `--branch` | 默认 `origin` / `master` |
| `--no-commit` / `--no-push` | 只同步到工作区 / 提交但不推送 |
| `--json` | 机器可读输出 |

## 手工兜底（没有 Python 时）

```bash
# 1. 本机目录按优先级取其一，例如：
#    ~/.dsh/skills → ~/.agents/skills → ~/.claude/skills → ~/.codex/skills
# 2. 比对（只关心含 SKILL.md 的目录）
diff -rq "<本机目录>/<skill>" "<仓库>/<skill>"
# 3. 同步（同名不同内容必须先征得用户同意）
cp -a "<本机目录>/<skill>/." "<仓库>/<skill>/"
# 4. 提交并推送（中文 Conventional Commits）
git -C <仓库> add -- <仓库>/<skill>
git -C <仓库> commit -m "feat(skills): 同步本机 skills"
git -C <仓库> push origin master
```

## 注意事项

- **不要**为了让仓库「干净」而删除仓库里本机没有的 skill。
- **不要**把本机 skills 目录里的非 skill 内容搬进仓库。
- 仓库工作区原本就有未提交改动时，引擎只提交本次同步的 skill 路径，其余改动保持原样（会提示）。若用户希望先处理这些改动，先按用户意愿处理。
- macOS/Windows 差异只会影响 `pull_skills` 的安装方式（软链接 vs 复制），push 侧只做文件复制。
