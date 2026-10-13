---
name: design-an-interface
description: 用并行子代理为一个模块生成多个截然不同的接口设计。适用于用户要设计 API、探索接口方案、比较模块形态，或提到 "design it twice"（同一设计做两遍）时。
---

# 设计模块接口

源自《A Philosophy of Software Design》（软件设计哲学）中的 "Design It Twice"（同一设计做两遍）：你的第一个想法多半不是最好的。生成多个截然不同的设计，再加以比较。

## 工作流

### 1. 收集需求

设计之前，先弄清楚：

- [ ] 这个模块解决什么问题？
- [ ] 调用方是谁？（其他模块、外部用户、测试）
- [ ] 关键操作有哪些？
- [ ] 有哪些约束？（性能、兼容性、既有模式）
- [ ] 哪些应藏在内部，哪些应对外暴露？

开口问："这个模块需要做什么？谁来用它？"

### 2. 生成设计（并行子代理）

用 Task 工具同时派出 3 个以上子代理。每个子代理必须产出**截然不同**的方案。

```
Prompt template for each sub-agent:

Design an interface for: [module description]

Requirements: [gathered requirements]

Constraints for this design: [assign a different constraint to each agent]
- Agent 1: "Minimize method count - aim for 1-3 methods max"
- Agent 2: "Maximize flexibility - support many use cases"
- Agent 3: "Optimize for the most common case"
- Agent 4: "Take inspiration from [specific paradigm/library]"

Output format:
1. Interface signature (types/methods)
2. Usage example (how caller uses it)
3. What this design hides internally
4. Trade-offs of this approach
```

### 3. 展示设计

展示每个设计时，给出：

1. **接口签名** —— 类型、方法、参数
2. **用法示例** —— 调用方在实践中的真实用法
3. **隐藏了什么** —— 留在内部的复杂度

按顺序逐个展示，让用户在比较之前先消化每一种方案。

### 4. 比较设计

全部展示完后，从以下维度比较：

- **接口简单度**：方法更少、参数更简单
- **通用 vs 专用**：灵活性 vs 聚焦
- **实现效率**：接口形态是否容得下高效的内部实现？
- **深度**：小接口藏住大复杂度（好）vs 大接口配薄实现（坏）
- **正确使用的容易度** vs **误用的容易度**

用行文讨论取舍，不要列表格。突出各方案分歧最大之处。

### 5. 综合

最好的设计往往融合了多个方案的洞见。可以问：

- "哪个设计最贴合你的主要用例？"
- "其他设计里有没有值得吸收的元素？"

## 评估标准

出自《A Philosophy of Software Design》：

**接口简单度**：方法更少、参数更简单 = 更容易学会，也更容易正确使用。

**通用性**：无需改动即可应对未来的用例。但要警惕过度泛化。

**实现效率**：接口形态能否支撑高效的实现？还是逼出别扭的内部结构？

**深度**：小接口藏住大复杂度 = 深模块（好）；大接口配薄实现 = 浅模块（避免）。

## 反模式

- 不要放任子代理产出雷同的设计——强制要求截然不同
- 不要跳过比较环节——价值正源于对比
- 不要动手实现——这里只关心接口形态
- 不要以实现工作量作为评判依据
