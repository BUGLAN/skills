# 性能剖析

在浏览器自动化过程中采集 Chrome DevTools 性能档案（performance profile），用于性能分析。

**相关文档**：[commands.md](commands.md)（完整命令参考）、[SKILL.md](../SKILL.md)（快速上手）。

## 目录

- [基础剖析](#basic-profiling)
- [Profiler 命令](#profiler-commands)
- [类别](#categories)
- [使用场景](#use-cases)
- [输出格式](#output-format)
- [查看性能档案](#viewing-profiles)
- [限制](#limitations)

## 基础剖析

```bash
# Start profiling
agent-browser profiler start

# Perform actions
agent-browser navigate https://example.com
agent-browser click "#button"
agent-browser wait 1000

# Stop and save
agent-browser profiler stop ./trace.json
```

## Profiler 命令

```bash
# Start profiling with default categories
agent-browser profiler start

# Start with custom trace categories
agent-browser profiler start --categories "devtools.timeline,v8.execute,blink.user_timing"

# Stop profiling and save to file
agent-browser profiler stop ./trace.json
```

## 类别

`--categories` 选项接受以逗号分隔的 Chrome trace 类别列表。默认类别包括：

- `devtools.timeline` —— 标准 DevTools 性能跟踪
- `v8.execute` —— 执行 JavaScript 的耗时
- `blink` —— 渲染器事件
- `blink.user_timing` —— `performance.mark()` / `performance.measure()` 调用
- `latencyInfo` —— 从输入到呈现的延迟追踪
- `renderer.scheduler` —— 任务调度与执行
- `toplevel` —— 覆盖面广的基础事件

另含若干 `disabled-by-default-*` 类别，用于提供详细的时间线、调用栈和 V8 CPU 剖析数据。

## 使用场景

### 诊断页面加载缓慢

```bash
agent-browser profiler start
agent-browser navigate https://app.example.com
agent-browser wait --load networkidle
agent-browser profiler stop ./page-load-profile.json
```

### 剖析用户交互

```bash
agent-browser navigate https://app.example.com
agent-browser profiler start
agent-browser click "#submit"
agent-browser wait 2000
agent-browser profiler stop ./interaction-profile.json
```

### CI 性能回归检查

```bash
#!/bin/bash
agent-browser profiler start
agent-browser navigate https://app.example.com
agent-browser wait --load networkidle
agent-browser profiler stop "./profiles/build-${BUILD_ID}.json"
```

## 输出格式

输出为 Chrome Trace Event 格式的 JSON 文件：

```json
{
  "traceEvents": [
    { "cat": "devtools.timeline", "name": "RunTask", "ph": "X", "ts": 12345, "dur": 100, ... },
    ...
  ],
  "metadata": {
    "clock-domain": "LINUX_CLOCK_MONOTONIC"
  }
}
```

`metadata.clock-domain` 字段依宿主平台（Linux 或 macOS）设置；Windows 上省略该字段。

## 查看性能档案

用以下任一工具加载输出的 JSON 文件：

- **Chrome DevTools**：Performance 面板 > Load profile（Ctrl+Shift+I > Performance）
- **Perfetto UI**：https://ui.perfetto.dev/ —— 拖入 JSON 文件即可
- **Trace Viewer**：在任意 Chromium 浏览器中打开 `chrome://tracing`

## 限制

- 仅支持 Chromium 内核浏览器（Chrome、Edge），不支持 Firefox 或 WebKit。
- 剖析进行期间，trace 数据会持续累积在内存中（上限 500 万条事件）。采集完关注点后请尽快停止剖析。
- 停止时收集数据有 30 秒超时；若浏览器无响应，stop 命令可能失败。
