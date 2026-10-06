---
name: watchdog
description: 使用于用户明确输入 "/watchdog" 或明确要求在代码修改完成后执行 watchdog 记录、验证、录屏、提审流程时。
license: MIT
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Watchdog 三阶段流程

## 核心规则

`/watchdog` 会显式启用本 Skill，但本 Skill **不会改变 Claude Code 的默认编码行为**。

当用户输入类似下面的请求时：

```text
/watchdog 将"留言板"这几个字修改为蓝色
```

必须严格按三个阶段执行：

1. 先执行环境发现阶段，只读取 watchdog 元信息
2. 再按普通编码任务完成用户要求的代码修改
3. 代码修改完成后，再进入 watchdog 的记录、重启、E2E、录屏、提审流程

## 何时使用

仅在以下情况使用本 Skill：

- 用户明确输入 `/watchdog`
- 用户明确要求把已完成的改动录入 watchdog
- 用户明确要求执行 watchdog 的验证、录屏或审阅流程

以下情况**不要**使用本 Skill：

- 普通的修复 bug 请求
- 普通的新增功能请求
- 用户没有明确提到 `/watchdog`

## 不可违反的顺序

只要启用了本 Skill，就必须遵守下面的顺序：

### 阶段零：环境发现阶段（只读）

开始编码前，先读取 watchdog 中已经存在的事实信息，避免猜测：

- 当前 label 的 session 列表
- 各 session 的启动命令
- 各 session 的工作目录
- session 状态
- 可用于推断端口或入口 URL 的线索

这一阶段只允许读取，不允许执行任何会改变 watchdog 状态的操作。

在这个阶段：

- 默认且优先运行 `watchdog get-status [label] --json`
- 仅在 `get-status` 无法提供足够事实时，才允许补充运行 `watchdog label sessions <label> --json`
- 仅在 `get-status` 无法提供足够事实时，才允许补充运行 `watchdog status <label> --json`
- 仅在排障或兼容旧流程时，才允许补充运行 `watchdog fix-context <label> --json`
- 不允许创建 attempt
- 不允许记录改动
- 不允许更新 label 状态
- 不允许因为读取到 watchdog 信息就改变 Claude Code 的默认编码方式
- 不允许把 watchdog CLI 变成实现策略的决定者，它只提供事实，不决定如何写代码

环境发现结束后，必须先整理一份简短摘要，再进入编码阶段。摘要至少包括：

- 当前 label
- 目标 session_id
- 启动命令
- 工作目录
- 已确认的服务 URL 或端口
- 仍未确认的信息

### 阶段一：默认编码阶段

先把用户请求当作普通编码任务处理：

- 阅读相关文件
- 修改代码
- 运行必要验证
- 确认代码改动已经完成

在这个阶段：

- 不要让 watchdog CLI 决定如何编码
- 不要因为启用了 `/watchdog` 而改变实现策略
- 不要在代码尚未完成前就开始 attempt 记录流程
- 如果环境发现阶段仍缺少关键事实，例如页面入口 URL 或端口，先明确指出缺失项，再向用户确认；不要猜测

### 阶段二：Watchdog 后处理阶段

只有在代码改动已经完成后，才执行下面的 watchdog 流程：

1. 确定目标 label
2. 视需要获取上下文
3. 创建 attempt
4. 记录改动文件
5. 重启相关 session
6. 视需要执行 E2E 测试和录屏
7. 记录验证结果
8. 更新状态为等待审阅
9. 告知用户审阅地址

## 前提条件

在执行 watchdog 后处理前，确保以下服务已运行：

- `watchdog run <label> "<command>"`，即目标服务已通过 watchdog 启动
- `watchdog web`，即 Web 界面已运行

本 Skill **不会**启动这些服务，只会使用和重启已存在的 session。

## 阶段零详细流程：环境发现

### 0.1 确定目标 Label

如果用户已经指定 label，直接使用该 label。否则优先读取当前目录 `.watchdog/config.json` 中的 `current_label`：

```bash
watchdog get-status --json
```

如果 `current_label` 缺失或无效，再根据错误提示中的候选 labels 选择目标 label；必要时可补充列出活跃 labels：

```bash
watchdog labels --active --json
```

### 0.2 读取 session 元信息

默认只使用下面这一条命令获取环境事实：

```bash
watchdog get-status [label] --json
```

其中：

- 启动命令以 `sessions[*].command` 为准
- 工作目录以 `sessions[*].cwd` 或 `workspace.workspace_root` 为准
- 目标 session 以 `derived.recommended_session_id` 和 `sessions` 返回的列表与状态为准
- 端口或 URL 线索以 `derived.url_port_hints` 为准

只有在 `get-status` 返回的信息不足以区分 session 用途时，才允许补充使用：

```bash
watchdog label sessions <label> --json
watchdog status <label> --json
```

如果存在多个 session，需要根据 `command` 和状态区分其用途，例如：

- 前端服务 session
- 后端服务 session
- Web 管理服务 session

不要在未区分 session 角色前就假设某个端口或页面入口属于目标服务。

### 0.3 读取补充上下文

如果 `get-status` 仍缺少任务目标、失败历史或建议动作，再补充读取：

```bash
watchdog fix-context <label> --json
```

这一步只是补充信息，不是环境发现的默认主来源。

### 0.4 端口与入口 URL 推断规则

端口和入口 URL 必须按下面的优先级确认：

1. 如果用户 prompt、已有上下文或 label goal 已明确给出 URL，则优先使用显式 URL
2. 否则，从 `watchdog get-status [label] --json` 返回的 `derived.url_port_hints` 中提取端口线索
3. 如果 command 中包含显式端口参数，如 `8000`、`--port 3000`、`http.server 8888`，优先采用这些端口线索
4. 如果有多个 session，根据 `sessions[*].command` 判断哪个是前端入口、哪个是后端 API、哪个是管理服务
5. 如果仍无法确认页面入口 URL 或端口，必须先说明“缺少明确 URL/端口事实”，然后向用户确认

禁止编造端口、URL 或启动方式。

### 0.5 编码前摘要

在开始编码前，必须先整理并显式说明一份简短事实摘要。建议格式如下：

```text
环境发现摘要：
- Label: <label>
- 目标 session: <session_id>
- 启动命令: <command>
- 工作目录: <cwd>
- 已确认 URL/端口: <facts>
- 未确认信息: <unknowns>
```

只有在这份摘要完成后，才进入默认编码阶段。

## 阶段二详细流程：Watchdog 后处理

### 1. 确定目标 Label

如果用户已经指定 label，直接使用该 label。否则列出活跃 labels 供选择：

```bash
watchdog labels --active --json
```

### 2. 获取上下文

默认情况下，这一步是**补充上下文步骤**，不是启动信息的主来源。

仅在以下情况执行：

- 用户明确要求先看 watchdog 上下文
- 你需要参考历史 attempts 或近期错误来补充验证信息
- 你需要确认应当重启哪个 session

命令：

```bash
watchdog fix-context <label> --json
```

这会返回：

- `goal`
- `failed_sessions`
- `recent_errors`
- `previous_attempts`
- `suggested_actions`

### 3. 创建 Attempt

在代码修改已经完成后，创建新的 attempt：

```bash
watchdog attempt create <label> --goal "<任务目标>"
```

记录返回的 `attempt_number`，后续步骤需要使用。

### 4. 记录改动

修改完成后，记录本次变更涉及的文件：

```bash
watchdog attempt record-changes <label> <attempt_number> --files "file1.py,file2.py"
```

如果需要更详细记录，也可以通过 JSON 输入：

```bash
echo '{"files": ["file1.py", "file2.py"], "diff": "...diff内容..."}' | watchdog attempt record-changes <label> <attempt_number> --json-input
```

### 5. 分类改动并确定重启范围

在重启或执行可视化验证前，先根据“改动文件 + 任务意图 + 验证入口”判断本次改动类型。

#### 5.1 改动分类规则

优先依据以下信息分类：

- 改动文件类型、路径、模块归属
- 用户任务目标
- 最终验证是通过首屏静态页面、交互动作，还是后端接口/脚本完成

默认分类如下：

- **纯静态 UI 改动**：颜色、字体、间距、边框、阴影、静态布局等首屏可直接观察的变化
- **交互型 UI 改动**：点击、输入、hover、展开/收起、tab 切换、弹窗、异步加载、状态切换、动画流程等需要过程证据的变化
- **纯后端改动**：主要改动后端逻辑、接口、脚本或服务，且验证不依赖前端页面
- **混合改动**：同时涉及前后端，或仅看改动文件和任务意图仍无法可靠判断影响面

当文件归类和任务意图冲突时，按更保守的一侧处理。

#### 5.2 Session 重启决策矩阵

重启目标 session 时，应以前置环境发现阶段确认的 `session_id`、`command` 和服务角色为准，不要在此时重新猜测应该重启哪个服务。

默认规则：

- 仅 UI 改动：只重启前端 session
- 仅后端改动且任务不依赖前端验证：只重启后端 session
- 仅后端改动但结果要通过前端页面验证或体现：重启前后端相关 session
- 混合改动或无法可靠判断影响面：重启所有相关业务 session
- Web 管理服务或非目标业务 session 不默认重启，除非本次改动直接涉及它们

如果代码改动需要重新加载服务，重启对应 session：

```bash
watchdog restart <label> <session_id>
```

可以先查询 session 列表：

```bash
watchdog label sessions <label> --json
```

### 6. 执行截图、E2E 和录屏

#### 6.1 验证分级决策矩阵

验证方式按改动类型分级：

- **纯静态 UI 改动**：默认要求截图，不要求录屏
- **交互型 UI 改动**：要求截图 + 录屏；如果交互本身构成关键验证路径，还应执行对应 E2E 操作
- **纯后端改动**：默认不强制截图或录屏，除非用户明确要求，或结果需要通过可视界面证明
- **混合改动**：至少按更高要求的一侧执行；通常需要截图，如涉及交互流程则同时录屏

可直接按下面理解：

- 样式轻量修改，例如标题颜色、字号、静态布局微调：截图即可
- 需要点击、输入、展开、切换或等待状态变化后才能看到结果：截图 + 录屏
- 后端接口或脚本修复，且无需启动前端场景：以接口/测试验证为主，不强制截图或录屏

#### 6.2 何时必须保留截图

以下情况默认应保留截图：

- 纯静态 UI 改动
- 交互型 UI 改动的关键结果页、关键状态页或最终落点页
- 用户明确要求提供可视化证据

截图文件建议保存到：

```text
.watchdog/labels/<label>/attempts/<attempt_number>/screenshots/
```

#### 6.3 浏览器工具约束

执行截图、E2E 测试和录屏时，默认且优先必须使用 `agent-browser` CLI。

禁止直接使用以下工具替代 `agent-browser`：

- `chrome-devtools` MCP
- 其他浏览器类 MCP 工具
- 任何未明确要求的浏览器自动化工具

必须先实际尝试 `agent-browser`，不能只在文字上说使用 `agent-browser`，实际却调用别的浏览器工具。

只有在以下情况才允许降级：

- 本机未安装 `agent-browser`
- `agent-browser` 命令不可用
- `agent-browser` 明确报错且无法继续完成任务

如果发生降级，必须先明确说明：

1. 为什么 `agent-browser` 不可用
2. 将改用什么工具
3. 哪些验证步骤会继续执行

#### 6.4 使用 agent-browser 执行截图和录屏

**重要**：Watchdog 不提供截图或录屏编排 CLI，需要使用 `agent-browser` 完成截图、端到端测试和录屏。

典型流程：

```bash
agent-browser open <url>
agent-browser snapshot -i
agent-browser fill @e1 "text"
agent-browser click @e2
agent-browser wait --load networkidle
agent-browser screenshot result.png
agent-browser record start recording.webm
# ...执行交互...
agent-browser record stop
```

截图和录屏不一定同时需要：

- 纯静态 UI：至少截图
- 交互型 UI：截图 + 录屏
- 非 UI 改动：按验证需要决定是否截图

录屏文件建议保存到：

```text
.watchdog/labels/<label>/attempts/<attempt_number>/recording.webm
```

### 7. 记录验证结果

验证通过：

```bash
watchdog attempt validate <label> <attempt_number> --passed --e2e --recording --recording-path <recording_path>
```

如果本次验证只有截图，没有录屏，仍然允许记录为通过；此时不需要传 `--recording` 或 `--recording-path`，但应在 attempt 摘要中说明截图产物位置和验证依据。

验证失败：

```bash
watchdog attempt validate <label> <attempt_number> --failed --error "具体错误信息"
```

### 8. 更新状态

```bash
watchdog label status <label> awaiting_review
```

### 9. 通知用户审阅

告知用户访问 Web 界面：

```text
处理完成，请访问 http://localhost:8765/label/<label> 审阅：
- 查看截图或录屏验证结果
- 查看代码改动
- 确认通过或拒绝
```

## 会话管理

### 重启服务

```bash
watchdog restart <label> <session_id>
```

### 停止服务

```bash
watchdog stop <label> <session_id>
watchdog stop <label>
```

## 示例

### 示例：修改页面标题颜色并在完成后执行 watchdog

```text
用户请求：
/watchdog 将“留言板”这几个字修改为蓝色
```

正确执行顺序：

1. 先确定 label
2. 调用 `watchdog get-status [label] --json`，一次读取 session、启动命令、工作目录、状态、attempt 摘要和失败上下文
3. 根据 command、prompt 或现有上下文确认页面入口 URL 或端口
4. 输出一份环境发现摘要
5. 再按普通编码流程修改前端代码，把“留言板”文字改成蓝色
6. 完成本地验证，确认页面表现正确
7. 创建 attempt
8. 记录修改过的文件
9. 依据改动类型决定需要重启哪些 session
10. 如果只是样式轻量改动，使用 agent-browser 截图验证；如果涉及交互，再执行录屏验证
11. 调用 `watchdog attempt validate`
12. 调用 `watchdog label status <label> awaiting_review`
13. 告知用户去 Web 页面审阅
```

错误做法：

- 编码前不读取任何 watchdog 事实，直接猜测端口、URL 或启动方式
- 一开始就运行 watchdog 流程并用它接管编码
- 在代码未完成前就创建 attempt 并记录结果
- 把 `/watchdog` 理解成“改用另一套编码流程”

## 注意事项

1. **`/watchdog` 只改变后处理，不改变编码方式**：编码任务仍然先按 Claude Code 默认方式完成。
2. **默认先发现，后编码，再记录**：先只读获取环境事实，再编码，最后才进入 attempt 和审阅流程。
3. **环境发现阶段只读**：默认读取 `get-status` 不算污染流程；补充读取 session、status、fix-context 也不算污染流程；创建 attempt、记录改动、更新状态才算进入后处理。
4. **本 Skill 不负责启动服务**：只使用已存在的 watchdog session，并在需要时重启。
5. **不要猜测启动信息**：启动命令、工作目录、session 状态以 watchdog CLI 返回结果为准。
6. **端口与 URL 允许推断，但不允许编造**：有明确事实就用事实；没有事实就说明缺口并向用户确认。
7. **UI 验证采用分级策略**：纯静态 UI 改动默认截图即可；交互型 UI 改动要求截图 + 录屏。
8. **重启范围按影响面分流**：仅 UI 改动只重启前端 session；仅后端改动且不依赖前端验证时只重启后端；混合或不确定场景重启所有相关业务 session。
9. **E2E 工具必须一致**：如果声明使用 `agent-browser`，实际执行时也必须先调用 `agent-browser`，不能偷偷切换到 `chrome-devtools` MCP。
10. **优先使用结构化输出**：阶段 0 默认使用 `watchdog get-status --json`；其他命令能加 `--json` 时尽量加，方便后续解析和记录。
11. **人类审阅是终点**：完成记录和验证后，最终状态应进入 `awaiting_review`，等待用户在 Web 界面确认。
