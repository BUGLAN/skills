---
name: agent-browser
description: 面向 AI agent 的浏览器自动化 CLI。当用户需要与网站交互时使用，包括打开页面、填写表单、点击按钮、截图、提取数据、测试 Web 应用，或自动化任何浏览器任务。触发场景包括「打开一个网站」「填写表单」「点一个按钮」「截一张图」「抓取页面数据」「测试这个 Web 应用」「登录某个网站」「自动化浏览器操作」等请求，以及任何需要程序化网页交互的任务。
allowed-tools: Bash(npx agent-browser:*), Bash(agent-browser:*)
---

# 使用 agent-browser 进行浏览器自动化

该 CLI 通过 CDP 直接驱动 Chrome/Chromium。可通过 `npm i -g agent-browser`、`brew install agent-browser` 或 `cargo install agent-browser` 安装。运行 `agent-browser install` 下载 Chrome；运行 `agent-browser upgrade` 升级到最新版本。

## 核心工作流

每次浏览器自动化都遵循以下模式：

1. **导航**：`agent-browser open <url>`
2. **快照（snapshot）**：`agent-browser snapshot -i`（获取 `@e1`、`@e2` 这样的元素 ref）
3. **交互**：用 ref 完成点击、填写、选择
4. **重新快照**：页面导航或 DOM 变化后，重新获取最新的 ref

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output: @e1 [input type="email"], @e2 [input type="password"], @e3 [button] "Submit"

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

## 命令串联

可以在一次 shell 调用中用 `&&` 串联多条命令。浏览器由后台守护进程（daemon）保持运行，在命令之间持续存活，因此串联是安全的，也比分开调用更高效。

```bash
# Chain open + wait + snapshot in one call
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser snapshot -i

# Chain multiple interactions
agent-browser fill @e1 "user@example.com" && agent-browser fill @e2 "password123" && agent-browser click @e3

# Navigate and capture
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser screenshot page.png
```

**何时串联：** 后续步骤不依赖中间命令输出时，用 `&&` 串联（如 open + wait + screenshot）；需要先解析输出再继续时，分开执行（如先 snapshot 找到 ref，再用这些 ref 交互）。

## 处理登录认证

自动化需要登录的网站时，按场景选择合适的方式：

**方式一：从用户浏览器导入登录态（一次性任务的最快选择）**

```bash
# Connect to the user's running Chrome (they're already logged in)
agent-browser --auto-connect state save ./auth.json
# Use that auth state
agent-browser --state ./auth.json open https://app.example.com/dashboard
```

状态文件以明文保存会话 token——请加入 `.gitignore`，不再使用时及时删除。设置 `AGENT_BROWSER_ENCRYPTION_KEY` 可启用静态加密。

**方式二：持久化 profile（重复任务的最简方案）**

```bash
# First run: login manually or via automation
agent-browser --profile ~/.myapp open https://app.example.com/login
# ... fill credentials, submit ...

# All future runs: already authenticated
agent-browser --profile ~/.myapp open https://app.example.com/dashboard
```

**方式三：会话名（自动保存/恢复 cookies 与 localStorage）**

```bash
agent-browser --session-name myapp open https://app.example.com/login
# ... login flow ...
agent-browser close  # State auto-saved

# Next time: state auto-restored
agent-browser --session-name myapp open https://app.example.com/dashboard
```

**方式四：认证保险库（凭据加密存储，按名称登录）**

```bash
echo "$PASSWORD" | agent-browser auth save myapp --url https://app.example.com/login --username user --password-stdin
agent-browser auth login myapp
```

`auth login` 先以 `load` 方式导航，然后等待登录表单选择器出现后再填写/点击，在加载较慢的 SPA 登录页上更可靠。

**方式五：状态文件（手动保存/加载）**

```bash
# After logging in:
agent-browser state save ./auth.json
# In a future session:
agent-browser state load ./auth.json
agent-browser open https://app.example.com/dashboard
```

OAuth、双因素认证（2FA）、基于 cookie 的认证以及 token 刷新等模式，参见 [references/authentication.md](references/authentication.md)。

## 核心命令

```bash
# Navigation
agent-browser open <url>              # Navigate (aliases: goto, navigate)
agent-browser close                   # Close browser

# Snapshot
agent-browser snapshot -i             # Interactive elements with refs (recommended)
agent-browser snapshot -s "#selector" # Scope to CSS selector

# Interaction (use @refs from snapshot)
agent-browser click @e1               # Click element
agent-browser click @e1 --new-tab     # Click and open in new tab
agent-browser fill @e2 "text"         # Clear and type text
agent-browser type @e2 "text"         # Type without clearing
agent-browser select @e1 "option"     # Select dropdown option
agent-browser check @e1               # Check checkbox
agent-browser press Enter             # Press key
agent-browser keyboard type "text"    # Type at current focus (no selector)
agent-browser keyboard inserttext "text"  # Insert without key events
agent-browser scroll down 500         # Scroll page
agent-browser scroll down 500 --selector "div.content"  # Scroll within a specific container

# Get information
agent-browser get text @e1            # Get element text
agent-browser get url                 # Get current URL
agent-browser get title               # Get page title
agent-browser get cdp-url             # Get CDP WebSocket URL

# Wait
agent-browser wait @e1                # Wait for element
agent-browser wait --load networkidle # Wait for network idle
agent-browser wait --url "**/page"    # Wait for URL pattern
agent-browser wait 2000               # Wait milliseconds
agent-browser wait --text "Welcome"    # Wait for text to appear (substring match)
agent-browser wait --fn "!document.body.innerText.includes('Loading...')"  # Wait for text to disappear
agent-browser wait "#spinner" --state hidden  # Wait for element to disappear

# Downloads
agent-browser download @e1 ./file.pdf          # Click element to trigger download
agent-browser wait --download ./output.zip     # Wait for any download to complete
agent-browser --download-path ./downloads open <url>  # Set default download directory

# Network
agent-browser network requests                 # Inspect tracked requests
agent-browser network requests --type xhr,fetch  # Filter by resource type
agent-browser network requests --method POST   # Filter by HTTP method
agent-browser network requests --status 2xx    # Filter by status (200, 2xx, 400-499)
agent-browser network request <requestId>      # View full request/response detail
agent-browser network route "**/api/*" --abort  # Block matching requests
agent-browser network har start                # Start HAR recording
agent-browser network har stop ./capture.har   # Stop and save HAR file

# Viewport & Device Emulation
agent-browser set viewport 1920 1080          # Set viewport size (default: 1280x720)
agent-browser set viewport 1920 1080 2        # 2x retina (same CSS size, higher res screenshots)
agent-browser set device "iPhone 14"          # Emulate device (viewport + user agent)

# Capture
agent-browser screenshot              # Screenshot to temp dir
agent-browser screenshot --full       # Full page screenshot
agent-browser screenshot --annotate   # Annotated screenshot with numbered element labels
agent-browser screenshot --screenshot-dir ./shots  # Save to custom directory
agent-browser screenshot --screenshot-format jpeg --screenshot-quality 80
agent-browser pdf output.pdf          # Save as PDF

# Clipboard
agent-browser clipboard read                      # Read text from clipboard
agent-browser clipboard write "Hello, World!"     # Write text to clipboard
agent-browser clipboard copy                      # Copy current selection
agent-browser clipboard paste                     # Paste from clipboard

# Dialogs (alert, confirm, prompt)
agent-browser dialog accept              # Accept dialog
agent-browser dialog accept "my input"   # Accept prompt dialog with text
agent-browser dialog dismiss             # Dismiss/cancel dialog
agent-browser dialog status              # Check if a dialog is currently open

# Diff (compare page states)
agent-browser diff snapshot                          # Compare current vs last snapshot
agent-browser diff snapshot --baseline before.txt    # Compare current vs saved file
agent-browser diff screenshot --baseline before.png  # Visual pixel diff
agent-browser diff url <url1> <url2>                 # Compare two pages
agent-browser diff url <url1> <url2> --wait-until networkidle  # Custom wait strategy
agent-browser diff url <url1> <url2> --selector "#main"  # Scope to element
```

## 批量执行

把由字符串数组组成的 JSON 数组通过管道传给 `batch`，即可在一次调用中执行多条命令。多步工作流由此省去每条命令单独启动进程的开销。

```bash
echo '[
  ["open", "https://example.com"],
  ["snapshot", "-i"],
  ["click", "@e1"],
  ["screenshot", "result.png"]
]' | agent-browser batch --json

# Stop on first error
agent-browser batch --bail < commands.json
```

命令序列已知且不依赖中间输出时用 `batch`；步骤之间需要解析输出时（如先 snapshot 找到 ref 再交互），用独立命令或 `&&` 串联。

## 常见模式

### 表单提交

```bash
agent-browser open https://example.com/signup
agent-browser snapshot -i
agent-browser fill @e1 "Jane Doe"
agent-browser fill @e2 "jane@example.com"
agent-browser select @e3 "California"
agent-browser check @e4
agent-browser click @e5
agent-browser wait --load networkidle
```

### 使用认证保险库登录（推荐）

```bash
# Save credentials once (encrypted with AGENT_BROWSER_ENCRYPTION_KEY)
# Recommended: pipe password via stdin to avoid shell history exposure
echo "pass" | agent-browser auth save github --url https://github.com/login --username user --password-stdin

# Login using saved profile (LLM never sees password)
agent-browser auth login github

# List/show/delete profiles
agent-browser auth list
agent-browser auth show github
agent-browser auth delete github
```

`auth login` 在交互前会等待用户名/密码/提交按钮选择器出现，超时时间与默认操作超时一致。

### 基于状态持久化的登录

```bash
# Login once and save state
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "$USERNAME"
agent-browser fill @e2 "$PASSWORD"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Reuse in future sessions
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

### 会话持久化

```bash
# Auto-save/restore cookies and localStorage across browser restarts
agent-browser --session-name myapp open https://app.example.com/login
# ... login flow ...
agent-browser close  # State auto-saved to ~/.agent-browser/sessions/

# Next time, state is auto-loaded
agent-browser --session-name myapp open https://app.example.com/dashboard

# Encrypt state at rest
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
agent-browser --session-name secure open https://app.example.com

# Manage saved states
agent-browser state list
agent-browser state show myapp-default.json
agent-browser state clear myapp
agent-browser state clean --older-than 7
```

### 处理 iframe

iframe 内容会自动内联进快照。iframe 内元素的 ref 自带 frame 上下文，可以直接交互。

```bash
agent-browser open https://example.com/checkout
agent-browser snapshot -i
# @e1 [heading] "Checkout"
# @e2 [Iframe] "payment-frame"
#   @e3 [input] "Card number"
#   @e4 [input] "Expiry"
#   @e5 [button] "Pay"

# Interact directly — no frame switch needed
agent-browser fill @e3 "4111111111111111"
agent-browser fill @e4 "12/28"
agent-browser click @e5

# To scope a snapshot to one iframe:
agent-browser frame @e2
agent-browser snapshot -i         # Only iframe content
agent-browser frame main          # Return to main frame
```

### 数据提取

```bash
agent-browser open https://example.com/products
agent-browser snapshot -i
agent-browser get text @e5           # Get specific element text
agent-browser get text body > page.txt  # Get all page text

# JSON output for parsing
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

### 并行会话

```bash
agent-browser --session site1 open https://site-a.com
agent-browser --session site2 open https://site-b.com

agent-browser --session site1 snapshot -i
agent-browser --session site2 snapshot -i

agent-browser session list
```

### 连接已有的 Chrome

```bash
# Auto-discover running Chrome with remote debugging enabled
agent-browser --auto-connect open https://example.com
agent-browser --auto-connect snapshot

# Or with explicit CDP port
agent-browser --cdp 9222 snapshot
```

自动连接会通过 `DevToolsActivePort` 和常见调试端口（9222、9229）发现 Chrome；若基于 HTTP 的 CDP 发现失败，则回退为直接建立 WebSocket 连接。

### 配色方案（深色模式）

```bash
# Persistent dark mode via flag (applies to all pages and new tabs)
agent-browser --color-scheme dark open https://example.com

# Or via environment variable
AGENT_BROWSER_COLOR_SCHEME=dark agent-browser open https://example.com

# Or set during session (persists for subsequent commands)
agent-browser set media dark
```

### 视口与响应式测试

```bash
# Set a custom viewport size (default is 1280x720)
agent-browser set viewport 1920 1080
agent-browser screenshot desktop.png

# Test mobile-width layout
agent-browser set viewport 375 812
agent-browser screenshot mobile.png

# Retina/HiDPI: same CSS layout at 2x pixel density
# Screenshots stay at logical viewport size, but content renders at higher DPI
agent-browser set viewport 1920 1080 2
agent-browser screenshot retina.png

# Device emulation (sets viewport + user agent in one step)
agent-browser set device "iPhone 14"
agent-browser screenshot device.png
```

`scale` 参数（第 3 个参数）在不改变 CSS 布局的前提下设置 `window.devicePixelRatio`。测试 retina 渲染或需要更高分辨率截图时使用。

### 可视化浏览器（调试）

```bash
agent-browser --headed open https://example.com
agent-browser highlight @e1          # Highlight element
agent-browser inspect                # Open Chrome DevTools for the active page
agent-browser record start demo.webm # Record session
agent-browser profiler start         # Start Chrome DevTools profiling
agent-browser profiler stop trace.json # Stop and save profile (path optional)
```

也可以通过环境变量 `AGENT_BROWSER_HEADED=1` 启用有界面模式。浏览器扩展在有界面和无头模式下均可使用。

### 本地文件（PDF、HTML）

```bash
# Open local files with file:// URLs
agent-browser --allow-file-access open file:///path/to/document.pdf
agent-browser --allow-file-access open file:///path/to/page.html
agent-browser screenshot output.png
```

### iOS 模拟器（移动版 Safari）

```bash
# List available iOS simulators
agent-browser device list

# Launch Safari on a specific device
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com

# Same workflow as desktop - snapshot, interact, re-snapshot
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1          # Tap (alias for click)
agent-browser -p ios fill @e2 "text"
agent-browser -p ios swipe up         # Mobile-specific gesture

# Take screenshot
agent-browser -p ios screenshot mobile.png

# Close session (shuts down simulator)
agent-browser -p ios close
```

**环境要求：** macOS 且装有 Xcode，以及 Appium（`npm install -g appium && appium driver install xcuitest`）

**真机：** 预先配置好的 iOS 物理设备同样适用。使用 `--device "<UDID>"`，UDID 可通过 `xcrun xctrace list devices` 获取。

## 安全

所有安全特性均需主动开启。默认情况下，agent-browser 对导航、操作和输出不做任何限制。

### 内容边界（推荐 AI agent 启用）

启用 `--content-boundaries` 后，源自页面的输出会被标记包裹，帮助 LLM 区分工具输出与不可信的页面内容：

```bash
export AGENT_BROWSER_CONTENT_BOUNDARIES=1
agent-browser snapshot
# Output:
# --- AGENT_BROWSER_PAGE_CONTENT nonce=<hex> origin=https://example.com ---
# [accessibility tree]
# --- END_AGENT_BROWSER_PAGE_CONTENT nonce=<hex> ---
```

### 域名白名单

把导航限制在可信域名内。`*.example.com` 这类通配符也匹配裸域名 `example.com`。发往非白名单域名的子资源请求、WebSocket 与 EventSource 连接同样会被拦截。请把目标页面依赖的 CDN 域名一并加入：

```bash
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"
agent-browser open https://example.com        # OK
agent-browser open https://malicious.com       # Blocked
```

### 操作策略

用策略文件管控破坏性操作：

```bash
export AGENT_BROWSER_ACTION_POLICY=./policy.json
```

`policy.json` 示例：

```json
{ "default": "deny", "allow": ["navigate", "snapshot", "click", "scroll", "wait", "get"] }
```

认证保险库操作（`auth login` 等）不受操作策略约束，但域名白名单依然生效。

### 输出限制

防止大页面输出淹没上下文：

```bash
export AGENT_BROWSER_MAX_OUTPUT=50000
```

## Diff 对比（验证变更）

执行某个操作后，用 `diff snapshot` 验证效果是否符合预期。它会把当前无障碍树（accessibility tree）与会话中上一次的快照进行对比。

```bash
# Typical workflow: snapshot -> action -> diff
agent-browser snapshot -i          # Take baseline snapshot
agent-browser click @e2            # Perform action
agent-browser diff snapshot        # See what changed (auto-compares to last snapshot)
```

用于视觉回归测试或监控：

```bash
# Save a baseline screenshot, then compare later
agent-browser screenshot baseline.png
# ... time passes or changes are made ...
agent-browser diff screenshot --baseline baseline.png

# Compare staging vs production
agent-browser diff url https://staging.example.com https://prod.example.com --screenshot
```

`diff snapshot` 的输出用 `+` 表示新增、`-` 表示移除，与 git diff 类似。`diff screenshot` 会生成一张差异图，变化像素以红色高亮，并给出不一致像素百分比。

## 超时与慢速页面

默认超时为 25 秒，可通过环境变量 `AGENT_BROWSER_DEFAULT_TIMEOUT`（单位毫秒）覆盖。遇到较慢的网站或较大的页面时，应使用显式等待，而不是依赖默认超时：

```bash
# Wait for network activity to settle (best for slow pages)
agent-browser wait --load networkidle

# Wait for a specific element to appear
agent-browser wait "#content"
agent-browser wait @e1

# Wait for a specific URL pattern (useful after redirects)
agent-browser wait --url "**/dashboard"

# Wait for a JavaScript condition
agent-browser wait --fn "document.readyState === 'complete'"

# Wait a fixed duration (milliseconds) as a last resort
agent-browser wait 5000
```

对于始终偏慢的网站，在 `open` 之后使用 `wait --load networkidle`，确保页面完全加载后再快照。如果某个元素渲染较慢，直接用 `wait <selector>` 或 `wait @ref` 等待它。

## JavaScript 对话框（alert / confirm / prompt）

页面弹出 JavaScript 对话框（`alert()`、`confirm()` 或 `prompt()`）时，在对话框被处理之前，所有其他浏览器命令（snapshot、screenshot、click 等）都会被阻塞。如果命令开始莫名超时，先检查是否有待处理的对话框：

```bash
# Check if a dialog is blocking
agent-browser dialog status

# Accept the dialog (dismiss the alert / click OK)
agent-browser dialog accept

# Accept a prompt dialog with input text
agent-browser dialog accept "my input"

# Dismiss the dialog (click Cancel)
agent-browser dialog dismiss
```

存在待处理对话框时，所有命令响应都会附带 `warning` 字段，标明对话框类型与消息。在 `--json` 模式下，它表现为响应对象中的 `"warning"` 键。

## 会话管理与清理

并行运行多个 agent 或自动化任务时，务必使用命名会话以避免冲突：

```bash
# Each agent gets its own isolated session
agent-browser --session agent1 open site-a.com
agent-browser --session agent2 open site-b.com

# Check active sessions
agent-browser session list
```

任务结束后务必关闭浏览器会话，避免进程残留：

```bash
agent-browser close                    # Close default session
agent-browser --session agent1 close   # Close specific session
```

如果上一个会话没有正常关闭，守护进程可能仍在运行。开始新工作前，先用 `agent-browser close` 清理。

让守护进程在空闲一段时间后自动退出（适用于临时/CI 环境）：

```bash
AGENT_BROWSER_IDLE_TIMEOUT_MS=60000 agent-browser open example.com
```

## ref 生命周期（重要）

ref（`@e1`、`@e2` 等）在页面变化后即告失效。以下情况之后务必重新快照：

- 点击会触发导航的链接或按钮
- 提交表单
- 动态内容加载（下拉菜单、模态框）

```bash
agent-browser click @e5              # Navigates to new page
agent-browser snapshot -i            # MUST re-snapshot
agent-browser click @e1              # Use new refs
```

## 标注截图（视觉模式）

使用 `--annotate` 截图，会在交互元素上叠加编号标签，每个标签 `[N]` 对应 ref `@eN`。截图同时会缓存 ref，因此无需单独快照即可立即交互。

```bash
agent-browser screenshot --annotate
# Output includes the image path and a legend:
#   [1] @e1 button "Submit"
#   [2] @e2 link "Home"
#   [3] @e3 textbox "Email"
agent-browser click @e2              # Click using ref from annotated screenshot
```

以下情况适合使用标注截图：

- 页面上有未标注的图标按钮或纯视觉元素
- 需要核对视觉布局或样式
- 存在 Canvas 或图表元素（文本快照看不见它们）
- 需要对元素位置做空间推理

## 语义定位器（ref 的替代方案）

当 ref 不可用或不可靠时，改用语义定位器：

```bash
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find role button click --name "Submit"
agent-browser find placeholder "Search" type "query"
agent-browser find testid "submit-btn" click
```

## JavaScript 求值（eval）

用 `eval` 在浏览器上下文中执行 JavaScript。**shell 引号处理可能破坏复杂表达式**——请改用 `--stdin` 或 `-b` 规避。

```bash
# Simple expressions work with regular quoting
agent-browser eval 'document.title'
agent-browser eval 'document.querySelectorAll("img").length'

# Complex JS: use --stdin with heredoc (RECOMMENDED)
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify(
  Array.from(document.querySelectorAll("img"))
    .filter(i => !i.alt)
    .map(i => ({ src: i.src.split("/").pop(), width: i.width }))
)
EVALEOF

# Alternative: base64 encoding (avoids all shell escaping issues)
agent-browser eval -b "$(echo -n 'Array.from(document.querySelectorAll("a")).map(a => a.href)' | base64)"
```

**为什么要注意：** shell 处理命令时，内层双引号、`!`（历史展开）、反引号和 `$()` 都可能在 JavaScript 到达 agent-browser 之前将其破坏。`--stdin` 和 `-b` 两个选项可完全绕开 shell 解释。

**经验法则：**

- 单行且无嵌套引号 -> 用单引号包裹的常规 `eval 'expression'` 即可
- 出现嵌套引号、箭头函数、模板字符串或多行 -> 使用 `eval --stdin <<'EVALEOF'`
- 程序化/生成的脚本 -> 使用 `eval -b` 加 base64

## 配置文件

在项目根目录创建 `agent-browser.json` 作为持久化配置：

```json
{
  "headed": true,
  "proxy": "http://localhost:8080",
  "profile": "./browser-data"
}
```

优先级从低到高：`~/.agent-browser/config.json` < `./agent-browser.json` < 环境变量 < CLI 选项。可用 `--config <path>` 或环境变量 `AGENT_BROWSER_CONFIG` 指定自定义配置文件（文件缺失或非法时直接报错退出）。所有 CLI 选项都映射为 camelCase 键（如 `--executable-path` -> `"executablePath"`）。布尔开关接受 `true`/`false`（如 `--headed false` 可覆盖配置）。用户配置与项目配置中的扩展会合并而非相互替换。

## 深入文档

| 参考文档 | 适用场景 |
| --- | --- |
| [references/commands.md](references/commands.md) | 全部命令与选项的完整参考 |
| [references/snapshot-refs.md](references/snapshot-refs.md) | ref 生命周期、失效规则与问题排查 |
| [references/session-management.md](references/session-management.md) | 并行会话、状态持久化与并发抓取 |
| [references/authentication.md](references/authentication.md) | 登录流程、OAuth、2FA 处理与状态复用 |
| [references/video-recording.md](references/video-recording.md) | 用于调试和文档的录制工作流 |
| [references/profiling.md](references/profiling.md) | 用 Chrome DevTools 剖析做性能分析 |
| [references/proxy-support.md](references/proxy-support.md) | 代理配置、地域测试与轮换代理 |

## 浏览器引擎选择

用 `--engine` 选择本地浏览器引擎，默认为 `chrome`。

```bash
# Use Lightpanda (fast headless browser, requires separate install)
agent-browser --engine lightpanda open example.com

# Via environment variable
export AGENT_BROWSER_ENGINE=lightpanda
agent-browser open example.com

# With custom binary path
agent-browser --engine lightpanda --executable-path /path/to/lightpanda open example.com
```

支持的引擎：
- `chrome`（默认）—— 经 CDP 驱动 Chrome/Chromium
- `lightpanda` —— 经 CDP 驱动的 Lightpanda 无头浏览器（比 Chrome 快 10 倍、内存占用低 10 倍）

Lightpanda 不支持 `--extension`、`--profile`、`--state` 和 `--allow-file-access`。安装方法见 https://lightpanda.io/docs/open-source/installation。

## 开箱即用的模板

| 模板 | 说明 |
| --- | --- |
| [templates/form-automation.sh](templates/form-automation.sh) | 带校验的表单填写 |
| [templates/authenticated-session.sh](templates/authenticated-session.sh) | 登录一次，复用状态 |
| [templates/capture-workflow.sh](templates/capture-workflow.sh) | 截图并提取内容 |

```bash
./templates/form-automation.sh https://example.com/form
./templates/authenticated-session.sh https://app.example.com/login
./templates/capture-workflow.sh https://example.com ./output
```
