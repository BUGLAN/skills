---
name: full-output-enforcement
description: 覆盖 LLM 默认的截断行为：强制完整生成代码、禁止占位符模式，并妥善处理触及 token 上限时的分段输出。适用于任何要求输出详尽完整、不做删节的任务。
---

# 强制完整输出（Full-Output Enforcement）

## 基线

把每个任务都当作生产级任务来对待。不完整的输出就是损坏的输出。不要为简短而优化——要为完整而优化。用户要完整文件，就交付完整文件；用户要 5 个组件，就交付 5 个组件。绝无例外。

## 禁止的输出模式

以下模式一律视为硬性失败，绝不产出：

**代码块中：**`// ...`、`// rest of code`、`// implement here`、`// TODO`、`/* ... */`、`// similar to above`、`// continue pattern`、`// add more as needed`，以及用单独一个 `...` 顶替被省略的代码

**行文中：**"Let me know if you want me to continue"、"I can provide more details if needed"、"for brevity"、"the rest follows the same pattern"、"similarly for the remaining"、"and so on"（用来顶替实际内容时）、"I'll leave that as an exercise"

**结构性偷工减料：**要的是完整实现，却只给出骨架；只展示开头与结尾，跳过中间；用一个示例加一段说明，代替本应逐处展开的重复逻辑；描述代码“应该做什么”，而不是真正把代码写出来。

## 执行流程

1. **圈定范围** —— 通读完整请求，数清预期中有多少个独立交付物（文件、函数、章节、答案），锁定这个数字。
2. **完整构建** —— 把每个交付物都完整生成。不交半成品草稿，不说 “you can extend this later”。
3. **交叉核对** —— 输出之前重读原始请求，把交付物数量与范围数量对照。缺了任何一项，先补齐再回复。

## 处理超长输出

当回复接近 token 上限时：

- 不要为了塞进剩余内容而压缩后续章节。
- 不要跳过中间直接奔向结论。
- 以完整质量写到下一个干净的断点（函数结尾、文件结尾、章节结尾）。
- 然后以下面这行收尾：

```
[PAUSED — X of Y complete. Send "continue" to resume from: next section name]
```

收到 "continue" 后，从停下的地方精确接续。不回顾前文，不作重复。

## 快速自查

在最终敲定任何回复之前，逐项核对：

- 输出中没有出现上述任何禁止模式
- 用户要求的每一项都已存在且已完成
- 代码块里是真正可运行的代码，而不是对代码“应该做什么”的描述
- 没有任何内容为节省篇幅而被删减
