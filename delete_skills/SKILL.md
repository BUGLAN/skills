---
name: delete-skills
description: 按自然语言指令从 skills 仓库中删除一个或多个 skill，提交并推送到远端（默认 origin master），同时刷新 README.md 技能列表。用于用户要求「删除/移除某个 skill」「把 X 从 skills 仓库删掉」「skills 里不要 X 了」或提到 `/delete_skills`（skill 名为 `delete-skills`）时。
---

# /delete_skills —— 从仓库删除 skill 并推送

## 何时使用

- 用户说「删掉某个 skill」「把 X 从 skills 仓库移除」「以后不要 Y 了」。
- 用户输入 `/delete_skills`。

## 核心行为（必须遵守）

1. **只删仓库里的 skill 目录**（含 `SKILL.md` 的目录）。默认**不动**本机 skills 目录里的真实内容。
2. **自然语言必须先落到明确的名字上**：把用户的话映射到仓库中**确实存在**的 skill 名。
   - 明确点名 → 直接使用；
   - 靠功能/关键词描述 → 用 README 的技能列表（名称 + 简介）匹配；
   - 匹配到 0 个或匹配到多个 → **停下，把候选列给用户选**，绝不猜着删。
3. **删完自动刷新 README**，用中文 Conventional Commits 提交并推送 `origin master`。
4. **远端领先时先停下**：删除前会 `git fetch`，若远端有本地缺少的提交，就停止并让用户先 `/pull_skills`，避免造成分叉。
5. **本机残留要如实告知**：
   - 本机对应位置若是**软链接/junction**（指向被删目录）→ 自动清理该链接，避免悬空；
   - 本机对应位置若是**实体目录** → 默认保留，并明确警告：它仍会出现在本机 skill 列表里，且**下次 `/push_skills` 会把它重新带回仓库**；要一起删干净得加 `--also-local`。
6. 删除是破坏性操作（远端也会同步删除），但历史仍可回滚。执行前用 `--dry-run` 展示将删除的清单。

## 执行步骤

### 1. 定位仓库根与引擎

1. 环境变量 `SKILLS_REPO`；
2. 本 skill 的安装位置：skills 目录里的 `delete_skills` 若是软链/junction，取真实路径上溯到含 `.git` 的目录；
3. 否则询问用户仓库路径。

```powershell
# Windows / PowerShell
(Get-Item -LiteralPath '<skill 目录>').Target        # 其父目录即仓库根
```

```bash
# macOS / Linux
readlink -f '<skill 目录>'                            # 其父目录即仓库根
```

### 2. 把自然语言变成明确的名字

先看仓库里有什么（名称 + 简介）：

```bash
python3 <仓库根>/scripts/skill_sync.py status     # 列出仓库 skill 与状态
# 或直接读 <仓库根>/README.md 的「技能列表」小节
```

规则：**只能删仓库里已经存在的 skill**。候选不唯一或匹配不到时，把候选清单交给用户定，不要自行扩大范围；用户说的名字与仓库里的名字差一个连字符/下划线时，务必先确认（例如 `commit_and_push` 与 `commit-and-push` 是两个不同的 skill）。

### 3. 先看将要发生什么

```bash
python3 <仓库根>/scripts/skill_sync.py delete <skill1> <skill2> --dry-run
```

### 4. 正式删除

```bash
python3 <仓库根>/scripts/skill_sync.py delete <skill1> <skill2>
```

用户同时想清掉本机那份（仅限本机该目录里的对应内容）：

```bash
python3 <仓库根>/scripts/skill_sync.py delete <skill1> --also-local
```

### 5. 按退出码处理

| 退出码 | 含义 | 你要做的 |
|---|---|---|
| 0 | 删除并推送成功（或 dry-run 完成） | 按汇报模板说明删了什么、本机残留如何 |
| 1 | 错误（名字不存在、fetch/push 失败） | 原样转达，不要绕过；名字不存在时列出仓库现有 skill |
| 2 | 已停止（分支不符 / 远端领先） | 让用户先 `/pull_skills` 或切回正确分支 |

### 6. 汇报模板

- 从仓库删除：N 个（逐个名字）；
- README.md 是否已刷新；
- 本机：清理了哪些链接、保留了哪些实体目录（以及「下次 push 会带回来」的警告）；
- 提交：`<短 SHA> <提交标题>`；推送 `origin master` 成功或失败原因。

## 参数速查

| 参数 | 作用 |
|---|---|
| `--dry-run` | 只展示将删除的清单，不写入 |
| `--also-local` | 同时删除本机对应目录（危险，需用户明确要求） |
| `--no-readme` | 不刷新 README.md |
| `--no-commit` / `--no-push` | 只删工作区 / 提交但不推送 |
| `--allow-behind` | 远端领先时也继续（危险） |
| `--dir PATH` / `--agent dsh\|claude\|codex` | 指定本机 skills 目录（只影响本机链接清理） |
| `--repo PATH` | 手动指定仓库路径 |
| `--remote` / `--branch` | 默认 `origin` / `master` |
| `--json` | 机器可读输出 |

## 手工兜底（没有 Python 时）

```bash
git -C <仓库> fetch origin && git -C <仓库> rev-list --count HEAD..origin/master   # 非 0 → 先停下
git -C <仓库> rm -r -- <skill>            # 删除并暂存
# 同步刷新 README 的技能列表，然后：
git -C <仓库> commit -m "chore(skills): 删除 skills（<skill>）"
git -C <仓库> push origin master
```

## 注意事项

- 不要删除 `scripts/`、`.git/` 或任何不含 `SKILL.md` 的内容。
- 不要在用户只要求「从仓库删除」时顺手删掉本机实体目录。
- 本机实体目录被保留是**特意**的设计：删掉别人的工作副本比你预期的影响更大，需要用户显式选择 `--also-local`。
