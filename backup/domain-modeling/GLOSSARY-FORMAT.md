# GLOSSARY.md 格式

## 结构

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

> 上面的模板保持英文原样，是刻意为之：生成的 `GLOSSARY.md` 沿用这套骨架（`## Language`、`_Avoid_`），这样与上游 skill 互通，也便于 grep 和机器读取。正文说明用中文。

## 规则

- **要有主见。** 同一个概念存在多个词时，挑出最好的那个，其余的列到 `_Avoid_` 下。
- **定义要短。** 最多一两句。定义它*是什么*，而不是它*做什么*。
- **只收本项目上下文特有的术语。** 通用编程概念（timeout、错误类型、工具类模式）不属于这里，哪怕项目里到处都在用。加一个术语之前先问自己：这是本上下文独有的概念，还是通用编程概念？只有前者才该收。
- **出现自然聚类时用子标题分组。** 如果所有术语同属一个内聚的领域，平铺列表就可以。

## 单上下文 vs 多上下文仓库

**单上下文（多数仓库）：** 仓库根目录一个 `GLOSSARY.md`。

**多上下文：** 仓库根目录的 `GLOSSARY-MAP.md` 列出各个上下文、它们所在的位置，以及彼此之间的关系：

```md
# Glossary Map

## Contexts

- [Ordering](./src/ordering/GLOSSARY.md): receives and tracks customer orders
- [Billing](./src/billing/GLOSSARY.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/GLOSSARY.md): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

skill 会自行推断适用哪种结构：

- 如果存在 `GLOSSARY-MAP.md`，读它来找到各个上下文
- 如果只有根目录的 `GLOSSARY.md`，就是单上下文
- 如果两个都没有，在第一个术语被敲定时惰性创建根目录的 `GLOSSARY.md`

存在多个上下文时，推断当前话题属于哪一个。判断不了就问。
