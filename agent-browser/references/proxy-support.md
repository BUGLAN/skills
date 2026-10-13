# 代理支持

代理配置：用于地域测试、规避限流和企业网络环境。

**相关文档**：[commands.md](commands.md)（全局选项）、[SKILL.md](../SKILL.md)（快速上手）。

## 目录

- [基础代理配置](#basic-proxy-configuration)
- [带认证的代理](#authenticated-proxy)
- [SOCKS 代理](#socks-proxy)
- [代理绕过](#proxy-bypass)
- [常见场景](#common-use-cases)
- [验证代理连接](#verifying-proxy-connection)
- [故障排查](#troubleshooting)
- [最佳实践](#best-practices)

## 基础代理配置

使用 `--proxy` 选项，或通过环境变量设置代理：

```bash
# Via CLI flag
agent-browser --proxy "http://proxy.example.com:8080" open https://example.com

# Via environment variable
export HTTP_PROXY="http://proxy.example.com:8080"
agent-browser open https://example.com

# HTTPS proxy
export HTTPS_PROXY="https://proxy.example.com:8080"
agent-browser open https://example.com

# Both
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
agent-browser open https://example.com
```

## 带认证的代理

代理需要认证时：

```bash
# Include credentials in URL
export HTTP_PROXY="http://username:password@proxy.example.com:8080"
agent-browser open https://example.com
```

## SOCKS 代理

```bash
# SOCKS5 proxy
export ALL_PROXY="socks5://proxy.example.com:1080"
agent-browser open https://example.com

# SOCKS5 with auth
export ALL_PROXY="socks5://user:pass@proxy.example.com:1080"
agent-browser open https://example.com
```

## 代理绕过

用 `--proxy-bypass` 或 `NO_PROXY` 让特定域名绕过代理：

```bash
# Via CLI flag
agent-browser --proxy "http://proxy.example.com:8080" --proxy-bypass "localhost,*.internal.com" open https://example.com

# Via environment variable
export NO_PROXY="localhost,127.0.0.1,.internal.company.com"
agent-browser open https://internal.company.com  # Direct connection
agent-browser open https://external.com          # Via proxy
```

## 常见场景

### 地域测试

```bash
#!/bin/bash
# Test site from different regions using geo-located proxies

PROXIES=(
    "http://us-proxy.example.com:8080"
    "http://eu-proxy.example.com:8080"
    "http://asia-proxy.example.com:8080"
)

for proxy in "${PROXIES[@]}"; do
    export HTTP_PROXY="$proxy"
    export HTTPS_PROXY="$proxy"

    region=$(echo "$proxy" | grep -oP '^\w+-\w+')
    echo "Testing from: $region"

    agent-browser --session "$region" open https://example.com
    agent-browser --session "$region" screenshot "./screenshots/$region.png"
    agent-browser --session "$region" close
done
```

### 抓取时轮换代理

```bash
#!/bin/bash
# Rotate through proxy list to avoid rate limiting

PROXY_LIST=(
    "http://proxy1.example.com:8080"
    "http://proxy2.example.com:8080"
    "http://proxy3.example.com:8080"
)

URLS=(
    "https://site.com/page1"
    "https://site.com/page2"
    "https://site.com/page3"
)

for i in "${!URLS[@]}"; do
    proxy_index=$((i % ${#PROXY_LIST[@]}))
    export HTTP_PROXY="${PROXY_LIST[$proxy_index]}"
    export HTTPS_PROXY="${PROXY_LIST[$proxy_index]}"

    agent-browser open "${URLS[$i]}"
    agent-browser get text body > "output-$i.txt"
    agent-browser close

    sleep 1  # Polite delay
done
```

### 企业网络访问

```bash
#!/bin/bash
# Access internal sites via corporate proxy

export HTTP_PROXY="http://corpproxy.company.com:8080"
export HTTPS_PROXY="http://corpproxy.company.com:8080"
export NO_PROXY="localhost,127.0.0.1,.company.com"

# External sites go through proxy
agent-browser open https://external-vendor.com

# Internal sites bypass proxy
agent-browser open https://intranet.company.com
```

## 验证代理连接

```bash
# Check your apparent IP
agent-browser open https://httpbin.org/ip
agent-browser get text body
# Should show proxy's IP, not your real IP
```

## 故障排查

### 代理连接失败

```bash
# Test proxy connectivity first
curl -x http://proxy.example.com:8080 https://httpbin.org/ip

# Check if proxy requires auth
export HTTP_PROXY="http://user:pass@proxy.example.com:8080"
```

### 经过代理时的 SSL/TLS 错误

有些代理会做 SSL 检查。遇到证书错误时：

```bash
# For testing only - not recommended for production
agent-browser open https://example.com --ignore-https-errors
```

### 性能缓慢

```bash
# Use proxy only when necessary
export NO_PROXY="*.cdn.com,*.static.com"  # Direct CDN access
```

## 最佳实践

1. **使用环境变量**——不要硬编码代理凭据
2. **合理设置 NO_PROXY**——本地流量不要走代理
3. **自动化前先测试代理**——用简单请求验证连通性
4. **妥善处理代理故障**——对不稳定的代理实现重试逻辑
5. **大规模抓取时轮换代理**——分摊负载并避免封禁
