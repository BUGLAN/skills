# 快照与 Ref

紧凑的元素引用（ref），大幅降低 AI agent 的上下文消耗。

**相关文档**：[commands.md](commands.md)（完整命令参考）、[SKILL.md](../SKILL.md)（快速上手）。

## 目录

- [ref 的工作原理](#how-refs-work)
- [Snapshot 命令](#the-snapshot-command)
- [使用 ref](#using-refs)
- [ref 生命周期](#ref-lifecycle)
- [最佳实践](#best-practices)
- [ref 记法详解](#ref-notation-details)
- [问题排查](#troubleshooting)

## ref 的工作原理

传统方式：
```
Full DOM/HTML → AI parses → CSS selector → Action (~3000-5000 tokens)
```

agent-browser 方式：
```
Compact snapshot → @refs assigned → Direct interaction (~200-400 tokens)
```

## Snapshot 命令

```bash
# Basic snapshot (shows page structure)
agent-browser snapshot

# Interactive snapshot (-i flag) - RECOMMENDED
agent-browser snapshot -i
```

### Snapshot 输出格式

```
Page: Example Site - Home
URL: https://example.com

@e1 [header]
  @e2 [nav]
    @e3 [a] "Home"
    @e4 [a] "Products"
    @e5 [a] "About"
  @e6 [button] "Sign In"

@e7 [main]
  @e8 [h1] "Welcome"
  @e9 [form]
    @e10 [input type="email"] placeholder="Email"
    @e11 [input type="password"] placeholder="Password"
    @e12 [button type="submit"] "Log In"

@e13 [footer]
  @e14 [a] "Privacy Policy"
```

## 使用 ref

拿到 ref 后即可直接交互：

```bash
# Click the "Sign In" button
agent-browser click @e6

# Fill email input
agent-browser fill @e10 "user@example.com"

# Fill password
agent-browser fill @e11 "password123"

# Submit the form
agent-browser click @e12
```

## ref 生命周期

**重要**：页面一旦变化，ref 即告失效！

```bash
# Get initial snapshot
agent-browser snapshot -i
# @e1 [button] "Next"

# Click triggers page change
agent-browser click @e1

# MUST re-snapshot to get new refs!
agent-browser snapshot -i
# @e1 [h1] "Page 2"  ← Different element now!
```

## 最佳实践

### 1. 交互前务必先快照

```bash
# CORRECT
agent-browser open https://example.com
agent-browser snapshot -i          # Get refs first
agent-browser click @e1            # Use ref

# WRONG
agent-browser open https://example.com
agent-browser click @e1            # Ref doesn't exist yet!
```

### 2. 导航后重新快照

```bash
agent-browser click @e5            # Navigates to new page
agent-browser snapshot -i          # Get new refs
agent-browser click @e1            # Use new refs
```

### 3. 动态变化后重新快照

```bash
agent-browser click @e1            # Opens dropdown
agent-browser snapshot -i          # See dropdown items
agent-browser click @e7            # Select item
```

### 4. 只快照特定区域

页面复杂时，可以只快照局部：

```bash
# Snapshot just the form
agent-browser snapshot @e9
```

## ref 记法详解

```
@e1 [tag type="value"] "text content" placeholder="hint"
│    │   │             │               │
│    │   │             │               └─ Additional attributes
│    │   │             └─ Visible text
│    │   └─ Key attributes shown
│    └─ HTML tag name
└─ Unique ref ID
```

### 常见模式

```
@e1 [button] "Submit"                    # Button with text
@e2 [input type="email"]                 # Email input
@e3 [input type="password"]              # Password input
@e4 [a href="/page"] "Link Text"         # Anchor link
@e5 [select]                             # Dropdown
@e6 [textarea] placeholder="Message"     # Text area
@e7 [div class="modal"]                  # Container (when relevant)
@e8 [img alt="Logo"]                     # Image
@e9 [checkbox] checked                   # Checked checkbox
@e10 [radio] selected                    # Selected radio
```

## iframe

快照会自动检测并内联 iframe 内容。主 frame 快照运行时，每个 `Iframe` 节点都会被解析，其子无障碍树直接内联在输出中该节点下方。分配给 iframe 内元素的 ref 自带 frame 上下文，因此 `click`、`fill`、`type` 等交互无需手动切换 frame。

```bash
agent-browser snapshot -i
# @e1 [heading] "Checkout"
# @e2 [Iframe] "payment-frame"
#   @e3 [input] "Card number"
#   @e4 [input] "Expiry"
#   @e5 [button] "Pay"
# @e6 [button] "Cancel"

# Interact with iframe elements directly using their refs
agent-browser fill @e3 "4111111111111111"
agent-browser fill @e4 "12/28"
agent-browser click @e5
```

**要点**：
- 只展开一层 iframe 嵌套（iframe 中的 iframe 不再递归展开）
- 阻止无障碍树访问的跨域 iframe 会被静默跳过
- 空 iframe 或没有可交互内容的 iframe 不会出现在输出中
- 要把快照限定在单个 iframe，先 `frame @ref` 再 `snapshot -i`

## 问题排查

### 「Ref not found」错误

```bash
# Ref may have changed - re-snapshot
agent-browser snapshot -i
```

### 元素在快照中不可见

```bash
# Scroll down to reveal element
agent-browser scroll down 1000
agent-browser snapshot -i

# Or wait for dynamic content
agent-browser wait 1000
agent-browser snapshot -i
```

### 元素过多

```bash
# Snapshot specific container
agent-browser snapshot @e5

# Or use get text for content-only extraction
agent-browser get text @e5
```
