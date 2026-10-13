# 认证模式

登录流程、会话持久化、OAuth、双因素认证（2FA）与带登录态的浏览。

**相关文档**：[session-management.md](session-management.md)（状态持久化详情）、[SKILL.md](../SKILL.md)（快速上手）。

## 目录

- [从你的浏览器导入登录态](#import-auth-from-your-browser)
- [持久化 profile](#persistent-profiles)
- [会话持久化](#session-persistence)
- [基础登录流程](#basic-login-flow)
- [保存登录态](#saving-authentication-state)
- [恢复登录态](#restoring-authentication)
- [OAuth / SSO 流程](#oauth--sso-flows)
- [双因素认证（2FA）](#two-factor-authentication)
- [HTTP Basic 认证](#http-basic-auth)
- [基于 cookie 的认证](#cookie-based-auth)
- [Token 刷新处理](#token-refresh-handling)
- [安全最佳实践](#security-best-practices)

## 从你的浏览器导入登录态

最快的认证方式，是复用你已登录的 Chrome 会话中的 cookie。

**第 1 步：以远程调试模式启动 Chrome**

```bash
# macOS
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222

# Linux
google-chrome --remote-debugging-port=9222

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

像平常一样，在这个 Chrome 窗口中登录目标网站。

> **安全提示**：`--remote-debugging-port` 会在 localhost 上暴露完整的浏览器控制权，任何本地进程都能连接并读取 cookie、执行 JS 等。只在自己的可信机器上使用，用完关闭 Chrome。

**第 2 步：抓取登录态**

```bash
# Auto-discover the running Chrome and save its cookies + localStorage
agent-browser --auto-connect state save ./my-auth.json
```

**第 3 步：在自动化中复用**

```bash
# Load auth at launch
agent-browser --state ./my-auth.json open https://app.example.com/dashboard

# Or load into an existing session
agent-browser state load ./my-auth.json
agent-browser open https://app.example.com/dashboard
```

这适用于任何网站，包括 OAuth 流程复杂、有 SSO 或 2FA 的站点——只要 Chrome 里已有有效的会话 cookie。

> **安全提示**：状态文件以明文保存会话 token。请将它们加入 `.gitignore`，不再需要时删除，并设置 `AGENT_BROWSER_ENCRYPTION_KEY` 启用静态加密。参见[安全最佳实践](#security-best-practices)。

**提示**：配合 `--session-name` 使用，导入的登录态会在重启后自动持久化：

```bash
agent-browser --session-name myapp state load ./my-auth.json
# From now on, state is auto-saved/restored for "myapp"
```

## 持久化 profile

用 `--profile` 让 agent-browser 指向一个 Chrome 用户数据目录。cookies、IndexedDB、service worker、缓存等所有内容都会跨浏览器重启持久保留，无需显式 save/load：

```bash
# First run: login once
agent-browser --profile ~/.myapp-profile open https://app.example.com/login
# ... complete login flow ...

# All subsequent runs: already authenticated
agent-browser --profile ~/.myapp-profile open https://app.example.com/dashboard
```

不同项目或测试用户使用不同路径：

```bash
agent-browser --profile ~/.profiles/admin open https://app.example.com
agent-browser --profile ~/.profiles/viewer open https://app.example.com
```

也可以通过环境变量设置：

```bash
export AGENT_BROWSER_PROFILE=~/.myapp-profile
agent-browser open https://app.example.com/dashboard
```

## 会话持久化

用 `--session-name` 按名称自动保存和恢复 cookies 与 localStorage，无需手动管理文件：

```bash
# Auto-saves state on close, auto-restores on next launch
agent-browser --session-name twitter open https://twitter.com
# ... login flow ...
agent-browser close  # state saved to ~/.agent-browser/sessions/

# Next time: state is automatically restored
agent-browser --session-name twitter open https://twitter.com
```

对状态做静态加密：

```bash
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
agent-browser --session-name secure open https://app.example.com
```

## 基础登录流程

```bash
# Navigate to login page
agent-browser open https://app.example.com/login
agent-browser wait --load networkidle

# Get form elements
agent-browser snapshot -i
# Output: @e1 [input type="email"], @e2 [input type="password"], @e3 [button] "Sign In"

# Fill credentials
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"

# Submit
agent-browser click @e3
agent-browser wait --load networkidle

# Verify login succeeded
agent-browser get url  # Should be dashboard, not login
```

## 保存登录态

登录完成后，保存状态以备复用：

```bash
# Login first (see above)
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --url "**/dashboard"

# Save authenticated state
agent-browser state save ./auth-state.json
```

## 恢复登录态

加载已保存的状态，跳过登录：

```bash
# Load saved auth state
agent-browser state load ./auth-state.json

# Navigate directly to protected page
agent-browser open https://app.example.com/dashboard

# Verify authenticated
agent-browser snapshot -i
```

## OAuth / SSO 流程

针对 OAuth 重定向：

```bash
# Start OAuth flow
agent-browser open https://app.example.com/auth/google

# Handle redirects automatically
agent-browser wait --url "**/accounts.google.com**"
agent-browser snapshot -i

# Fill Google credentials
agent-browser fill @e1 "user@gmail.com"
agent-browser click @e2  # Next button
agent-browser wait 2000
agent-browser snapshot -i
agent-browser fill @e3 "password"
agent-browser click @e4  # Sign in

# Wait for redirect back
agent-browser wait --url "**/app.example.com**"
agent-browser state save ./oauth-state.json
```

## 双因素认证（2FA）

2FA 通过人工介入处理：

```bash
# Login with credentials
agent-browser open https://app.example.com/login --headed  # Show browser
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3

# Wait for user to complete 2FA manually
echo "Complete 2FA in the browser window..."
agent-browser wait --url "**/dashboard" --timeout 120000

# Save state after 2FA
agent-browser state save ./2fa-state.json
```

## HTTP Basic 认证

适用于使用 HTTP Basic 认证的网站：

```bash
# Set credentials before navigation
agent-browser set credentials username password

# Navigate to protected resource
agent-browser open https://protected.example.com/api
```

## 基于 cookie 的认证

手动设置认证 cookie：

```bash
# Set auth cookie
agent-browser cookies set session_token "abc123xyz"

# Navigate to protected page
agent-browser open https://app.example.com/dashboard
```

## Token 刷新处理

适用于 token 会过期的会话：

```bash
#!/bin/bash
# Wrapper that handles token refresh

STATE_FILE="./auth-state.json"

# Try loading existing state
if [[ -f "$STATE_FILE" ]]; then
    agent-browser state load "$STATE_FILE"
    agent-browser open https://app.example.com/dashboard

    # Check if session is still valid
    URL=$(agent-browser get url)
    if [[ "$URL" == *"/login"* ]]; then
        echo "Session expired, re-authenticating..."
        # Perform fresh login
        agent-browser snapshot -i
        agent-browser fill @e1 "$USERNAME"
        agent-browser fill @e2 "$PASSWORD"
        agent-browser click @e3
        agent-browser wait --url "**/dashboard"
        agent-browser state save "$STATE_FILE"
    fi
else
    # First-time login
    agent-browser open https://app.example.com/login
    # ... login flow ...
fi
```

## 安全最佳实践

1. **绝不提交状态文件**——其中含有会话 token
   ```bash
   echo "*.auth-state.json" >> .gitignore
   ```

2. **凭据使用环境变量**
   ```bash
   agent-browser fill @e1 "$APP_USERNAME"
   agent-browser fill @e2 "$APP_PASSWORD"
   ```

3. **自动化结束后做好清理**
   ```bash
   agent-browser cookies clear
   rm -f ./auth-state.json
   ```

4. **CI/CD 使用短生命周期会话**
   ```bash
   # Don't persist state in CI
   agent-browser open https://app.example.com/login
   # ... login and perform actions ...
   agent-browser close  # Session ends, nothing persisted
   ```
