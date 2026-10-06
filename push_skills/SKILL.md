---
name: push-skills
description: 把本机 skills 目录中的 skill 同步进 skills 仓库（新增与更新都自动纳入），自动刷新 README.md 技能列表，提交并推送到远端（默认 origin master）。用于用户要求「把本机 skills 同步/推送上去」「推送到 GitHub」或提到 `/push_skills`（skill 名为 `push-skills`）时。支持：(1) 只处理含 SKILL.md 的 skill 目录，本机其它内容不关心；(2) 本机独有 skill 默认作为「新增」同步，本机更新过的 skill 默认先用 fetch 校验远端没有领先，然后自动覆盖仓库版本；(3) 远端领先或 fetch 失败时停下提示，不冒进；(4) 中文 Conventional Commits 提交；(5) 推送失败时保留本地提交并如实汇报；(6) README 简介保持全中文——缺中文时由 agent 译好写进 scripts/readme-i18n.json，绝不修改 skill 自己的 description；(7) 遵守 .skillignore 黑名单：名单内的 skill 不新增、不更新、不安装、不进 README，删除过的 skill 因此不会被重新上传。
---

# /push_skills —— 本机 skills → 仓库 → 远端

## 何时使用

- 用户说「把本机 skills 同步到仓库 / 推到 GitHub」「更新我的 skills 仓库」。
- 用户输入 `/push_skills`。
- 本机**新增或更新**了 skill，想让其它设备也能拿到。

如果用户要的是相反方向（远端 → 本机），用 `/pull_skills`；要从仓库删 skill，用 `/delete_skills`。

## 前置条件

- 本机存在 skills 仓库的 git 克隆，且远端已配置（默认 `origin`、分支 `master`）。新设备上先克隆本仓库（`https://github.com/BUGLAN/skills.git`）。
- 本 skill 依赖仓库内的引擎脚本 `<仓库根>/scripts/skill_sync.py`（仅需 Python 3，标准库）。

## 核心行为（必须遵守，不要自行发挥）

1. **本机 skills 目录只取其一**，优先级：`dsh` > `claude` > `codex`。
   - dsh 组按顺序看 `~/.dsh/skills`（DSH rank 400）与 `~/.agents/skills`（DSH rank 500，共享目录）；
   - 组内优先「存在且非空」的那个；整组都不存在时按优先级落到下一组。
   - 脚本会把选中目录和全部候选一起打印出来，**留在汇报里，不要省略**。
2. **只处理 skill**：目录下含 `SKILL.md` 的才算是 skill。本机 skills 目录里的其它文件/目录一律不关心、不动。
3. **本机独有 skill 默认作为「新增」同步进仓库**。若用户明确表示「只更新仓库里已有的、不要加新的」，用 `--only-tracked`。
4. **本机更新过的 skill 默认自动纳入同步并上传**（`--on-conflict=auto`）：
   - 先 `git fetch`；**远端没有领先**时，用本机版本覆盖仓库版本，然后提交推送；
   - **远端领先，或 fetch 失败无法确认**时 → 停下（退出码 2），让用户先 `/pull_skills` 拉平远端，避免把别的设备的改动顶掉；
   - 无条件覆盖用 `--on-conflict=overwrite`（危险，需用户明确同意）；`--on-conflict=ask` 可退回「先提示」的旧行为；`--on-conflict=skip` 只同步新增。
5. **README.md 自动刷新**：push 会按仓库当前 skill 重新生成 README 的技能列表并一起提交推送；新增 skill 时无需手工改 README。`--no-readme` 可跳过。
6. **README 的简介必须是中文，而且绝不动 skill 自己的 description**：
   - README 简介的数据来源是 `<仓库根>/scripts/readme-i18n.json`（中文简介映射表）；表里没有的 skill 会回落到 `SKILL.md` 的英文原文。
   - 引擎会提示「在 README 里显示的还是英文简介」，**翻译这件事由你（agent）做，不要推给用户**：把简介译成中文写进映射表，最少一条 `{"zh": "中文简介"}`，然后重新 push。
   - 想同时获得「原文变了 → 中文简介可能过期」的检测，再补 `src` 字段：该 skill `SKILL.md` 原文 `description` 归一化（连续空白压成一个空格）后的 **sha1 前 12 位**；不填不影响使用。
   - **绝对不要为了让 README 变中文去改 `SKILL.md` 的 `description`**：那会让本机相对仓库永远处于「已更新」状态、反复产生无意义提交，还会偏离上游。映射表只是展示层，skill 本体保持原样。
7. **`.skillignore` 黑名单：名单里的 skill 不新增、不更新、不安装、不进 README**：
   - 它的用途是让「已经删掉的 skill」不会被本机残留副本在下次 push 时带回来；`/delete_skills` 会自动写入名单，用户手动增删忽略项也可以（push 会把 `.skillignore` 的改动一起提交）。
   - 引擎会打印「按 .skillignore 跳过：…」，**这不是静默忽略**，要写进汇报。
   - 若名单里某个 skill **仍存在于仓库中**（矛盾状态），引擎会警告但**不自动删除**：提示用户用 `/delete_skills <名字>` 清理，或从名单里删掉该行以恢复跟踪。
   - 取消忽略后，本机那份会在下次 push 被正常收回仓库。
8. **仓库有、本机没有的 skill 一律不动**，绝不删除仓库内容（删除是 `/delete_skills` 的职责）。
9. **提交信息用中文 Conventional Commits，提交后自动 push**（`origin master`）。不要改动 git 配置。
10. 推送失败时本地提交不丢，如实汇报失败原因和建议的重试命令，**不要** force push。

## 执行步骤

### 1. 定位仓库根与引擎

按顺序确定仓库根：

1. 环境变量 `SKILLS_REPO`；
2. 本 skill 的安装位置：若 skills 目录里的 `push_skills` 是指向仓库的软链/junction，对其取真实路径（realpath）后上溯到含 `.git` 的目录；
3. 都没有就问用户仓库路径。

引擎路径为 `<仓库根>/scripts/skill_sync.py`。`python3` 不存在时用 `python`（Windows 常见）。

```powershell
# Windows / PowerShell：<skill 目录> 指加载到的 SKILL.md 所在目录
(Get-Item -LiteralPath '<skill 目录>').Target        # 例如 E:\repo\skills\push_skills，其父目录即仓库根
```

```bash
# macOS / Linux
readlink -f '<skill 目录>'                            # 其父目录即仓库根
```

### 2. 先看将要发生什么

```bash
python3 <仓库根>/scripts/skill_sync.py push --dry-run
```

把「本机 skills 目录（哪一个、为什么）」「远端是否领先」「新增」「本机更新」「无需改动」「仓库独有（不动）」念给用户。

### 3. 正式同步

```bash
python3 <仓库根>/scripts/skill_sync.py push
```

成功时汇报：新增/更新了哪些 skill、README 是否刷新、提交号与提交信息、推送到的远端与分支。

### 4. 出现「英文简介」提示时（这是 agent 的活）

引擎会列出 README 里仍显示英文简介的 skill。**不要推给用户，也不要改 SKILL.md**，按下面做：

1. 读这些 skill 的 `SKILL.md`，把 `description` 译成中文（保留触发场景与关键信息；GSAP、CSS、React 这类术语可留英文）；
2. 写进 `<仓库根>/scripts/readme-i18n.json`：`"skill名": { "zh": "中文简介……", "src": "<原文 sha1 前 12 位，可省略>" }`；
3. 重新执行 `push`，README 会用中文简介重新生成。

```bash
# 只想补中文、不算 src（最省事）
python3 - <<'PY'
import json, pathlib
p = pathlib.Path("<仓库根>/scripts/readme-i18n.json")
data = json.loads(p.read_text(encoding="utf-8"))
data["<skill名>"] = {"zh": "<中文简介>"}
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY

# 需要 src（原文 sha1 前 12 位）时：
python3 -c "import hashlib,sys;print(hashlib.sha1(' '.join(sys.argv[1].split()).encode()).hexdigest()[:12])" "<SKILL.md 原文 description>"
```

同理，若引擎提示「中文简介可能过期」，说明该 skill 的原文 `description` 变了：重新读一遍、更新映射表里的 `zh` 与 `src` 即可。

### 5. 退出码 2：停下来问人

| 触发原因 | 处理 |
|---|---|
| 远端领先本地 | 让用户先跑 `/pull_skills`，再重新 push；确认要无视时用 `--allow-behind` |
| fetch 失败（离线） | 说明无法确认远端状态；用户确认以本机为准后用 `--on-conflict=overwrite` |
| `--on-conflict=ask` 下的内容差异 | 把差异原样汇报，用户确认后用 `--on-conflict=overwrite`，或 `--on-conflict=skip` 只同步新增 |

**不要**在用户没确认的情况下用 `--on-conflict=overwrite` 顶掉远端历史。

### 6. 汇报模板

- 选中的本机目录 + 为什么选它（同附候选列表）；
- 远端状态：fetch 是否成功、是否领先；
- 新增 N 个 / 更新 N 个 / 一致 N 个 / 跳过 N 个；
- 按 `.skillignore` 跳过 N 个（列出名字）；
- README.md：已刷新 / 本来就是最新 / 按 `--no-readme` 跳过；
- README 中文简介：全部中文 / 刚补了 N 条（列出名字）/ 有 M 条可能过期；
- 提交：`<短 SHA> <提交标题>`；推送：`origin master` 成功或失败原因。

## 参数速查

| 参数 | 作用 |
|---|---|
| `--dry-run` | 只展示计划，不写入 |
| `--on-conflict=auto\|ask\|skip\|overwrite` | 同名内容不同时：自动（默认，先 fetch 校验）/ 停下提示 / 保留仓库版 / 无条件用本机覆盖 |
| `--only-tracked` | 只更新仓库已有的 skill，忽略本机独有 |
| `--no-readme` | 不刷新 README.md |
| `--allow-behind` | 远端领先时也继续（危险） |
| `--dir PATH` | 手动指定本机 skills 目录 |
| `--agent dsh\|claude\|codex` | 只在指定组里挑目录 |
| `--repo PATH` | 手动指定仓库路径 |
| `--remote` / `--branch` | 默认 `origin` / `master` |
| `--no-commit` / `--no-push` | 只同步到工作区 / 提交但不推送 |
| `--json` | 机器可读输出 |

只想单独刷新或校验 README：

```bash
python3 <仓库根>/scripts/skill_sync.py readme          # 按仓库当前内容刷新
python3 <仓库根>/scripts/skill_sync.py readme --check  # 只检查（需更新时退出码 2）
```

README 的中文简介数据文件是 `<仓库根>/scripts/readme-i18n.json`：**由 agent 维护，用户不需要手改**；`description` 保持在 skill 里原样不动。

忽略名单文件是 `<仓库根>/.skillignore`（每行一个 skill 目录名，`#` 开头为注释，不支持通配符）：名单里的 skill 不新增、不更新、不安装、不进 README；push 会把它的改动一起提交，所以用户手动增删忽略项也会被同步到其它设备。

## 手工兜底（没有 Python 时）

```bash
# 1. 本机目录按优先级取其一，例如：
#    ~/.dsh/skills → ~/.agents/skills → ~/.claude/skills → ~/.codex/skills
# 2. 比对（只关心含 SKILL.md 的目录）
diff -rq "<本机目录>/<skill>" "<仓库>/<skill>"
# 3. 同步（本机更新覆盖仓库前，确认远端没有领先：git fetch 后 HEAD..origin/master 为 0）
cp -a "<本机目录>/<skill>/." "<仓库>/<skill>/"
# 4. 刷新 README 技能列表，然后提交并推送（中文 Conventional Commits）
git -C <仓库> add -- <仓库>/<skill> <仓库>/README.md
git -C <仓库> commit -m "feat(skills): 同步本机 skills"
git -C <仓库> push origin master
```

## 注意事项

- **不要**为了让仓库「干净」而删除仓库里本机没有的 skill。
- **不要**把本机 skills 目录里的非 skill 内容搬进仓库。
- 仓库工作区原本就有未提交改动时，引擎只提交本次同步的 skill 路径与 README.md，其余改动保持原样（会提示）。
- README.md 的技能列表位于 `<!-- SKILLS:START -->` / `<!-- SKILLS:END -->` 之间；标记之外的手写内容不会被覆盖。
