---
name: pull-skills
description: 从远端拉取 skills 仓库最新内容，并把本机缺失的 skill 安装到本机 skills 目录（优先软链接，用户要求或系统不支持时才复制）。用于用户要求「拉取/同步 skills 到本机」「在新设备上装好 skills」或提到 `/pull_skills`（skill 名为 `pull-skills`）时。默认 origin master；仓库工作区有未提交改动时立即停止并告知用户，不做任何覆盖；本机有、仓库没有的 skill 一律不动。
---

# /pull_skills —— 远端 → 仓库 → 本机

## 何时使用

- 用户说「拉一下 skills」「把仓库里的 skills 同步到本机」「换设备后装好 skills」。
- 用户输入 `/pull_skills`。
- 需要补齐本机缺失的 skill。

反方向（本机 → 仓库 → 远端）用 `/push_skills`。

## 前置条件

- 本机存在 skills 仓库的 git 克隆，远端已配置（默认 `origin`、分支 `master`）。
- **新设备上还没有克隆时**：先用用户给的仓库地址克隆到任意目录（本仓库为 `https://github.com/BUGLAN/skills.git`），再继续。克隆后本 skill 才会随 `/pull_skills` 一起安装到本机 skills 目录。
- 引擎脚本 `<仓库根>/scripts/skill_sync.py`（仅需 Python 3，标准库）。

## 核心行为（必须遵守）

1. **先查仓库工作区是否干净**：只要有未提交改动（uncommitted），**立即停止，不 pull、不动本机**，把改动列表原样告知用户，并给出处理建议（先 `/push_skills` 提交推送，或 `git stash` / 手动处理）。
2. 干净后执行 `git pull --ff-only origin master`；分叉或失败就如实报错，**不要** reset、**不要** force。
3. **本机 skills 目录只取其一**，优先级 `dsh` > `claude` > `codex`（dsh 组依次看 `~/.dsh/skills`、`~/.agents/skills`，组内优先「存在且非空」）。脚本会打印选中目录与全部候选，**必须写进汇报**。
4. **同步本机**：
   - 本机缺失的 skill → 安装；
   - **安装默认软链接**（本机目录里的 `<skill>` 指向仓库里的同名目录，之后仓库更新即自动生效）；
   - Windows 上软链接创建失败会退化为 junction（无需管理员）；
   - **只有用户明确说「复制」时才用 `--copy`**；macOS/Windows 上因文件系统（外接盘、exFAT、网络盘）或权限导致软链接失败时，先原样报错，**征得用户同意后**再用 `--copy` 重跑，不要静默改成复制。
5. **本机有、仓库没有的 skill：一律不动**，只在汇报里列为「本机独有（未处理）」。绝不删除、绝不搬走。
6. **已存在但内容与仓库不一致的 skill（含实体目录）→ 不覆盖，先告知**：列出差异，让用户决定「保留本地改动就先 /push_skills」还是「丢弃本地改动用 `--force` 覆盖」。
7. 全部动作都是幂等的：重复执行只会有「已就位 / 无需安装」的结果。

## 执行步骤

### 1. 定位仓库根与引擎

1. 环境变量 `SKILLS_REPO`；
2. 本 skill 安装位置：skills 目录里的 `pull_skills` 若是软链/junction，取其真实路径上溯到含 `.git` 的目录；
3. 否则询问用户仓库路径。

定位仓库的具体办法（本 skill 通常以软链接安装，解析软链即可）：

```powershell
# Windows / PowerShell：<skill 目录> 指加载到的 SKILL.md 所在目录
(Get-Item -LiteralPath '<skill 目录>').Target        # 例如 E:\repo\skills\pull_skills，其父目录即仓库根
```

```bash
# macOS / Linux
readlink -f '<skill 目录>'                            # 其父目录即仓库根
```

三种都拿不到时，直接问用户仓库克隆在哪个路径，或用 `--repo` 显式传入。

### 2. 先 dry-run 确认计划

```bash
python3 <仓库根>/scripts/skill_sync.py pull --dry-run
```

注意：dry-run **不会**检查远端、也**不会**真正 pull，只演示安装计划。工作区脏的拦截在正式运行时才生效。

### 3. 正式拉取并同步

```bash
python3 <仓库根>/scripts/skill_sync.py pull
```

用户明确要求复制安装时：

```bash
python3 <仓库根>/scripts/skill_sync.py pull --copy
```

以下是危险操作，**必须**先拿到用户对具体差异的明确同意：

```bash
# 用仓库版本覆盖本机不一致的 skill（会丢弃本地改动）
python3 <仓库根>/scripts/skill_sync.py pull --force
```

### 4. 按退出码处理

| 退出码 | 含义 | 你要做的 |
|---|---|---|
| 0 | 完成或本来就最新 | 汇报安装了什么、本机独有哪些被忽略 |
| 1 | 错误（fetch/pull/安装失败） | 原样转达错误与引擎给的建议，不要绕过 |
| 2 | 已停止，需要用户决策 | 把「未提交改动」或「不一致清单」原样汇报，等用户指示 |

### 5. 汇报模板

- 远端 / 分支 / 拉取后的 HEAD；
- 选中的本机目录 + 为什么（同附候选列表）；
- 新安装：N 个（逐个名字 + 安装方式：软链 / junction / 复制）；
- 已就位：N 个；
- 不一致未覆盖：N 个（列出名字与差异）；
- 本机独有未处理：N 个；
- 若退出码为 2，明确写出「已停止，未覆盖任何东西」。

## 参数速查

| 参数 | 作用 |
|---|---|
| `--dry-run` | 只展示安装计划，不写入 |
| `--copy` | 用复制安装（需用户明确要求） |
| `--force` | 用仓库版本覆盖本机不一致的 skill（会丢本地改动，需用户同意） |
| `--no-pull` | 不访问远端，只用当前仓库内容同步本机 |
| `--allow-dirty` | 工作区脏时仍继续（危险，默认禁止） |
| `--dir PATH` | 手动指定本机 skills 目录 |
| `--agent dsh\|claude\|codex` | 只在指定组里挑目录 |
| `--repo PATH` | 手动指定仓库路径 |
| `--remote` / `--branch` | 默认 `origin` / `master` |
| `--json` | 机器可读输出 |

`status` 子命令可做只读诊断，随时可用：

```bash
python3 <仓库根>/scripts/skill_sync.py status
```

## 手工兜底（没有 Python 时）

```bash
git -C <仓库> status --porcelain        # 非空 → 立即停下告知用户
git -C <仓库> pull --ff-only origin master
# 本机目录按优先级取其一：~/.dsh/skills → ~/.agents/skills → ~/.claude/skills → ~/.codex/skills
# 只安装本机缺失的 skill；默认软链，不要顺手覆盖已存在的
ln -s "<仓库>/<skill>" "<本机目录>/<skill>"        # macOS / Linux
# Windows：mklink /J "<本机目录>\<skill>" "<仓库>\<skill>"
```

## 注意事项

- 永远不要为了「对齐仓库」而删除本机独有 skill，也不要删除本机未被仓库跟踪的内容。
- 软链接失败是**预期内的跨平台差异**，处理方式是明确报错 + 询问用户是否改用 `--copy`，不是静默复制。
- 本机目录若原本是指向别处（例如 `~/.claude/skills` 里的 junction 指向 `~/.agents/skills`）且内容与仓库一致，引擎视为「已就位」，不会改写链接。
