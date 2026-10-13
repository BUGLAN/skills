# 会话管理

多个相互隔离的浏览器会话，支持状态持久化与并发浏览。

**相关文档**：[authentication.md](authentication.md)（登录模式）、[SKILL.md](../SKILL.md)（快速上手）。

## 目录

- [命名会话](#named-sessions)
- [会话隔离特性](#session-isolation-properties)
- [会话状态持久化](#session-state-persistence)
- [常见模式](#common-patterns)
- [默认会话](#default-session)
- [会话清理](#session-cleanup)
- [最佳实践](#best-practices)

## 命名会话

用 `--session` 选项隔离浏览器上下文：

```bash
# Session 1: Authentication flow
agent-browser --session auth open https://app.example.com/login

# Session 2: Public browsing (separate cookies, storage)
agent-browser --session public open https://example.com

# Commands are isolated by session
agent-browser --session auth fill @e1 "user@example.com"
agent-browser --session public get text body
```

## 会话隔离特性

每个会话都独立拥有：
- Cookies
- LocalStorage / SessionStorage
- IndexedDB
- 缓存
- 浏览历史
- 打开的标签页

## 会话状态持久化

### 保存会话状态

```bash
# Save cookies, storage, and auth state
agent-browser state save /path/to/auth-state.json
```

### 加载会话状态

```bash
# Restore saved state
agent-browser state load /path/to/auth-state.json

# Continue with authenticated session
agent-browser open https://app.example.com/dashboard
```

### 状态文件内容

```json
{
  "cookies": [...],
  "localStorage": {...},
  "sessionStorage": {...},
  "origins": [...]
}
```

## 常见模式

### 复用已登录会话

```bash
#!/bin/bash
# Save login state once, reuse many times

STATE_FILE="/tmp/auth-state.json"

# Check if we have saved state
if [[ -f "$STATE_FILE" ]]; then
    agent-browser state load "$STATE_FILE"
    agent-browser open https://app.example.com/dashboard
else
    # Perform login
    agent-browser open https://app.example.com/login
    agent-browser snapshot -i
    agent-browser fill @e1 "$USERNAME"
    agent-browser fill @e2 "$PASSWORD"
    agent-browser click @e3
    agent-browser wait --load networkidle

    # Save for future use
    agent-browser state save "$STATE_FILE"
fi
```

### 并发抓取

```bash
#!/bin/bash
# Scrape multiple sites concurrently

# Start all sessions
agent-browser --session site1 open https://site1.com &
agent-browser --session site2 open https://site2.com &
agent-browser --session site3 open https://site3.com &
wait

# Extract from each
agent-browser --session site1 get text body > site1.txt
agent-browser --session site2 get text body > site2.txt
agent-browser --session site3 get text body > site3.txt

# Cleanup
agent-browser --session site1 close
agent-browser --session site2 close
agent-browser --session site3 close
```

### A/B 测试会话

```bash
# Test different user experiences
agent-browser --session variant-a open "https://app.com?variant=a"
agent-browser --session variant-b open "https://app.com?variant=b"

# Compare
agent-browser --session variant-a screenshot /tmp/variant-a.png
agent-browser --session variant-b screenshot /tmp/variant-b.png
```

## 默认会话

省略 `--session` 时，命令使用默认会话：

```bash
# These use the same default session
agent-browser open https://example.com
agent-browser snapshot -i
agent-browser close  # Closes default session
```

## 会话清理

```bash
# Close specific session
agent-browser --session auth close

# List active sessions
agent-browser session list
```

## 最佳实践

### 1. 会话命名要有语义

```bash
# GOOD: Clear purpose
agent-browser --session github-auth open https://github.com
agent-browser --session docs-scrape open https://docs.example.com

# AVOID: Generic names
agent-browser --session s1 open https://github.com
```

### 2. 用完即清理

```bash
# Close sessions when done
agent-browser --session auth close
agent-browser --session scrape close
```

### 3. 安全处理状态文件

```bash
# Don't commit state files (contain auth tokens!)
echo "*.auth-state.json" >> .gitignore

# Delete after use
rm /tmp/auth-state.json
```

### 4. 为长会话设置超时

```bash
# Set timeout for automated scripts
timeout 60 agent-browser --session long-task get text body
```
