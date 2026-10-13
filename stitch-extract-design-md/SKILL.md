---
name: stitch-extract-design-md
description: >-
  直接从前端源码提取完整的设计系统文档（DESIGN.md）——支持 React、Vue、Svelte、
  Angular、纯 HTML/CSS 或任意 Web 框架。通过分析组件文件、样式表、Tailwind 配置、
  主题定义与设计令牌（design token），生成内容详实、与 Stitch 兼容的设计系统文档。
  当用户想从现有代码库逆向还原设计系统、审查项目的视觉语言、从源文件中提取设计令牌，
  或想弄清前端仓库的样式模式时，使用本技能——哪怕用户只是问“这个应用长什么样？”
  或“把这段代码里的设计提取出来”。
allowed-tools:
  - "stitch*:*"
  - "Bash"
  - "Read"
  - "Write"
  - "web_fetch"
---

# 从前端代码提取设计系统

分析前端源码，提取一份完整的设计系统文档（DESIGN.md），直接从源文件捕捉项目的视觉语言——颜色、字体排印、间距、组件模式与布局原则，全程无需构建或运行应用。

## 为什么需要这个技能

`design-md` 技能基于渲染后的 HTML 工作。但很多时候你手头只有一个代码库，还没法把应用跑起来，就想先弄清它的设计系统——可能依赖没装全、构建已经坏了，或者只是想快速做一次审查。本技能直接读取源文件本身：样式表、组件文件、主题配置和 Tailwind 配置。速度更快，而且任何环境下都可用。

## 适用场景

- 用户手上有前端代码库，想提取或整理它的设计系统
- 用户想把项目的视觉识别迁移进 Stitch
- 用户要求“审查某个仓库的样式”或“理解它的设计语言”
- 用户想基于现有源码生成一份 DESIGN.md
- 应用无法构建或渲染，但源码可用
- 用户想统一或梳理代码库中不一致的样式

## 前提条件

- 能访问前端项目的源码目录
- 无需构建或运行时依赖——本技能只读取源文件

---

## 工作流程

### 阶段 1：项目摸底

先弄清自己面对的是什么项目，这决定了后续采用哪套提取模式。

#### 1. 识别框架与技术栈

扫描项目根目录下的标志性文件：

| 特征文件 | 框架 / 工具 |
|:---|:---|
| `package.json` 含 `react` | React / Next.js |
| `package.json` 含 `vue` | Vue / Nuxt |
| `package.json` 含 `svelte` | Svelte / SvelteKit |
| `package.json` 含 `@angular/core` | Angular |
| `tailwind.config.js/ts` | Tailwind CSS |
| `postcss.config.js` | PostCSS 流水线 |
| 依赖中有 `styled-components` 或 `@emotion` | CSS-in-JS |
| 仅有 `.css` / `.scss` / `.less` 文件 | 纯 CSS / SASS |
| `theme.js` / `theme.ts` / `tokens.js` | 设计令牌文件 |

先读 `package.json`——它能揭示所用框架、CSS 工具链，以及引入的设计令牌库（如 `style-dictionary`、`@chakra-ui/react`、`@mui/material`、`ant-design`）。这些背景告诉你*该去哪里*找样式信息。

#### 2. 梳理源码目录结构

找出将要分析的关键目录和文件：

```
src/
├── components/     ← Component-level styles
├── styles/         ← Global stylesheets
├── theme/          ← Theme definitions, tokens
├── assets/         ← Fonts, images
├── app.css         ← Root styles
└── index.css       ← Entry CSS
```

另外留意：
- `tailwind.config.js` / `tailwind.config.ts` —— 自定义颜色、字体、间距
- `globals.css` / `global.css` —— CSS 自定义属性（变量）
- 任何 `theme.*` 或 `tokens.*` 文件
- 组件库配置（如 `chakra-theme.ts`、`vuetify.config.ts`）

#### 3. 阅读对应框架的参考指南

按所用框架查阅相应的提取模式：

- **React / Next.js / Tailwind** → [references/react-tailwind.md](references/react-tailwind.md)
- **Vue / Nuxt** → [references/vue.md](references/vue.md)
- **Svelte / SvelteKit** → [references/svelte.md](references/svelte.md)
- **Angular** → [references/angular.md](references/angular.md)
- **纯 CSS / SASS / Less** → [references/plain-css.md](references/plain-css.md)

这些参考文档包含各框架特有的模式，用于定位颜色、字体排印、间距与组件样式。继续之前，先读完与你项目匹配的那一份。

---

### 阶段 2：深度提取

系统地逐项处理每个设计维度：先从源文件收集原始数据，再将其提炼成描述性语言。

目标不是罗列每一条 CSS 属性，而是理解样式选择背后的*意图*，用自然、有编辑质感的语言描述出来，让另一位设计师（或 Stitch）能据此重现同样的视觉感受。

#### 1. 视觉主题与氛围

先读最宏观的样式，把握整体基调：

- **根背景**：`body` 或根元素的背景是什么？浅奶油色（#f 区间）传达轻盈、干净；深色（#0-#2 区间）传达沉郁、戏剧感。
- **留白哲学**：间距取值是宽裕（32px 以上）还是紧凑？查看根容器、区块包裹层和卡片组件上的 padding/margin 值。
- **密度**：数一数每个页面/区块里的组件数量。少而疏即为极简；多而密即为信息密集。
- **色温**：中性色偏暖（奶油色、棕褐色）还是偏冷（蓝灰、石板灰）？
- **整体感受**：用 1-2 句饱满的文字概括这种基调。

在源码中留意这些信号：

| 源码位置 | 它能告诉你什么 |
|:---|:---|
| 布局根元素上的 `background-color` 或 Tailwind `bg-*` | 整体明暗倾向 |
| Tailwind 配置或 CSS 变量中的间距刻度 | 留白哲学 |
| 组件数量与包裹层 padding 的对比 | 密度 |
| 自定义属性命名（`--warm-*` 还是 `--cool-*`） | 色温意图 |
| 主题文件中的注释 | 开发者亲口写下的设计意图 |

#### 2. 色彩体系与角色

提取代码库中每一个不重复的颜色，并为它们指派功能角色。在所有层面搜索：

**去哪里找颜色：**

| 层面 | 搜索什么 |
|:---|:---|
| CSS 自定义属性 | `--color-*`、`--primary`、`--bg-*` |
| Tailwind 配置 | `theme.extend.colors` |
| 主题/令牌文件 | 颜色对象、调色板 |
| 组件样式 | `background-color`、`color`、`border-color` |
| 内联/scoped 样式 | 模板中的 `bg-*`、`text-*` 类名 |
| CSS-in-JS 主题对象 | `colors`、`palette` 键 |

**如何组织：** 按功能而非色相给颜色分组：

1. **基础底色** —— 背景与表面颜色
2. **强调与交互色** —— CTA 按钮、激活状态、链接
3. **文字与文本层级** —— 主要、次要、三级文本
4. **功能状态** —— 成功、错误、警告、信息

为每个颜色起一个描述性的名字，唤起色彩的气质，而不是干巴巴的十六进制值：

- ❌ `#294056` → “蓝色”
- ✅ `#294056` → **“Deep Muted Teal-Navy”**（深灰调青蓝）—— 主 CTA、激活态导航

**去重很重要。** 代码库里常有近似重复的颜色（如 `#333` 与 `#2C2C2C`）。把它们合并到最能代表目标色的那一个名字之下。

#### 3. 字体排印规则

提取完整的字体排印体系：

**字体族：**
- 检查 CSS `font-family`、Tailwind `fontFamily`、Google Fonts 链接或本地 `@font-face` 声明。
- 留意每种字体的**性格**：几何还是人文，衬线还是无衬线，传达怎样的情绪。

**字号阶梯（层级）：**
- 找出每一级标题（H1-H6）和正文文本，记录：
  - `font-size`（rem 或 px）
  - `font-weight`（数值 + 描述性名称）
  - `letter-spacing`（以及为什么——为了优雅？为了紧凑？）
  - `line-height`（正文从宽以求易读？展示字收紧？）
- 梳理组件用法：产品卡片用哪级标题？hero 区块呢？

**间距原则：**
- 文本间距与整体间距刻度是什么关系？
- 标题与正文各自的 letter-spacing 规律
- line-height 哲学（正文宽松舒展，展示字更紧）

#### 4. 组件样式

分析最重要的 4-5 个 UI 基础组件：

**按钮：**
- 圆角半径（以及它传达什么——活泼？专业？极简？）
- primary、secondary、ghost 三种变体的配色方案
- hover/focus/active 状态与过渡时长
- padding 比例（水平与垂直）

**卡片 / 容器：**
- 圆角半径（常与按钮不同——略更圆）
- 阴影策略：完全扁平、hover 时浮现浅阴影，还是始终抬升？
- 描边处理：发丝线描边、彩色点缀，还是不描边？
- 内部 padding（宽裕还是紧凑？）
- 卡片内图片的处理方式（通栏出血、留白内缩，还是圆角？）

**导航：**
- 布局模式（横向顶栏、纵向侧栏、抽屉）
- 字体处理（大写、letter-spacing、字重）
- 激活/hover 状态指示（下划线、颜色、背景）
- 移动端行为（汉堡菜单、底部导航、抽屉）

**输入框与表单：**
- 描边样式与聚焦态行为
- 圆角风格是否与按钮一致
- padding 与触控目标尺寸

**领域特有组件：**
- 找出 1-2 个本项目独有的组件（如产品卡片、仪表盘小组件、聊天气泡），并描述它们的样式模式。

#### 5. 布局原则

提取结构性体系：

**网格与结构：**
- 最大内容宽度（来自容器上的 `max-width`）
- 栏格系统（CSS Grid、Flexbox 模式、既定断点）
- 响应式断点（来自 media query 或 Tailwind 配置）

**留白策略：**
- 基础间距单位（8px 栅格？4px？自定义？）
- 区块外边距（大区块之间留多少空间）
- 边缘留白（不同断点下的页面边距）

**对齐与视觉平衡：**
- 文本对齐模式（hero 居中、正文左对齐）
- 图文比例
- 视觉权重分布

**响应式行为：**
- 移动优先还是桌面优先？
- 栅格如何折叠？padding 如何缩放？
- 触控目标尺寸

#### 6. Stitch 生成要点

把提取结果综合成 Stitch 可直接使用的提示词：

- **氛围语言**：把基调转译成自然的描述性词汇
- **颜色参照**：按描述性名称 + hex 值列出各颜色
- **组件提示词**：写出 2-3 条能在 Stitch 中重现关键组件的示例提示词
- **迭代指南**：在该设计系统内打磨各屏幕的技巧

---

### 阶段 3：撰写 DESIGN.md

把所有内容装配成标准 DESIGN.md 格式，放到项目目录的 `.stitch/DESIGN.md`（`.stitch/` 目录不存在就先创建）。

> [!IMPORTANT]
> 文件顶部的 YAML frontmatter **必须**包含 `name` 与 `colors` 映射，与 [examples/DESIGN.md](examples/DESIGN.md) 示例中的写法完全一致。其他技能要解析这套设计系统，依赖这些结构化数据。
>
> 缺少这段至少包含核心颜色令牌的 YAML 块，即视为未正确使用本技能。

以 [examples/DESIGN.md](examples/DESIGN.md) 示例中的格式作为模板。文件必须以 YAML 块开头，其后为各 Markdown 章节：

```markdown
# Design System: [Project Name]
**Project ID:** [If known, otherwise omit]

## 1. Visual Theme & Atmosphere
[Rich 2-paragraph description of mood, philosophy, and key characteristics]

## 2. Color Palette & Roles
### Primary Foundation
### Accent & Interactive
### Typography & Text Hierarchy
### Functional States

## 3. Typography Rules
### Hierarchy & Weights
### Spacing Principles

## 4. Component Stylings
### Buttons
### Cards & [Domain-Specific Containers]
### Navigation
### Inputs & Forms
### [Domain-Specific Components]

## 5. Layout Principles
### Grid & Structure
### Whitespace Strategy
### Alignment & Visual Balance
### Responsive Behavior & Touch

## 6. Design System Notes for Stitch Generation
### Language to Use
### Color References
### Component Prompts
### Incremental Iteration
```

---

### 阶段 4：集成（可选）

如果用户想把设计系统推送进 Stitch：

1. 交给 `manage-design-system` 技能执行 MCP 的创建/更新调用
2. 你写好的 DESIGN.md 就是输入——Stitch API 集成由 manage-design-system 技能负责

如果用户只要文档本身，完成阶段 3 即可交付。

---

## 质量清单

交付 DESIGN.md 之前，逐项核对：

- [ ] 每个颜色都有描述性名称、hex 值和功能角色
- [ ] 字体排印涵盖字体族、性格描述和完整层级
- [ ] 组件样式描述了形状、颜色、状态与过渡
- [ ] 布局涵盖 max-width、栅格、断点与间距策略
- [ ] Stitch 生成要点使用自然语言，而非 CSS 语法
- [ ] 氛围章节读起来像编辑文案，而不是技术文档
- [ ] 近似重复的颜色已经合并
- [ ] 文档捕捉到样式背后的*意图*，而不只是原始数值

## 提升提取质量的技巧

- **读注释和 commit message。** 开发者常在代码注释（`/* hero section — breathable */`）和 commit message 里记录设计意图。这些是理解*为什么*的金矿。
- **检查是否用了设计令牌库。** 如果项目用了 `style-dictionary`、`@tokens-studio` 或类似工具，这些文件就是设计取值最权威的来源。
- **主题文件比组件样式信号更强。** 一份定义了调色板的 `theme.ts` 告诉你设计系统的本来意图；组件里散落的内联样式则告诉你实际落地了什么。两者都值得看，但要从主题文件入手。
- **Tailwind 配置本身就是一套设计系统。** 如果项目定制过 `tailwind.config.js`，那它*就是*设计系统——先从它提取，再抽查组件里有没有覆写。
- **CSS 自定义属性都出于有意。** 开发者定义了 `--brand-primary`，就是在告诉你：这是一个设计令牌。尊重它。
