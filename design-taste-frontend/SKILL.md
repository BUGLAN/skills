---
name: design-taste-frontend
description: 面向落地页、作品集与重设计的反 AI 味前端技能。Agent 先读懂需求简报、推断正确的设计方向，交付不带模板感的界面。能用真实设计系统就用真实设计系统，重设计先审计，并执行严格的 Pre-Flight 检查。
---

# tasteskill：反 AI 味前端技能

> 落地页、作品集与重设计。不适用于仪表盘、数据表格，也不适用于多步骤产品 UI。
> 以下每条规则都是**视情境而定**的，没有一条会自动触发。先读懂简报，再只取用契合的部分。

---

## 0. 简报推断（动手之前先读懂局面）

在碰代码或拧旋钮之前，先**推断用户真正想要什么**。大多数 LLM 设计产出之所以糟糕，是因为模型直接跳向某种默认审美，而不去读懂局面。

### 0.A 先读这些信号
1. **页面类型** - 落地页（SaaS / 消费品 / 代理公司 / 活动）、作品集（开发者 / 设计师 / 创意工作室）、重设计（保留还是推翻）、编辑类 / 博客。
2. **用户口中的氛围词** - "minimalist"、"calm"、"Linear-style"、"Awwwards"、"brutalist"、"premium consumer"、"Apple-y"、"playful"、"serious B2B"、"editorial"、"agency-y"、"glassy"、"dark tech"。
3. **参考信号** - 用户贴出的链接与截图、点名的产品、正在对标的品牌。
4. **受众** - B2B 采购评审团、追求设计感的消费者，还是扫一眼作品集的招聘官。审美由受众决定，而不是由你的品味决定。
5. **既有品牌资产** - logo、色彩、字体、摄影。对重设计而言，这些是起点素材，不是可选输入（见第 11 节）。
6. **隐性约束** - 无障碍优先的受众、公共部门、强监管行业、信任优先的电商、儿童产品。这些约束**优先于**审美偏好。

### 0.B 生成之前先输出一行「设计判读」
写任何代码之前，先用一行声明：**「判读如下：\<page kind>，面向 \<audience>，采用 \<vibe> 语言，倾向 \<design system or aesthetic family>。」**

判读示例：
- *「判读如下：B2B SaaS 落地页，面向技术买家，采用 Linear 风格的极简语言，倾向 Tailwind utilities + Geist + 克制动效。」*
- *「判读如下：独立设计师作品集，面向招聘负责人，采用编辑类 / 动态字体语言，倾向原生 CSS + scroll-driven animation + 定制字体排印。」*
- *「判读如下：公共部门服务网站重设计，采用信任优先语言，倾向 GOV.UK Frontend 或 USWDS。」*

### 0.C 简报含糊时，只问一个问题，不要瞎猜
只问**一个**澄清问题，绝不做连环问卷，且只在设计判读确实出现分歧时才问。例如：*「这个设计该更接近 Linear 的干净利落，还是 Awwwards 的实验感？」*

如果能从上下文自信推断出来，就**不要问**，直接声明设计判读并继续。

### 0.D 反默认纪律
不要默认使用：AI 紫渐变、深色网格背景上居中的 hero、三张等宽功能卡、到处都是的千篇一律 glassmorphism、满屏无限循环的微动画、Inter + slate-900。这些都是 LLM 的默认套路。要基于设计判读，有意识地越过它们。

---

## 1. 三大旋钮（核心配置）

设计判读完成后再设定三个旋钮。下文每一项布局、动效与密度决策都以它们为前提。

* **`DESIGN_VARIANCE: 8`** - 1 = 完全对称，10 = 艺术化的混沌
* **`MOTION_INTENSITY: 6`** - 1 = 静态，10 = 电影感 / 物理动效
* **`VISUAL_DENSITY: 4`** - 1 = 美术馆 / 疏朗，10 = 驾驶舱 / 数据密排

**基线：** `8 / 6 / 4`。除非设计判读要求覆盖，否则就用这组值。不要让用户去编辑这个文件，覆盖在对话中完成即可。

### 1.A 旋钮推断（设计判读 → 旋钮取值）
| 信号 | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| "minimalist / clean / calm / editorial / Linear-style" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury / brand" | 7-8 | 5-7 | 3-4 |
| "playful / wild / Dribbble / Awwwards / experimental / agency" | 9-10 | 8-10 | 3-4 |
| "landing page / portfolio / marketing site (default)" | 7-9 | 6-8 | 3-5 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3-4 | 2-3 | 4-5 |
| "redesign - preserve" | 沿用现有 | +1 | 沿用现有 |
| "redesign - overhaul" | +2 | +2 | 沿用现有 |

### 1.B 用例预设
| 用例 | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| 落地页（SaaS，主流） | 7 | 6 | 4 |
| 落地页（代理公司 / 创意） | 9 | 8 | 3 |
| 落地页（高端消费） | 7 | 6 | 3 |
| 作品集（设计师 / 工作室） | 8 | 7 | 3 |
| 作品集（开发者） | 6 | 5 | 4 |
| 编辑类 / 博客 | 6 | 4 | 3 |
| 公共部门服务 | 3 | 2 | 5 |
| 重设计 - 保留 | 沿用 | 沿用+1 | 沿用 |
| 重设计 - 推翻 | +2 | +2 | 沿用 |

### 1.C 旋钮如何驱动产出
把它们（或用户覆盖后的值）当作全局变量使用。本文档中的交叉引用一律指向这些确切的变量名，绝不要另造 `LAYOUT_VARIANCE` 或 `ANIM_LEVEL` 之类的别名。

---

## 2. 简报 → 设计系统映射

拿到设计判读（第 0 节）和旋钮（第 1 节）之后，选对地基。有官方包的东西不要自己发明 CSS，也不要把某种审美潮流冒充成官方系统。

### 2.A 何时动用真正的设计系统（使用官方包）
| 简报读起来像… | 选用 | 理由 |
|---|---|---|
| Microsoft / 企业级 SaaS / 仪表盘 | `@fluentui/react-components` 或 `@fluentui/web-components` | 官方 Fluent UI，Microsoft token，无障碍已就绪 |
| Google 风格 UI，Material 风味的产品 | `@material/web` + Material 3 tokens | 官方出品，可通过 Material Theming 主题化 |
| IBM 风格 B2B / 企业级数据分析 | `@carbon/react` + `@carbon/styles` | 官方 Carbon，数据密排模式成熟 |
| Shopify 应用界面 | `polaris.js` web components / Polaris React | Shopify admin UI 的硬性要求 |
| Atlassian / Jira 风格产品 | `@atlaskit/*` + `@atlaskit/tokens` | 官方 Atlassian DS |
| GitHub 风格开发者工具 / 社区页面 | `@primer/css` 或 `@primer/react-brand` | 官方 Primer；营销页用 Brand 变体 |
| 英国公共部门服务 | `govuk-frontend` | 法律与监管层面的预期 |
| 美国公共部门 / 信任优先 | `uswds` | 同上 |
| 本地商家 / 代理公司的快速 MVP | Bootstrap 5.3 | 无聊、快速、能用 |
| 现代无障碍 React 基础 | `@radix-ui/themes` | 原语 + 打磨成熟的主题 |
| 组件自有的现代 SaaS | shadcn/ui (`npx shadcn@latest add ...`) | 代码归你所有，定制容易；绝不交付默认形态 |
| 基于 Tailwind 的现代 SaaS / AI 营销 | Tailwind v4 utilities + `dark:` variant | 独立开发者与小团队构建的默认选择 |

**诚实原则：** 如果简报指向上述某个系统，就安装并使用**官方**包。不要手写复刻它的 CSS，也不要导入一套系统的 token 再覆盖掉九成。

**一个项目只用一套系统。** 不要在同一棵组件树里混用 Fluent React 与 Carbon，也不要把 shadcn/ui 组件塞进 Material 3 应用。

### 2.B 简报指向的是一种审美，而非一套系统
对下面这些方向，**没有唯一的官方包**。用原生 CSS + Tailwind + 一个有维护的组件库来构建，并在代码注释里诚实标注哪些是借鉴的灵感，哪些是官方素材。

| 审美 | 诚实的实现 |
|---|---|
| Glassmorphism（毛玻璃） | `backdrop-filter`、分层边框、高光叠加。为 `prefers-reduced-transparency` 提供实色填充回退。 |
| Bento（Apple 风格的瓷砖网格） | 用 CSS Grid 混排格子尺寸。没有任何库能独占它。 |
| Brutalism（粗野主义） | 原生 CSS、等宽字体、裸露边框。不用库。 |
| 编辑类 / 杂志风 | 衬线字体、非对称网格、慷慨留白。不用库。 |
| 暗黑科技 / 黑客风 | 等宽 + 霓虹强调，终端母题。不用库。 |
| 极光 / mesh 渐变 | SVG 或多层径向渐变。不用库。 |
| 动态字体排印 | 原生 CSS 动画、scroll-driven animations，滚动劫持用 GSAP。不用库。 |
| **Apple Liquid Glass** | Apple 只在 Apple 平台范围内提供该设计的文档。**不存在官方的 `liquid-glass.css`。** Web 实现都是用 `backdrop-filter` + 分层边框 + 高光做出的近似，必须明确标注为近似方案。 |

---

## 3. 默认架构与约定

除非设计判读选定了某个真实设计系统（第 2.A 节），否则采用以下默认值：

### 3.A Stack（技术栈）
* **Framework（框架）：** React 或 Next.js。默认使用 Server Components（RSC）。
  * **RSC 安全：** 全局状态只在 Client Components 中生效。在 Next.js 中，要把 provider 包进一个 `"use client"` 组件。
  * **交互隔离：** 任何用到 Motion、scroll 监听或指针物理效果的组件，都**必须**是独立的叶子组件，文件顶部带 `'use client'`。Server Components 只渲染静态布局。
* **样式：** **Tailwind v4**（默认）。仅当既有项目确实要求时才用 Tailwind v3。
  * v4 下**不要**在 `postcss.config.js` 里用 `tailwindcss` 插件，请改用 `@tailwindcss/postcss` 或 Vite 插件。
* **动画：** **Motion**（即原先的 Framer Motion）。从 `motion/react` 导入（`import { motion } from "motion/react"`）。`framer-motion` 包仍作为旧别名可用，新代码请优先 `motion/react`。
* **字体：** 一律使用 `next/font`（Next.js）或以 `@font-face` + `font-display: swap` 自托管。生产环境绝不要通过 `<link>` 引入 Google Fonts。

### 3.B 状态
* 隔离的 UI 用局部 `useState` / `useReducer`。
* 全局状态仅用于避免深层 prop 逐层透传，可用 Zustand、Jotai 或 React context。
* **绝不**用 `useState` 追踪由用户输入驱动的连续值（鼠标位置、滚动进度、指针物理、磁吸悬停）。请用 Motion 的 `useMotionValue` / `useTransform` / `useScroll`。`useState` 每次变化都会重渲染 React 树，在移动端会直接卡死。

### 3.C 图标
* **允许的库（按优先级）：** `@phosphor-icons/react`、`hugeicons-react`、`@radix-ui/react-icons`、`@tabler/icons-react`。
* **不推荐：** `lucide-react`。仅当用户明确要求，或项目已依赖它时才可接受。
* **绝不手写 SVG 图标。** 缺字形时，装第二个库或用基本形状拼合，不要从零画图标路径。
* **一个项目只用一族。** 不要在同一棵组件树里混用 Phosphor 和 Lucide。
* **全局统一 `strokeWidth`**（例如 `1.5` 或 `2.0`）。

### 3.D Emoji 政策
默认不推荐在代码、标记和可见文本中使用 emoji，用图标库的字形替代。**例外：** 仅当用户明确要求俏皮 / 聊天体 / 社交原生氛围时才允许 emoji，即便如此也要克制、有意图地使用。

### 3.E 响应式与布局机制
* 统一断点（`sm 640`、`md 768`、`lg 1024`、`xl 1280`、`2xl 1536`）。
* 用 `max-w-[1400px] mx-auto` 或 `max-w-7xl` 约束页面布局宽度。
* **视口稳定：** 全高 hero 区块**绝不**用 `h-screen`，**一律**用 `min-h-[100dvh]`，避免移动端（iOS Safari 地址栏）引起布局跳动。
* **用 Grid，别用 Flex 算术：** **绝不**用复杂的 flexbox 百分比计算（`w-[calc(33%-1rem)]`），**一律**用 CSS Grid（`grid grid-cols-1 md:grid-cols-3 gap-6`）。

### 3.F 依赖核验（强制）
导入任何第三方库之前，先查 `package.json`。包不存在时，先输出安装命令。**绝不**假设某个库已经存在。

---

## 4. 设计工程指令（纠偏）

LLM 默认走向陈词滥调，要主动覆盖这些默认值。每条规则都有视情境的例外路径。

### 4.1 字体排印
* **展示型 / 标题：** 默认 `text-4xl md:text-6xl tracking-tighter leading-none`。
* **正文 / 段落：** 默认 `text-base text-gray-600 leading-relaxed max-w-[65ch]`。
* **无衬线字体选择：**
  * **不推荐作默认：** `Inter`。优先选 `Geist`、`Outfit`、`Cabinet Grotesk`、`Satoshi`，或契合品牌的衬线体。
  * **例外：** 用户明确要中性 / 标准 / Linear 风格质感，或简报是公共部门 / 无障碍优先站点时，Inter 可以接受。
* **值得掌握的搭配：** `Geist` + `Geist Mono`、`Satoshi` + `JetBrains Mono`、`Cabinet Grotesk` + `Inter Tight`、`GT America` + `IBM Plex Mono`。

* **衬线纪律（极不推荐作默认）：**
  * 衬线体**极不推荐作为任何项目的默认字体**。「显得有创意 / 高级 / 编辑范」不构成动用衬线的理由。「创意简报 = 衬线体」这一默认心智模型，是生产测试中被抓包最多的 AI 破绽，没有之一。
  * **只有以下情况之一明确成立时，衬线才可接受：**
    - 品牌简报白纸黑字点名了某款衬线字体；或
    - 审美流派确实是编辑类 / 奢侈 / 出版物 / 手稿 / 传承 / 复古，而且你能说清为什么这款特定衬线契合这个特定品牌。
  * 其余一切情形（创意代理、设计工作室、现代品牌、高端消费、作品集、生活方式类），**默认用无衬线展示字体**（Geist Display、ABC Diatype、Söhne Breit、Cabinet Grotesk Display、Migra Sans、GT Walsheim、Inter Display、PP Neue Montreal）。无衬线展示字体并不「无聊」，它成为默认的理由，正如黑色成为时尚的默认色。
  * **强调规则（相关）：** 想在标题中强调某个词（动态排印里 "and `spatial` design" 那种手法）时，用**同一字体的斜体或粗体**。不要为了视觉趣味往无衬线标题里硬塞一个衬线词（反之亦然）。跨字体族强调是业余做法，同族内的斜体 / 粗体强调才是正解。
  * **明确禁止作默认：** `Fraunces` 和 `Instrument_Serif`（LLM 最偏爱的两款展示衬线）。
  * **如果衬线确有正当理由**（如上所述，很少见），从这个池子里轮换选用，连续项目绝不复用同一款：PP Editorial New、GT Sectra Display、Cardinal Grotesque、Reckless Neue、Tiempos Headline、Recoleta、Cormorant Garamond、Playfair Display、EB Garamond、IvyPresto、Migra、Editorial Old、Saol Display、Söhne Breit Kursiv、Domaine Display、Canela、Schnyder、Tobias、NB Architekt、ITC Galliard。

* **斜体下降部留空（强制）：** 展示字体里用斜体且单词含下降部字母（`y g j p q`）时，`leading-[1]` 或 `leading-none` 会裁掉下降部。至少用 `leading-[1.1]`，并在外层元素上加 `pb-1` 或 `mb-1` 预留空间。交付前逐一审查展示标题里的每个斜体词。

### 4.2 色彩校准
* 强调色最多 1 个，饱和度默认 < 80%。
* **反紫规则（THE LILA RULE）：** 「AI 紫 / 蓝色辉光」审美不推荐作默认。不要自动给按钮加紫色光晕，不要随手来霓虹渐变。用中性底色（Zinc / Slate / Stone）搭配高对比的单一强调色（Emerald、Electric Blue、Deep Rose、Burnt Orange 等）。
* **例外：** 品牌或简报明确要求紫 / 紫罗兰 / lila 时，就大方拥抱，但要带着意图执行：一致的调色板、协调的中性色、克制的渐变，而不是千篇一律的 AI 渐变垃圾。
* **一个项目一套调色板。** 同一项目内不要在暖灰和冷灰之间来回摇摆。
* **色彩一致性锁（强制）：** 页面一旦选定强调色，就要在整页贯彻。暖灰站点不会在第 7 节突然冒出蓝色 CTA；玫瑰色强调的站点也不会在页脚出现青色状态徽章。选定一个强调色，锁死，交付前逐一审查每个组件。

* **高端消费调色板禁令（强制，出现频率第二高的 AI 破绽）：**
  * 高端消费类简报（锅具、康养、手作、奢侈、传统工艺、DTC 家居等）的 LLM 默认套路是**暖米色 / 奶油色 + 黄铜 / 陶土 / 牛血红 / 赭石 + 浓缩咖啡色 / 墨色深字**。具体被禁的默认背景与强调色 hex 色系：
    - 背景：`#f5f1ea`、`#f7f5f1`、`#fbf8f1`、`#efeae0`、`#ece6db`、`#faf7f1`、`#e8dfcb`（全部属于「暖纸 / 奶油 / 白垩 / 骨白」）
    - 强调：`#b08947`、`#b6553a`、`#9a2436`、`#9c6e2a`、`#bc7c3a`、`#7d5621`（全部属于「黄铜 / 陶土 / 牛血红 / 赭石」）
    - 文字：`#1a1714`、`#1a1814`、`#1b1814`（全部属于「浓缩咖啡 / 暖调近黑」）
  * 这套调色板被禁止作为高端消费类简报的默认选择。你交付过的每一个高端消费网站用的都是这套配色，品牌因此失去辨识度。
  * **默认替代方案（轮换使用，不要重复）：**
    - **冷奢：** 银灰 + 铬 + 烟灰（参考 Tesla、Apple Watch Hermes 去掉皮革的质感）
    - **森林：** 深绿 + 骨白 + 琥珀强调（参考 Filson、Patagonia 高端线）
    - **黑棕配：** 真正的近黑 + 暖棕褐，对比锐利，不带米色
    - **钴蓝 + 奶油：** 高饱和蓝对单一中性色，不用黄铜
    - **赤陶 + 板岩：** 暖锈色对冷灰，不用黄铜
    - **橄榄 + 砖红 + 纸白：** 灰调橄榄绿配砖红强调
    - **纯单色 + 一抹高饱和：** 近白 + 近黑 + 一个亮色强调（电光蓝、祖母绿、亮粉等）
  * **调色板轮换规则：** 如果上一个高端消费项目用了米色 + 黄铜系，这一个**必须**换用别的色系。同一套暖调手作配色绝不连续交付两次。
  * **例外：** 米色 + 黄铜 + 浓缩咖啡配色仅当品牌简报明确点名这些颜色，或品牌调性确属复古 / 手作 / 暖调工艺且你能说清为什么这套配色契合这个品牌时才可接受。以「这是锅具简报」为由直接套用，禁止。

### 4.3 布局多样化
* **反居中偏好：** `DESIGN_VARIANCE > 4` 时避免居中的 hero / H1 区块。强制改用「分屏」（50/50）、「左对齐内容 / 右对齐素材」、「非对称留白」或滚动钉住结构。
* **例外：** 编辑类 / 宣言式 / 发布公告类简报中，信息本身就是设计，居中 hero 可以接受。

### 4.4 材质、阴影与卡片
* 只有当浮起确实传达真实层级时才用卡片，否则用 `border-t`、`divide-y` 或负空间分组。
* 用阴影时，让它带上背景色的色调。浅色背景上不要用纯黑投影。
* `VISUAL_DENSITY > 7` 时：禁止千篇一律的卡片容器，让数据指标在素净布局中呼吸。
* **形状一致性锁（强制）：** 全页只选一套圆角标尺并贯彻到底。选项：全直角（radius 0）、全柔和（radius 12-16px）、全胶囊（交互元素全圆角）。混用仅当有成文规则（如「按钮全胶囊、卡片 16px、输入框 8px」）且处处遵守时才允许。方直角布局里放圆形按钮，或胶囊按钮页面上放直角卡片，都是坏设计。

### 4.5 交互 UI 状态
LLM 默认只做「静态成功态」。要始终实现完整的状态循环：
* **加载：** 骨架屏要与最终布局的形状一致，避免千篇一律的圆形 spinner。
* **空状态：** 构图讲究，并指引如何填充内容。
* **错误状态：** 清晰；表单用行内提示，上下文场景用 toast（仅限瞬时反馈）。
* **触觉反馈：** `:active` 时用 `-translate-y-[1px]` 或 `scale-[0.98]` 模拟物理按压。
* **按钮对比度检查（强制，无障碍）：** 交付任何按钮前，确认按钮文字在其背景上可读。白按钮配白字、`bg-white` 的 CTA 配 `text-white` 标签、无边框透明按钮直接压在页面背景上，全都在禁止之列。逐一审查每个 CTA：对比度至少 WCAG AA（正文 4.5:1，18px 以上大字 3:1）。摄影背景上的 ghost 按钮同样适用此规则（加背板、scrim 或描边）。
* **CTA 按钮换行禁令（强制）：** 桌面端按钮文字**必须**单行放下。"VIEW SELECTED WORK" 这类标签折成两三行，按钮就是坏的。修法二选一：缩短标签（主 CTA 最多 3 个词，最好 1-2 个），或加宽按钮（不要人为给 CTA 设 `max-width` 限制）。桌面端 CTA 换行属于 Pre-Flight 失败。
* **CTA 意图不得重复（强制）：** 同一页面出现两个意图相同的 CTA 即 Pre-Flight 失败。同意图示例："Get in touch" + "Contact us" + "Let's talk" + "Start a project" + "Start something" + "Reach out" 都是「联系」意图 → 只选**一个**标签，在页面各处（导航、hero、页脚）统一使用。同理，"Try free" + "Get started" + "Sign up free"（都是「注册」意图），"View work" + "See selected work" + "Browse projects"（都是「作品」意图）。一种意图只用一个标签。
* **表单对比度检查（强制，无障碍）：** 表单输入框、占位文字、focus 环、帮助文字、错误文字都必须相对所在区块背景通过 WCAG AA 对比度。近白表单上的浅色占位符、白色页面区块上的白色表单、对比度低于 4.5:1 的表单标签，全都在禁止之列。交付前逐一审查每个表单。

### 4.6 数据与表单模式
* 标签在输入框**上方**。帮助文字可选，但要写进标记。错误文字在输入框**下方**。输入块统一用 `gap-2`。
* 绝不用占位符当标签，一次都不行。

### 4.7 布局纪律（硬规则。违反任何一条都等于交付残次品）

* **Hero 必须装进首屏视口。** 桌面端标题最多 2 行，副文案最多 **20 词**且不超过 3-4 行，CTA 不滚动即可见。文案太长就缩小字号或删文案。如果 20 词的副文案说不清价值主张，那是价值主张本身不清晰，不是规则太紧。绝不让 hero 溢出首屏、逼用户滚动去找 CTA。
* **Hero 字号纪律。** 字号与图片尺寸要**一起**规划。hero 素材较大且标题超过 6 个词时，不要一上来就 `text-7xl/text-8xl`。合理默认区间：多数 hero 用 `text-4xl md:text-5xl lg:text-6xl`；标题只有 3-5 个词时才用 `text-6xl md:text-7xl`。4 行的 hero 标题一定是字号错误，绝不是文案长度问题。
* **Hero 顶部内边距上限（强制）：** 桌面端 hero 顶部内边距最大 `pt-24`（约 6rem）。再大就会让 hero 内容悬在视口半腰，看起来像布局 bug 而非有意留白。hero 需要更多呼吸感时，加大字号或素材尺寸，而不是顶部内边距。
* **Hero 元素堆叠纪律（文字元素最多 4 个）。** hero 是一个瞬间，不是功能清单。允许的文字元素总计最多 4 个：
  1. 眉题（eyebrow，小号全大写标签）或品牌条，或两者都不要，最多取其一
  2. 主标题（最多 2 行，见上文）
  3. 副文案（最多 20 词，最多 4 行）
  4. CTA（1 个主按钮 + 最多 1 个次按钮）
  - **Hero 中禁止出现：** CTA 下方的小标语（"Works with GitHub, GitLab, and self-hosted Git"）、信任微型条（"Used by engineering teams at..."）、价格诱饵（"Free for solo, $10/user for teams"）、功能要点列表、社会证明头像行。这些一律移到 hero 正下方的专属区块。
  - 同一个 hero 里既有眉题又有 CTA 下方标语时，删标语；既有品牌条又有标语时，删标语。每个 hero 最多保留一个次要小文字元素。
* **"Used by" / "Trusted by" logo 墙放在 hero 之下，绝不放进 hero。** hero 承载价值主张和主 CTA，logo 墙是正下方的独立区块。不要把信任 logo 塞进 hero 文案所在的同一行 flex 里。
* **导航在桌面端必须单行呈现。** `lg`（1024px）下放不下时，压缩标签、砍次要项，或改用汉堡菜单。桌面端两行导航就是坏设计。
* **导航高度上限：桌面端最高 80px，默认 64-72px。** 不要用那种吃掉 15% 视口的巨型「代理公司风」导航条。
* **Bento 网格必须有节奏，不能单向重复。** 不要连排 6 行「左图右文」。构图要有变化：全宽功能行、非对称格子尺寸、纵向断口交替使用。
* **BENTO 格数规则（强制）：** Bento 网格的格子数量必须与内容数量严格相等。3 个条目 → 3 格（1+2 拆分、2+1 或非对称三格）。5 个条目 → 5 格（2+3、3+2、1 大 + 4 小等）。网格中部或末尾出现空格，说明规划出错：重塑网格，不要贴一块空白瓷砖。
* **区块布局重复禁令。** 某个布局族（如三列图文卡、全宽引言、图文分栏）一旦用于某个区块，整页最多再出现一次。「精选委托」不能长得像「我们做什么」。8 个区块的落地页至少要用 4 种不同的布局族。
* **Z 字交替上限（强制）。** 「左图右文」「左文右图」来回交替的 zigzag 布局 = 平庸。这种图文分栏模式连续最多 2 个区块，第 3 个连续的图文分栏即 Pre-Flight 失败。用全宽区块、纵向堆叠区块、bento 网格、marquee 或其他布局族打破模式。
* **眉题克制（强制，生产测试中违反率第一的规则）。** 「眉题」是区块标题上方的小号全大写宽字距标签（如 `FOUR COLORWAYS`、`SELECTED WORK`、`THE HARDWARE`、`Git-native task management`）。典型 CSS 特征：`text-[11px] uppercase tracking-[0.18em]`、`font-mono text-[10.5px] uppercase tracking-[0.22em]`。AI 建的站恨不得每个区块标题上面都放眉题，节奏千篇一律。硬规则：
  - **每 3 个区块最多 1 个眉题。** hero 算 1 个区块，因此 9 个区块的页面最多共 3 个眉题。
  - 区块 A 有眉题，接下来 2 个区块不得再有。
  - **Pre-Flight 检查是机械的：** 数一遍所有区块组件里 `uppercase tracking`（或标题上方类似的小号大写等宽标签）的实例数。若数量 > ceil(sectionCount / 3)，即不通过。
  - **不用眉题时怎么办：** 直接去掉。标题本身就够了。真需要给区块归类时，区块在页面中的位置已经说明了一切，无需标签。
* **分栏标题禁令（强制）。** 「左侧大标题 + 右侧小解释段落」的区块头部模式（左 col-span-7/8、右 col-span-4/5，一小段正文悬在右栏）**默认禁止**。每个区块应只有一个聚焦的信息。确实同时需要标题和解释段落时，纵向堆叠（标题在上，正文在下，max-width 65ch）。只有存在真正的构图理由（如右栏承载的是视觉或交互元素，而非凑数文字）时才可动用分栏标题。
* **Bento 背景多样性（强制）。** Bento 与功能网格区块不能是 6 张白底卡里装文字。任何多格网格中至少 2-3 格要有真实的视觉变化：真实图片、契合品牌的渐变（不要 AI 紫）、图案或着色背景。奶油底上放奶油卡的纯文字 bento，哪怕页面其余部分再好，读起来也是无聊的 AI 默认。
* **移动端折叠必须逐区块显式声明。** 每个多栏布局都要在同一个组件里声明 `< 768px` 的回退方案。不要「没事，Tailwind 会处理」这种想当然。

### 4.8 图像与视觉素材策略

落地页和作品集是**视觉产品**。纯文字页面配 div 假截图，就是典型的 slop。

**视觉素材的优先级：**
1. **图像生成工具优先。** 环境中只要有任何图像生成工具（`generate_image`、MCP 图像工具、IDE 集成生成、OpenAI 图像工具等），就**必须**用它产出分区块素材：hero 摄影图、产品图、纹理背景、氛围图。按区块需要的长宽比生成。不要因为觉得手写 CSS 更快就跳过这一步。
2. **真实网络图片其次。** 没有生成工具时，用真实摄影图源。可接受的默认：
   * `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` 作占位摄影图（seed 要能描述该区块，如 `marrow-cookware-kitchen`）
   * 简报提供了真实图库或品牌 URL 时，直接使用
   * 明确允许时，用开放授权图源（直链 Unsplash、Pexels）
3. **最后手段：告知用户。** 两者都不可行时，**不要**用满页手绘 SVG 插画或 div 搭的「假截图」填充，而是留下清晰标注的占位槽（`<!-- TODO: hero product photo, 1600x1200 -->`），并在回复末尾说明：*「本页需要真实图片，位置如下：\[list of placements\]。请生成或提供这些图片。」*

**极简站点同样需要真实图片。** 纯文字页面不是极简，是半成品。即便是编辑类 Linear 风格站点，也至少要 2-3 张真实图片（hero、一张产品 / 生活方式图、一张辅助图）。简报气质克制时，生成黑白极简摄影即可；不要因为旋钮调得低就完全不放图。

**社会证明要用真实公司 logo。** 简报需要 "Trusted by / Used by / Customers" logo 墙时，不要默认用纯文字字标（排成一行的 `<span>Acme Co</span>`），要用真实 SVG logo：
* **来源：Simple Icons**（`https://cdn.simpleicons.org/{slug}/ffffff` 可取任意颜色，或用 `simple-icons` npm 包）。覆盖绝大多数知名品牌。
* **替代：devicon**，用于技术栈 logo（`@svgr/cli` 或 CDN）。
* **品牌名是虚构的？那就虚构一个 SVG 标志。** 生成简单的字标图案（圆圈中的单字母、双字母连字、抽象图形），以内联 `<svg>` 呈现并与页面风格一致。虚构品牌名配纯文字字标会显得千篇一律。
* **始终**确保 logo 在明暗两种模式下都能正常呈现（深底白标、浅底黑标，或单色主题变量）。
* **仅 logo 规则（强制）：** logo 墙 = 只有 logo，别无他物。不要在每个 logo 下面印行业 / 品类标签（不许 `Vercel` 下面加 `hosting`，不许 `Stripe` 下面加 `payments`，不许 `Cloudflare` 下面加 `infra`）。logo 本身就是信誉，标签提供不了用户不知道的信息。可选：品牌名作屏幕阅读器的 alt 文本；可选：链到品牌官网。仅此而已。

**手绘插画：**
* 来自图标库的 SVG 图标：没问题（见第 3.C 节）。
* 手绘装饰 SVG（自定义插画、logo、图形标识）：**强烈不推荐**，绝不作默认。仅以下情况可接受：
  - 简报明确要求（"draw me an SVG logo"）
  - 只是单一、简单的几何图形（一个方块、一个圆、展示字体的字标）
  - 你对产出质量有把握

**div 假截图一律禁止。** 用 `<div>` 矩形、假任务列表、假仪表盘、假终端窗口拼出的「手工产品预览」是一个典型 AI 破绽。需要展示产品时：
* 有真实截图 URL 就用真实截图
* 用图像工具生成一张
* 用真实组件预览（页面内嵌一个真正的迷你版 UI）
* 或者干脆不放预览，改用编辑类摄影图

**Hero 需要真实视觉。** 文字 + 渐变色块不是 hero，只是占位符。

### 4.9 内容密度

落地页活在**第一印象**里，而不是通读里。砍，要下狠手。

* **每个区块的默认内容形态：** 短标题（≤ 8 词）+ 短副段落（≤ 25 词）+ 一个视觉素材**或**一个 CTA。超出的部分必须由该区块的职责来证明其必要。
* **不要数据倾倒区块。** 营销页上放 20 行发表记录表、30 行获奖清单、巨型价格矩阵，都是错误布局。改用：
  - 前 3-5 条亮点 + 「查看完整列表」链接
  - marquee / carousel 承载广度
  - 数据本身就是产品时，干脆另立页面
* **长列表需要换一种 UI 组件，而不是把列表拉得更长。** 默认的带圆点 `<ul>` / `divide-y` 行是最偷懒的选择。超过 5 项时，改用以下任一：
  - 双栏拆分 + 分组条目
  - 卡片网格，每项一图一标签
  - 条目可分类时用 tabs / 手风琴
  - 横向 scroll-snap 药丸
  - 广度优先的列表（用户评价、logo、能力）用 carousel
  - 「大量不需要逐一关注的东西」用 marquee
  10 行、行行带发丝线的规格表是最糟糕的默认。要么把行归成 2-3 组、稀疏地加分隔线，要么改成一条规格一张卡的布局。
* **规格表专项（Marrow 锅具模式）。** 每行都挂 `border-b` 的长产品规格表，是锅具 / 硬件 / 服装 / 手作商品简报的 AI 默认，禁止。具体替代：
  - **双栏卡片网格：** 每条规格一张卡，含规格名、数值（大号展示数字）和一行「为何重要」的说明。桌面端双栏，移动端单栏。
  - **横向 scroll-snap 药丸：** 每条规格一颗药丸，用户滑动翻看。
  - **分组聚块：** 把 10 条规格归成 3 个逻辑簇（如 "Materials"、"Cooking"、"Warranty"），每簇一条柔和分隔线加一个簇标题。
  - **主打与余量：** 3-4 条主打规格做成大号展示瓷砖，其余折叠进「查看完整规格」的展开区。

* **文案自查（交付前强制）：** 宣布任务完成之前，重读页面上每一条可见字符串（标题、副标题、眉题、按钮标签、正文、图注、alt 文本、页脚文字、错误提示）。标记出任何这样的字符串：
  - **语法破碎**（"free on its past"、"two plans but one is honest"、脱离语境的 "to put it on the table"）
  - **指代不明**（没有前文却来一句 "we plan to stay that way"）
  - **AI 幻觉腔**（可爱但错误的文字游戏、不成立的生硬比喻、「优雅的空洞」式措辞）
  - **LLM 硬凹深沉感**（阴阳怪气的谦逊、假匠人标签、故作诗意的小字注脚）
  被标记的字符串一律重写。拿不准一句话是否通顺时，就换成平实的功能性句子。AI 生成的俏皮文案比无聊文案更糟。
* **假精确数字要警惕。** `92%`、`4.1×`、`48k`、`5.8 mm`、`13.4 lb` 这类数字，要么：
  - 来自真实数据（简报、品牌规范、公开指标），可以
  - 明确标注为虚构（`<!-- mock -->`、"example"、"sample data"），可以
  - 是 AI 编造的规格美学，禁止。不要伪造品牌从未宣称的工程精度。
* **每页一种文案语域。** 除非品牌声音明确要求，不要在同一构图里混搭技术等宽体（"47 tasks · 0.6 ctx-switches/day"）、编辑类散文和营销腔。

### 4.10 引言与用户评价

* 引文正文**最多 3 行**，绝不到 6 行。原始引文更长就删。落地页引言是节选，不是完整评论。
* 字号极小（如页脚式评价）时，行数上限可略微放宽。精神是「一眼看完」。
* **引文内不用 em-dash（破折号）** 作装饰（长停顿、动态破折号、破折号列表）。见第 9.G 节，em-dash 全面禁止。
* 署名：姓名 + 职务 +（可选）公司。绝不只写名字（"- Sarah"）。
* 引号：用真正的排版引号（ " " ）或干脆不用，不要用直 ASCII 引号（ " ）。

### 4.11 页面主题锁（明暗模式一致性）

整页只有一个主题，区块不得反转。

* 页面是暗色模式，所有区块就都是暗色模式。不许在暗色区块中间夹一个暖纸色的浅色区块（反之亦然）。不能让用户滚到一半感觉换了个网站。
* 例外：简报明确要求「色块叙事」或「滚动换主题」手法，且这是有意的构图（一次完整的主题切换、有强转场，而不是随机交替）时，每页允许一次。
* 默认行为：在页面层级选定 light、dark 或 auto（`prefers-color-scheme`）并锁死。同一主题族内的区块级底色微调没问题（`bg-zinc-950` 挨着 `bg-zinc-900`）；`bg-zinc-950` 的页面滚到一半翻成 `bg-amber-50` 就是坏的。
* 用自带主题化的设计系统（Radix Themes、配 `<Theme>` 的 shadcn/ui）时，在 `layout.tsx` 或页面根节点把主题设**一次**，不许个别区块覆盖。

---

## 5. 情境感知的主动增强

这些是工具，不是默认项。设计判读需要时才用。**没有一条会自动生效。**

* **Liquid Glass / Glassmorphism：** 适合高端消费、Apple 系、奢侈品牌或媒体叠加氛围；不适合仪表盘、公共部门或「无聊 B2B」。使用时要超越 `backdrop-blur`：加 1px 内边框（`border-white/10`）和细微内阴影（`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`），营造真实的边缘折射。`prefers-reduced-transparency` 下提供实色填充回退。
* **磁吸微物理：** `MOTION_INTENSITY > 5` 且简报偏高端 / 俏皮 / 代理风时使用。实现**只能**用 Motion 的 `useMotionValue` / `useTransform`，在 React 渲染周期之外进行，绝不用 `useState`。见第 3.B 节。
* **永续微交互**（Pulse、Typewriter、Float、Shimmer、Carousel）：`MOTION_INTENSITY > 5` 且区块确实因动效受益（状态指示、实时信息流、AI 感）时使用。**不是每张卡都需要无限循环。** 信息型区块就让它安静待着。弹簧物理用 `type: "spring", stiffness: 100, damping: 20`，不要线性缓动。
* **「宣称了动效，就要看得到动效。」** `MOTION_INTENSITY > 4` 时页面必须真的动起来：至少要有 hero 入场过渡、关键区块的滚动显现、CTA 的悬停物理。自称 `MOTION_INTENSITY: 7` 的静态页面是坏的。反过来，若现有条件做不出能跑的动效，就把旋钮降到 3，交付一个干净的静态页。绝不做半途而废的动效（被截断的 ScrollTrigger、跳变的入场、漏写的清理）。
* **动效必须有动机（强制）。** 加任何动画前先问：「这个动画传达了什么？」有效答案：层级（把注意力引向该看的地方）、叙事（按叙事顺序揭示内容）、反馈（回应用户操作）、状态切换（展示发生了变化）。无效答案：「看起来很酷」。因为 GSAP 可用就满屏 GSAP 是业余行为。每个 ScrollTrigger、每个 marquee、每个 pin 住的区块都要有理由。一句话说不清理由，就删掉这个动画。
* **每页 marquee 至多一个（强制）。** 横向滚动文字 marquee（"logos endlessly scrolling"、"manifesto scrolling sideways"、"kinetic word strip"）每页至多出现**一次**。同页两个以上 marquee 就是偷懒的凑数。挑出 marquee 真正服务内容的那个区块，其余区块换别的布局。
* **GSAP Sticky-Stack 模式（使用 scroll-stack 时）。** 「滚动卡片堆叠」必须是真正的 sticky-stack，不是按顺序逐个显现的列表。规范代码骨架见下方第 5.A 节。常见失败：trigger 在滚动中途触发，而不是在视口顶部钉住。修法：用 `start: "top top"`，不要 `start: "top center"` 或 `"top 80%"`。
* **GSAP Horizontal-Pan 模式（使用横向滚动劫持时）。** 规范骨架见下方第 5.B 节。常见失败：区块尚未钉住动画就开跑，用户看到半截画面。修法相同：`start: "top top"`，pin 住外层容器，scrub 内层轨道。

### 5.A Sticky-Stack - 规范骨架

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",                              // pin at viewport top
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div
          key={i}
          className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center"
        >
          {card}
        </div>
      ))}
    </div>
  );
}
```

要点：`start: "top top"`、`pin: true`，除最后一张外每张卡都被钉住，缩放 / 透明度变换由**下一张**卡的 scroll trigger 驱动（于是下一张到来时上一张缩小）。

### 5.B Horizontal-Pan - 规范骨架

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",                              // pin starts when section top hits viewport top
          end: () => `+=${distance}`,                    // scroll distance = track width minus viewport
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">
        {children}
      </div>
    </section>
  );
}
```

要点：`start: "top top"`、`pin: true`、`end: "+=${distance}"`（滚动长度 = 所需横向行程）、`scrub: 1`。外层容器被钉住，用户纵向滚动时内层轨道横向滑移。

### 5.C Scroll-Reveal Stagger - 规范骨架（更轻的替代）

简单的「条目进入视口时出现」（无需 pin）场景，优先用 Motion 的 `whileInView` 而非 GSAP：更轻，也不需要 ScrollTrigger：

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{
            duration: 0.6,
            delay: i * 0.06,
            ease: [0.16, 1, 0.3, 1],
          }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

适用场景：功能列表、评价网格、logo 墙，一切只需「随滚动入场」的东西。把 GSAP 留给真正的 pin / scrub 工作。

### 5.D 禁用的动画模式

* **`window.addEventListener("scroll", ...)`** 已禁。它在每个滚动帧上运行，容易卡顿，也没有批处理。请用 Motion 的 `useScroll()`、GSAP 的 `ScrollTrigger`、IntersectionObserver，或 CSS `scroll-driven animations`（`animation-timeline: view()`）。
* **在 React state 里用 `window.scrollY` 自算滚动进度**，原因同上，每帧都重渲染。
* **触碰 React state 的 `requestAnimationFrame` 循环。** 请改用 motion values（`useMotionValue` + `useTransform`）。
* **布局过渡：** 可见的状态变化（列表重排、弹窗展开、路由间共享元素）用 Motion 的 `layout` 和 `layoutId` props。不要「以防万一」给静态内容也套 `layout`，那会付出测量开销。
* **交错编排：** 序列重要的显现时刻用 `staggerChildren`（Motion）或 CSS 级联（`animation-delay: calc(var(--index) * 100ms)`）。`staggerChildren` 的父级（`variants`）与子级**必须**处于同一棵 Client Component 树。

---

## 6. 性能与无障碍护栏

### 6.A 硬件加速
* 只动画 `transform` 和 `opacity`，绝不动画 `top`、`left`、`width`、`height`。
* `will-change: transform` 惜用，只加在真正会动的元素上。

### 6.B Reduced Motion（强制）
* **`MOTION_INTENSITY > 3` 的任何动效都必须尊重 `prefers-reduced-motion`。** 没有商量余地。
* Motion 中：用 `useReducedMotion()` 包裹并降级为静态。
* CSS 中：把动画关进 `@media (prefers-reduced-motion: no-preference)`，或在 `@media (prefers-reduced-motion: reduce)` 下提供禁用动画的覆盖块。
* 无限循环、视差、滚动劫持、磁吸物理在减弱动态模式下**必须**坍缩为静态 / 瞬时呈现。

### 6.C 暗色模式（所有面向消费者的页面强制）
* **从第一天起就为两种模式设计。** 没有用户明确指示，绝不交付只有浅色或只有深色的页面。
* token 用 Tailwind `dark:` 变体或 CSS 变量，二选一，每个项目只定一种策略。
* **此处不指定具体的暗色配色。** 由简报决定。两种模式下都要保持视觉层级、品牌识别度和 WCAG AA 对比度（正文达 AAA）。
* 尊重 `prefers-color-scheme: dark`。默认跟随系统偏好，除非品牌坚持单一模式。

### 6.D Core Web Vitals 目标
* **LCP** < 2.5s。hero 图片必须 `next/image priority` 或预加载。
* **INP** < 200ms。重活移出主线程。
* **CLS** < 0.1。给图片、字体、嵌入内容预留空间。
* 宣布页面完工前先跑 Lighthouse。

### 6.E DOM 开销
* 颗粒 / 噪点滤镜**只**加在固定定位、`pointer-events-none` 的伪元素上（如 `fixed inset-0 z-[60] pointer-events-none`），**绝不**加在滚动容器上：持续的 GPU 重绘会毁掉移动端帧率。
* 注意包体积。Motion 不算小，Three.js 很大。首屏之外的一切都做懒加载。

### 6.F Z-Index 克制
绝不滥用任意 `z-50` 或 `z-10`。z-index 严格用于系统性的层级场景（sticky 导航、模态、遮罩、颗粒层），并在项目常量文件里记录 z-index 标尺。

---

## 7. 旋钮定义（技术参考）

### DESIGN_VARIANCE（1-10 级）
* **1-3（可预测）：** 对称 CSS Grid（12 栏、等 fr 单位）、等距内边距、居中对齐。
* **4-7（错位）：** `margin-top: -2rem` 叠压、图片长宽比错落（4:3 挨着 16:9）、左对齐标题配居中数据。
* **8-10（非对称）：** masonry 布局、带分数单位的 CSS Grid（`grid-template-columns: 2fr 1fr 1fr`）、大面积留白区（`padding-left: 20vw`）。
* **移动端覆盖：** 4-10 级的 `md:` 以上非对称布局，在 `< 768px` 视口**必须**坍缩为严格的单栏（`w-full`、`px-4`、`py-8`）。

### MOTION_INTENSITY（1-10 级）
* **1-3（静态）：** 无自动动画，只有 CSS `:hover` 和 `:active` 状态。反正 `prefers-reduced-motion` 本来就是默认模式。
* **4-7（流畅 CSS）：** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`；入场用 `animation-delay` 级联；聚焦 `transform` 和 `opacity`。
* **8-10（高级编排）：** 复杂滚动触发显现、视差、scroll-driven animation（CSS `animation-timeline` 或 GSAP ScrollTrigger）。用 Motion hooks。**绝不使用 `window.addEventListener('scroll')`**，这是硬禁令，不是「尽量别用」。许可的替代方案见第 5.D 节。

### VISUAL_DENSITY（1-10 级）
* **1-3（美术馆）：** 大量留白，区块间距巨大（`py-32` 到 `py-48`）。贵气、干净。
* **4-7（日常应用）：** 标准 Web 应用间距（`py-16` 到 `py-24`）。
* **8-10（驾驶舱）：** 紧凑内边距，不用卡片盒，数据间用 1px 细线分隔。强制：所有数字用 `font-mono`。

---

## 8. 暗色模式协议

默认双模式。除非简报是模拟印刷的编辑类页面，绝不默认只做浅色。

### 8.A Token 策略（选定一种，贯彻到底）
* **Tailwind `dark:` 变体**（utility-first 项目的默认）：每个颜色工具类都配好暗色变体（`bg-white dark:bg-zinc-950`、`text-gray-900 dark:text-gray-100`）。
* **CSS 变量**（用于 shadcn/ui、Radix Themes 或带主题化的组件库）：定义语义 token（`--surface`、`--surface-elevated`、`--text-primary`、`--accent`），在 `[data-theme="dark"]` 或 `@media (prefers-color-scheme: dark)` 下切换取值。

### 8.B 此处不规定具体颜色
由简报和品牌决定。本技能只强制以下几点：
* **对比度** - 正文至少 WCAG AA，hero 文案以 AAA 为目标。
* **层级对等** - 浅色下成立的视觉层级，深色下同样要成立。CTA 在浅色下跳，深色下也要跳。
* **品牌忠实** - 主品牌色保持可识别，不要为了暗色模式把品牌色抹成灰。
* **不用纯 `#000000` 也不用纯 `#ffffff`** - 用近黑（zinc-950、暖调近黑灰）和近白。纯值会杀死层次感。

### 8.C 默认模式
尊重 `prefers-color-scheme`，除非品牌坚持。任一模式会丢失关键品牌表达时，加一个手动切换。

### 8.D 收尾前两种模式都要测
开发过程中两种模式都打开看过。只见过一种模式的页面不许交付。

---

## 9. AI 破绽（禁用模式）

除非简报明确要求，否则避开这些标志性特征。

### 9.A 视觉与 CSS
* **默认不用**霓虹 / 外发光，改用内边框或细微的着色阴影。
* **不用纯黑（`#000000`）**，用近黑、zinc-950 或炭色。
* **不用过饱和强调色**，降低饱和度以融入中性色。
* **大标题不搞过度的渐变文字。**
* **不用自定义鼠标指针。** 过时、对无障碍有害、对性能有害。

### 9.B 字体排印
* **避免 Inter 作默认。** 见第 4.1 节，存在例外路径。
* **不用只会喊叫的超大 H1**，用字重 + 颜色控制层级，而不是堆字号。
* **衬线限制：** 衬线用于编辑类 / 奢侈 / 出版物场景，不用于仪表盘。

### 9.C 布局与间距
* **数学般精确**的内边距和外边距，不留元素悬浮、间距尴尬的死角。
* **不用三列等宽功能卡。** 「三张一模一样的卡片横排」这种功能行已被禁止。改用双栏 zigzag、非对称网格、滚动钉住或横向滚动替代。

### 9.D 内容与数据（“Jane Doe” 效应）
* **不用通用名字。** "John Doe"、"Sarah Chan"、"Jack Su" 这类一律不要，用有创意、真实、符合地域的名字。
* **不用通用头像。** 不要 SVG「蛋形」或 Lucide 用户图标，用可信的照片占位或定制样式。
* **不用假完美的数字。** 避免 `99.99%`、`50%`、`1234567`，用自然、带毛边的数据（`47.2%`、`+1 (312) 847-1928`）。
* **不用创业垃圾风品牌名。** "Acme"、"Nexus"、"SmartFlow"、"Cloudly" 之类不要，要编出贴合语境、听感真实的高级名字。
* **不用填充式动词。** "Elevate"、"Seamless"、"Unleash"、"Next-Gen"、"Revolutionize" 一律不要，只许具体的动词。

### 9.E 外部资源与组件
* **不手写 SVG 图标。** 用 Phosphor / HugeIcons / Radix / Tabler，Lucide 仅在明确要求时用。
* **手绘装饰 SVG 强烈不推荐**作默认（见第 4.8 节）。
* **不用 div 假截图。** 绝不用 `<div>` 矩形拼假产品 UI 来模拟截图，用真实图片、生成图片，或干脆不放预览。
* **不用失效的 Unsplash 链接。** 用 `https://picsum.photos/seed/{descriptive-string}/{w}/{h}`、生成的照片占位，或真实素材。
* **shadcn/ui 定制：** 允许，但**绝不**用默认形态。按项目审美定制圆角、颜色、阴影、字体。
* **生产级整洁：** 视觉上干净、令人过目难忘、经过细致打磨。

### 9.F 生产测试破绽（一律禁止）

这些模式来自真实的 LLM 生成落地页测试，是模型试图「装作有设计感」时的默认签名。除非简报点名要求，一律视为硬禁令。

**Hero 与页面顶部**
* **hero 里不放版本标签。** `V0.6`、`v2.0`、`BETA`、`INVITE-ONLY PREVIEW`、`EARLY ACCESS`、`ALPHA`，禁止作默认眉题。仅当简报明确是产品发布 / 预览状态时才可接受。
* **不用 "Brand · No. 01" 式的副眉题。** "Marrow · No. 01 · The 6-quart" 这类微元数据行，跳过。

**区块编号与微型标签**
* **不用区块编号眉题。** `00 / INDEX`、`001 · Capabilities`、`002 · Featured commission`、`06 · how it works`、`05 · The honest table`，禁止。眉题应该用平实语言点出主题，而不是编号计数。
* **图片和 bento 瓷砖上不放 `01 / 4` 式页码。** 用户自己会数，不需要标签。
* **不用 `Scroll · 001 Capabilities` 式滚动提示。** 一个简单箭头或 "Scroll" 就够了，不要带区块编号前缀。
* **不用 "Index of Work, 2018 - 2026" 式区间标签**作眉题。直接说这个区块是什么。

**分隔符与圆点**
* **中点（`·`）定量供应。** 元数据条里每行最多 1 个，**不要**拿它当万能分隔符（"foo · bar · baz · qux · quux"）。真需要分隔体系时，优先换行、发丝线或分栏。
* **列表 / 导航 / 徽章上不放装饰性彩色状态点。** "ONE Q4 SLOT OPEN" 前面的彩点、每个导航链接前的彩点、每个任务行前的彩点，默认禁止。仅当圆点传达真实语义状态（服务器状态、可约标记）且用得节制时才可接受。

**Em-dash 与排印花活**
* **em-dash（`—`）不作设计元素，也不出现在任何地方。** 完整的、不容商量的禁令见下方第 9.G 节。标题、眉题、药丸、正文、引文、署名、图注、按钮文字、alt 文本中一律禁止 em-dash 字符，用普通连字符（`-`）。
* **不用 `<br>` 切断再加斜体的标题**当默认「设计手法」。"for thirty\<br\>*years.*" 这类切分。标题首先要读得自然，简报有要求时才玩花。
* **不用竖排旋转文字**（把 "INDEX OF WORK, 2018 - 2026" 转 90°）。代理公司作品集的老掉牙手法。仅当简报明确是代理 / Awwwards / 实验风，且确实服务于构图时才用。
* **不用十字线 / 发丝网格线做装饰。** 只为让页面「显得有设计」而画的横竖线条，禁止。只有组织真实内容时才用。

**假产品预览**
* **hero 里不放 div 假产品 UI**（样式化 div 拼的假任务列表、假终端、假仪表盘）。这是头号 LLM 设计破绽。用真实截图、生成图片、真实组件预览，或什么都不放。
* **假截图里不放假版本页脚**（"v0.6.2-rc.1"、"last sync 4s ago · main"）。毫无信息量，一眼 AI。

**营销文案破绽**
* **不用 "Quietly in use at" / "Quietly trusted by" 式社会证明标题。** 用自然语言："Trusted by"、"Used at"、"Customers include"，或者 logo 本身会说话时干脆不要标题。
* **引言、博客或侧栏区块不用 "From the field" / "Field notes" / "Currently on the bench" / "On our desks" / "Loose plates" 式诗意标签。** 那是在表演匠人感。用平实的功能性标签（"Testimonials"、"Latest writing"、"Now working on"），或不加标签。
* **正文里不玩 "We respect the French ones" 式的假谦虚行业梗。** 自以为可爱，满口 AI 味。
* **页眉页脚不放天气 / 地域信息条**（"LIS 14:23 · 18°C"），除非简报明确围绕某个地点 / 跨时区分布式工作室。
* **眉题下不放微型元叙述句。** 区块标题下面挂 *"Each of these is a feature we ship today, not a roadmap promise. The list will stay short on purpose."* 这种句子纯属杂讯。眉题 + 标题 + 正文，足够了。
* **不用通用步骤标签。** "Stage 1 / Stage 2 / Stage 3"、"Step 1 / Step 2 / Step 3"、"Phase 01 / Phase 02 / Phase 03"、"Pass One / Pass Two / Pass Three"，一律禁止。步骤内容本身就是标签。真要体现递进，直接用动词或名词（"Install"、"Configure"、"Ship"），不要 "Stage 1: Install"。

**药丸、标签与版本戳**
* **图片上不叠药丸 / 标签 / 徽标。** 照片上不要压 `<span>` 标签（如 `Brand · 02`、`PLATE · BRAND`、`Field notes - journal`）。要么让图片自己说话，要么在图片正下方（图片之外）加图注。
* **不用装饰性摄影署名图注。** 图库 / picsum 图片下面挂 `Field study no. 12 · Ines Caetano`、`Plate 03 · House archive`、`Frame XII · 35mm` 这种字符串，矫饰。摄影署名**只**在真实摄影师授权的真实照片上使用。否则：要么不要图注，要么用一行功能性说明（"The 6-quart, in Sage."）。
* **营销页不放版本页脚。** `v1.4.2`、`Build 0048`、`last sync 4s ago · main` 这类页脚字符串是 CLI / 开发者工具的配件，不是落地页内容。营销 / 落地 / 作品集页面一律禁止。
* **不用 "Reservation 412 of 800" 式实时库存计数器**做装饰。仅当简报明确是带真实数据的限量等候名单时才用。

**装饰性文字条**
* **hero 底部不放装饰性文字条。** `BRAND. MOTION. SPATIAL.`、`TYPE / FORM / MOTION`、`DESIGN · BUILD · SHIP`、`ESTD. 2018 · LISBON · BRAND. MOTION. SPATIAL.` 这类小号等宽大写横条压在 hero 底部，是代理公司作品集的老套。默认禁止。仅当横条承载真实可点的链接（sticky 底部导航）或真实状态信息（cookie 横幅、文档站的构建信息）时才可接受。
* **区块标题右上角不放悬浮小字。** 模式是：区块有个巨大的左对齐标题，同一区块头部右上角悬着一小段解释文字，与任何东西都对不齐。这个悬浮物就是破绽。要么把小字直接放在标题下面，要么做干净的双栏头部（左标题、右对齐正文），不要角落小段落。

**列表、分隔线与打分条**
* **长列表 / 规格表不要每行同时挂 `border-t` + `border-b`。** 二选一（行间下边线，或组上方上边线），且用得稀疏。10 行规格表行行加发丝线是最偷懒的布局，替代 UI 组件见第 4.9 节。
* **对比可视化不用带填充背景轨道的打分 / 进度条。** 要表达「Y 中的 X」式对比时，优先用数字 + 小图标，或没有背景轨道的微型内联条。`bg-zinc-200` 的大填充轨道上面再盖一层部分填充，放在落地页上就是仪表盘 UI 垃圾。

**地域、时间与滚动提示**
* **地域 / 城市名 / 时间 / 天气信息条，99% 的简报都禁止。** hero 里的 "Lisbon, working with founders"、页脚里的 "1200-690 Lisbon, Portugal"、导航里的 "Lisbon 14:23 · 18°C"，都是代理作品集的装饰破绽。**只**在以下情况允许：简报明确描述跨时区协作的分布式工作室、以旅行为主题的品牌，或有真实线下实体场所。页脚提一个联系地址没问题，气氛组地域信息条不行。
* **滚动提示禁止。** `Scroll`、`↓ scroll`、`Scroll to explore`、`Scroll to walk through it`、滚轮动画图标。用户还没滚动时看到的就是 hero，他们知道什么是滚动。视口底部不需要标签。
* **装饰性状态点默认为零。** 导航项前、列表行前、徽章前、状态标签前的彩点都是破绽。仅当传达真实语义状态（真实服务器状态的 live 指示、实时可约标记）且每个页面区块限一个时才可接受。

### 9.G EM-DASH 禁令（违反率最高的破绽，没有之一）

**em-dash（`—`）全面禁止。** 它是 LLM 标志性的风格拐杖，也是生产测试中的头号视觉破绽。没有「限量使用」的豁免，没有「符合自然语言频率」的豁免，没有「正文里用用没事」的豁免。一个都没有。

* **标题中禁止。** 用句号或逗号。
* **眉题 / 标签 / 药丸 / 按钮文字 / 图注 / 导航项中禁止。** 用换行、分栏或发丝线替代。
* **正文中禁止。** 重构句子：拆成句号隔开的两句，或用逗号、括号、冒号。
* **引文署名中禁止。** 用带空格的普通连字符（` - `），或换行 + 更轻字重的名字。
* **作分隔符用的 en-dash（`–`）同样禁止。** 日期区间（`2018-2026`）用连字符，数字区间（`€40-80k`）用连字符。

页面中唯一允许的横线字符是：
* 普通连字符 `-`（复合词、区间、标记中的行分隔）
* 数学中的负号（`-5°C`）

产出中只要在用户可见处出现一个 `—` 或 `–`，即未通过 Pre-Flight 检查，必须重写。

这条规则不容商量。经验表明，写成「少用一点」时 agent 总会无视 em-dash 限制。这里的表述是二值的：em-dash 数量为零。

---

## 10. 参考词汇表（agent 应当认识的模式名）

这是词汇表，不是组件库。agent 应当**认识**这些模式名，以便围绕它们交流、带着它们做设计，并在设计判读需要时取用。**实现与代码草稿放在 Block Library（第 12 节），逐步充实。**

### Hero 范式
* **Asymmetric Split Hero（非对称分栏 hero）** - 一侧文字，一侧素材，留白慷慨。
* **Editorial Manifesto Hero（编辑宣言式 hero）** - 大字排印，无素材，近乎海报。
* **Video / Media Mask Hero（视频遮罩 hero）** - 文字作为遮罩镂空，叠在视频背景上。
* **Kinetic-Type Hero（动态字体 hero）** - 以动画字体排印作为主视觉。
* **Curtain-Reveal Hero（幕布揭示 hero）** - 随滚动像幕布一样分开。
* **Scroll-Pinned Hero（滚动钉住 hero）** - hero 钉在原地，内容从背后滚过。

### 导航与菜单
* **Mac OS Dock Magnification（Dock 放大导航）** - 屏幕边缘导航，图标悬停时流畅缩放。
* **Magnetic Button（磁吸按钮）** - 向光标方向吸附。
* **Gooey Menu（黏液菜单）** - 子项像黏稠液体一样分离。
* **Dynamic Island（灵动岛）** - 形变的药丸，承载状态 / 提醒。
* **Contextual Radial Menu（上下文环形菜单）** - 在点击处展开的环形菜单。
* **Floating Speed Dial（浮动快捷拨盘）** - FAB 弹出弧形排列的次级操作。
* **Mega Menu Reveal（大型菜单展开）** - 全屏下拉，内容交错淡入。

### 布局与网格
* **Bento Grid（便当格网格）** - 非对称瓷砖组合（Apple 控制中心）。
* **Masonry Layout（瀑布流布局）** - 错落网格，行高不定。
* **Chroma Grid（色变网格）** - 带细微渐变动画的边框 / 瓷砖。
* **Split-Screen Scroll（分屏滚动）** - 两半向相反方向滑动。
* **Sticky-Stack Sections（钉住堆叠区块）** - 滚动时钉住并层层堆叠的区块。

### 卡片与容器
* **Parallax Tilt Card（视差倾斜卡）** - 跟踪鼠标坐标的 3D 倾斜。
* **Spotlight Border Card（聚光边框卡）** - 边框在光标处点亮。
* **Glassmorphism Panel（毛玻璃面板）** - 带内部折射的磨砂玻璃。
* **Holographic Foil Card（全息箔卡）** - 悬停时虹彩偏移。
* **Tinder Swipe Stack（滑动卡组）** - 物理卡堆，可滑走。
* **Morphing Modal（形变弹窗）** - 按钮展开成为它自己的对话框。

### 滚动动画
* **Sticky Scroll Stack（粘性滚动堆叠）** - 卡片粘住并物理堆叠。
* **Horizontal Scroll Hijack（横向滚动劫持）** - 纵向滚动 → 横向平移。
* **Locomotive / Sequence Scroll（序列滚动）** - 视频 / 3D 序列与滚动条绑定。
* **Zoom Parallax（缩放视差）** - 中央背景图随滚动缩放。
* **Scroll Progress Path（滚动进度路径）** - SVG 线条随滚动绘制。
* **Liquid Swipe Transition（液体切换）** - 像黏稠液体一样的页面转场。

### 画廊与媒体
* **Dome Gallery（穹顶画廊）** - 3D 全景画廊。
* **Coverflow Carousel（Coverflow 轮播）** - 边缘呈角度的 3D 轮播。
* **Drag-to-Pan Grid（拖拽平移网格）** - 无边界的可拖拽画布。
* **Accordion Image Slider（手风琴图片滑块）** - 窄条悬停时展开。
* **Hover Image Trail（悬停图片尾迹）** - 鼠标划过时弹出图片尾迹。
* **Glitch Effect Image（故障效果图）** - 悬停时 RGB 通道错位。

### 字体排印与文字
* **Kinetic Marquee（动态 marquee）** - 无限文字带，随滚动反向。
* **Text Mask Reveal（文字遮罩揭示）** - 巨型文字成为透出视频的窗口。
* **Text Scramble Effect（文字乱码效果）** - 加载 / 悬停时黑客帝国式解码。
* **Circular Text Path（环形文字路径）** - 文字沿旋转的圆排布。
* **Gradient Stroke Animation（渐变描边动画）** - 描边文字上流动的渐变。
* **Kinetic Typography Grid（动态字体网格）** - 字母躲闪光标。

### 微交互与效果
* **Particle Explosion Button（粒子爆炸按钮）** - 成功时 CTA 碎成粒子。
* **Liquid Pull-to-Refresh（液态下拉刷新）** - 刷新指示像液滴脱落。
* **Skeleton Shimmer（骨架微光）** - 光泽扫过占位骨架。
* **Directional Hover-Aware Button（方向感知悬停按钮）** - 填充从光标进入的一侧涌入。
* **Ripple Click Effect（涟漪点击效果）** - 波纹从点击坐标扩散。
* **Animated SVG Line Drawing（SVG 线条动画）** - 矢量图形实时自我绘制。
* **Mesh Gradient Background（mesh 渐变背景）** - 有机熔岩灯色块。
* **Lens Blur Depth（镜头虚化景深）** - 虚化背景 UI，聚焦前景操作。

### 动画库选择
* **Motion（`motion/react`）** - UI / Bento / 状态变化动效的默认选择。
* **GSAP + ScrollTrigger** - 用于整页 scrolltelling 和滚动劫持，隔离在专用叶子组件里并做 `useEffect` 清理。
* **Three.js / WebGL** - 用于 canvas 背景和 3D 场景，同样遵守隔离规则。
* **绝不把 GSAP / Three.js 和 Motion 混在同一棵组件树里。** 它们会争抢同一些帧。

---

## 11. 重设计协议

本技能同时处理**全新构建（greenfield）和重设计**。模式判断错误是重设计产出糟糕的最大单一来源。

### 11.A 判断模式（第一个动作）
* **Greenfield（全新）** - 没有既有站点，或已批准彻底推翻。旋钮取第 1 节的基线。
* **重设计 - 保留** - 在不破坏品牌的前提下现代化。先审计，提取品牌 token，渐进演化。
* **重设计 - 推翻** - 在既有内容之上建立新视觉语言。视觉上按 greenfield 处理，内容和 IA（信息架构）保留。

拿不准时**只问一次**：*「这次重设计要保留既有品牌，还是视觉上从零开始？」*

### 11.B 动手前先审计
提出改动之前，先记录现状：
* **品牌 token** - 主色 / 强调色、字体 stack、logo 处理方式、圆角。
* **信息架构** - 页面树、主导航、关键转化路径。
* **内容区块** - 有什么、哪些在发挥作用、哪些是凑数。
* **要保留的模式** - 标志性交互、有辨识度的 hero、文案声音。
* **要淘汰的模式** - AI 味破绽、坏布局、死链、通用图库图、性能陷阱。
* **既有站点的旋钮读数** - 推断当前的 `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY`。这是你的起点，不是基线。
* **SEO 基线** - 当前有排名的页面、meta 标题、结构化数据、OG 卡片。**SEO 迁移是重设计的第一大风险。**

### 11.C 保留规则
* 未经要求**不要改动信息架构**。页面 slug、锚点 ID、主导航标签保持稳定，既为 SEO 也为用户的肌肉记忆。
* **应用第 4.2 节前先提取品牌色。** 本就偏紫的品牌继续紫，走反紫规则（THE LILA RULE）的例外路径。
* **保留文案声音**，除非被要求重写。视觉现代化 ≠ 内容重写。
* **尊重既有的无障碍成果。** focus 状态、alt 文本、键盘导航、对比度不许回退。
* **尊重既有埋点事件。** 下游追踪依赖的按钮、表单字段、区块 ID 不要改名。

### 11.D 现代化杠杆（按优先级）
按顺序应用，简报要求满足即停：
1. **字体翻新** - 单位风险的视觉提升最大。
2. **间距与节奏** - 加大区块内边距，修正纵向节奏。
3. **色彩重校准** - 降饱和、统一中性色、保留品牌强调色。
4. **动效层** - 给既有组件加上与 `MOTION_INTENSITY` 匹配的微交互。
5. **Hero 与关键区块重组** - 用第 10 节的词汇重构漏斗顶部。
6. **整块替换** - 仅当既有区块无药可救时。

### 11.E 决策树：定点演化还是全面重设计
* IA、内容和 SEO 健康 → **定点演化**（杠杆 1-4），以约四成的风险拿到约七成的价值。
* 视觉欠债是结构性的（IA 混乱、没有设计系统、移动端坏掉）→ **全面重设计**，内容严格保留。
* 品牌本身在变 → **greenfield（全新）**。

### 11.F 绝不允许静默更改的内容
未经用户明确批准，绝不修改：
* URL 结构 / 路由 slug。
* 主导航标签。
* 表单字段名或顺序（会破坏埋点和自动填充）。
* 品牌 logo 或字标。
* 既有的法律 / 同意 / cookie 文案。

---

## 12. BLOCK LIBRARY（契约 - 实现逐步落地于此）

参考词汇表（第 10 节）给模式命名，Block Library 用真实的 props、真实的动效规格和真实的代码草稿实现它们。

**状态：** 此处定义 schema。区块会逐步加入。不要脱离这个 schema 自由发挥新区块。

### 12.A 文件位置
```
skills/taste-skill/blocks/
  hero/
    asymmetric-split.md
    editorial-manifesto.md
    kinetic-type.md
    ...
  feature/
    bento-grid.md
    sticky-scroll-stack.md
    zig-zag.md
    ...
  social-proof/
  pricing/
  cta/
  footer/
  navigation/
  portfolio/
  transition/
```

### 12.B 必需的 Frontmatter
```yaml
---
name: asymmetric-split-hero
category: hero
dial_compatibility:
  variance: [6, 10]
  motion: [3, 10]
  density: [2, 5]
when_to_use: "Landing pages with one strong asset and one strong message. Default hero for SaaS, agency, premium consumer."
not_for: "Editorial / manifesto launches where the message IS the design."
stack: ["react", "next", "tailwind", "motion"]
---
```

### 12.C 必需的正文小节
1. **视觉草图** - 布局的简短 ASCII 图或文字描述。
2. **Props API** - 组件的接口。
3. **代码草稿** - 最小可用实现（默认 Server Component，动效用 Client 岛）。
4. **移动端回退** - `< 768px` 的显式折叠规则。
5. **动效变体** - 每个 `MOTION_INTENSITY` 区段（1-3、4-7、8-10）各一个变体，reduced-motion 回退显式写出。
6. **暗色模式说明** - 该区块专属的 token 策略。
7. **反模式** - 这个区块常见的翻车方式。
8. **参考** - 指向生产环境真实案例的链接。

### 12.D Block Library 纪律
* 一个文件一个区块，不做多区块文件。
* 每个区块必须可独立工作（放进页面即可渲染）。
* 每个区块必须通过 Pre-Flight 检查（第 14 节）。
* 依赖第 2.A 节设计系统的区块放在 `blocks/<category>/<name>--<system>.md` 下（如 `feature/bento-grid--material.md`）。

---

## 13. 适用范围之外

本技能**不**适用于：
* 仪表盘 / 高密度产品 UI / 管理后台（用第 2.A 节的 Fluent、Carbon、Atlassian 或 Polaris）。
* 数据表格（用 TanStack Table 或 AG Grid）。
* 多步骤表单 / 向导（用表单专属模式，本技能帮不上忙）。
* 代码编辑器（用 Monaco / CodeMirror 及其官方换肤）。
* 原生移动端（直接用 Apple HIG / Material）。
* 实时协作 UI（presence、光标、OT 感知，属于另一类问题）。

简报属于以上情形时，**明确说出来**，指给用户正确的工具，只把本技能的营销页 / 关于页 / 落地页部分用在它们适用的表面上。

---

## 14. 最终 Pre-Flight 检查

输出代码前跑完这张清单。这是最后一道过滤器。

**这不是可选项。每一项都要过。任何一项不过，产出就没完成。**

- [ ] **简报推断**已声明（第 0.B 节的一句话判读）？
- [ ] **旋钮取值**显式给出、有简报依据，而不是悄悄沿用基线？
- [ ] 适用时**设计系统**已从第 2 节选取，或审美取向已诚实标注？
- [ ] **重设计模式**已判定并完成审计（如适用，第 11 节）？
- [ ] **页面任何地方 em-dash（`—`）数量为零。** 标题、眉题、药丸、正文、引文、署名、图注、按钮、alt 文本。零。（第 9.G 节，不容商量。）
- [ ] **页面主题锁**：整页一个主题（light、dark 或 auto），没有区块中途反转（第 4.11 节）？
- [ ] **色彩一致性锁**：一个强调色贯穿所有区块、用法一致（第 4.2 节）？
- [ ] **形状一致性锁**：一套圆角体系贯彻全页（第 4.4 节）？
- [ ] **按钮对比度检查**：每个 CTA 文字在其背景上可读（不许白底白字，WCAG AA 4.5:1）？
- [ ] **CTA 按钮换行**：桌面端没有 CTA 标签折成 2 行以上？
- [ ] **表单对比度检查**：输入框、占位符、focus 环、标签相对区块背景都达到 WCAG AA？
- [ ] **衬线纪律**：如用衬线，不是 Fraunces 或 Instrument_Serif（若是，须有明确的品牌理由）？与上一个项目用的衬线不同？
- [ ] **高端消费调色板检查**：简报属高端消费（锅具 / 康养 / 手作 / 奢侈）时，配色不是 AI 默认的米色 + 黄铜 + 牛血红 + 浓缩咖啡系？与上一个高端消费项目的色系不同？
- [ ] **斜体下降部留空**：含 `y g j p q` 的每个斜体词都有 `leading-[1.1]` 下限 + `pb-1` 预留？
- [ ] **Hero 装进视口**：标题 ≤ 2 行，副文案 ≤ 20 词且 ≤ 4 行，CTA 不滚动可见，字号围绕图片规划？
- [ ] **Hero 顶部内边距**：桌面端最大 `pt-24`，hero 内容没有悬在视口半腰？
- [ ] **Hero 元素堆叠纪律**：hero 文字元素最多 4 个（眉题或品牌条、标题、副文案、CTA）？CTA 下没有小标语，hero 里没有信任微型条？
- [ ] **眉题计数（机械检查）**：数所有组件里区块标题上方 `uppercase tracking` 微标签的实例数。数量 ≤ ceil(sectionCount / 3)？hero 算 1。
- [ ] **分栏标题禁令**：区块头部没有「左大标题 + 右小解释段落」模式（改为纵向堆叠）？
- [ ] **Z 字交替上限**：没有 3 个以上连续区块使用同一种图文分栏布局？
- [ ] **CTA 意图不重复**：没有两个意图相同的 CTA（"Get in touch" + "Let's talk" 同时在页 = 不通过）？
- [ ] **Logo 墙 = 只有 logo**：logo 下面没印行业 / 品类标签？
- [ ] **Bento 背景多样性**：至少 2-3 格有真实视觉变化（图片、渐变、图案），不是清一色白底文字卡？
- [ ] **"Used by / Trusted by" logo 墙**位于 hero 之下而非其中，用真实 SVG logo（Simple Icons / devicon）或生成的 SVG 标志，而非纯文字字标？
- [ ] **文案自查**：每条可见字符串重读过，没有语法破碎或 AI 幻觉式短语（"free on its past" 之类）流出？
- [ ] **动效有动机**：每个动画都能用一句话说清理由（层级 / 叙事 / 反馈 / 状态切换），没有为秀而秀的 GSAP？
- [ ] **每页 marquee 至多一个**：同一页没有两个横向 marquee？
- [ ] **导航桌面端单行**，高度 ≤ 80px？
- [ ] **区块布局重复**检查：没有两个区块共用同一布局族（8 个区块至少 4 种不同布局族）？
- [ ] **Bento 有节奏且格数精确**（N 个条目 → N 格，中部和末尾没有空格）？
- [ ] **长列表用对了 UI 组件**（超过 5 项不用默认 `<ul>` + `divide-y`，替代方案见第 4.9 节）？
- [ ] **用了真实图片**（先生成工具，再 Picsum seed，再显式占位槽）- 没有 div 假截图、没有手绘装饰 SVG、没有纯文字极简？
- [ ] **图片上没叠药丸 / 标签**（没有 `Plate · Brand`，没有 `Field notes - journal`）？
- [ ] **没有装饰性摄影署名图注**（`Field study no. 12 · Ines Caetano`）？
- [ ] **营销页没有版本页脚**（`v1.4.2`、`Build 0048`）？
- [ ] **眉题下没有微型元叙述句**（"Each of these is a feature we ship today..."）？
- [ ] **hero 底部没有装饰性文字条**（`BRAND. MOTION. SPATIAL.`）？
- [ ] **区块标题右上角没有悬浮小字**？
- [ ] **对比可视化没有用带填充背景轨道的打分 / 进度条**？
- [ ] **没有地域 / 城市名 / 时间 / 天气信息条**（除非简报确实是分布式团队或以地点为核心）？
- [ ] **没有滚动提示**（`Scroll`、`↓ scroll`、`Scroll to explore`）？
- [ ] **hero 里没有版本标签**（V0.6、BETA、INVITE-ONLY），除非简报就是发布？
- [ ] **没有区块编号眉题**（`00 / INDEX`、`001 · Capabilities`、`06 · how it works`）？
- [ ] **没有装饰性圆点**（默认为零，仅用于真实语义状态）？
- [ ] **长列表 / 规格表没有每行同时挂 `border-t` + `border-b`**？
- [ ] **内容密度**正常：没有 20 行数据表，没有无端假精确的规格，副段落默认 ≤ 25 词？
- [ ] **引言正文 ≤ 3 行**，署名干净（无 em-dash）？
- [ ] **宣称动效 = 看得到动效**：`MOTION_INTENSITY > 4` 时页面真的在动，而不只是嘴上说说？
- [ ] **GSAP sticky-stack / horizontal-pan** 按第 5.A / 5.B 节规范骨架实现（`start: "top top"`、`pin: true`、scrub 正确）？
- [ ] **没用 `window.addEventListener('scroll')`** - 只用 Motion `useScroll()` / ScrollTrigger / IntersectionObserver / CSS scroll-driven animations？
- [ ] **减弱动态处理**：`MOTION_INTENSITY > 3` 的一切都做了包裹？
- [ ] **暗色模式** token 已定义，两种模式都测过？
- [ ] 高方差布局的**移动端折叠**显式声明（`w-full`、`px-4`、`max-w-7xl mx-auto`）？
- [ ] **视口稳定**：用 `min-h-[100dvh]`，绝不用 `h-screen`？
- [ ] **`useEffect` 动画**有严格的清理函数？
- [ ] **空 / 加载 / 错误**状态都齐了？
- [ ] 能用间距的地方**省掉了卡片**？
- [ ] **图标**只来自许可库（Phosphor / HugeIcons / Radix / Tabler），没有手绘 SVG 路径？
- [ ] **Motion** 隔离在带 `'use client'` 头部的 client 叶子组件里，并做了 memo？
- [ ] 没有第 9 节的 **AI 破绽**（Inter 作默认、AI 紫、三张等宽卡、Jane Doe、Acme、"Quietly in use at"）？
- [ ] **Core Web Vitals** 大概率达标（LCP < 2.5s、INP < 200ms、CLS < 0.1）？
- [ ] **一个项目一套设计系统**（没有 Material + shadcn 混用）？

任何一项无法诚实打勾，页面就没完成。修好再交付。

---

# 附录 - 有真实出处的参考资料

以下小节是引入的参考资料，为第 2 节点名的每个设计系统提供真实的安装命令、权威文档链接和可运行的起步片段。用它们让决策扎根于生产现实，而不是训练数据里的幻想。

## 附录 A - 各设计系统的安装命令

```bash
# Material Web (Material 3)
npm install @material/web

# Fluent UI React (v9)
npm install @fluentui/react-components

# Fluent UI Web Components (framework-free)
npm install @fluentui/web-components @fluentui/tokens

# IBM Carbon
npm install @carbon/react @carbon/styles

# Radix Themes
npm install @radix-ui/themes

# shadcn/ui (open code, owned components)
npx shadcn@latest init
npx shadcn@latest add button card badge separator input

# Primer CSS (GitHub product/devtool UI)
npm install --save @primer/css

# Primer Brand (GitHub marketing UI)
npm install @primer/react-brand

# GOV.UK Frontend
npm install govuk-frontend

# USWDS (US Web Design System)
npm install uswds

# Atlassian Design System (Atlaskit)
yarn add @atlaskit/css-reset @atlaskit/tokens @atlaskit/button @atlaskit/badge @atlaskit/section-message @atlaskit/card

# Bootstrap 5.3
npm install bootstrap

# Shopify Polaris Web Components (Shopify apps only)
# Add this to your app HTML head:
#   <meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />
#   <script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>
```

## 附录 B - 权威来源（重新造轮子之前先读这些）

### Material Web
- https://github.com/material-components/material-web
- https://material-web.dev/theming/material-theming/
- https://m3.material.io/develop/web

### Fluent UI
- https://fluent2.microsoft.design/get-started/develop
- https://fluent2.microsoft.design/components/web/react/
- https://github.com/microsoft/fluentui
- https://learn.microsoft.com/en-us/fluent-ui/web-components/

### Carbon
- https://carbondesignsystem.com/
- https://github.com/carbon-design-system/carbon
- https://carbondesignsystem.com/developing/react-tutorial/overview/
- https://carbondesignsystem.com/developing/web-components-tutorial/overview/

### Shopify Polaris
- https://shopify.dev/docs/api/app-home/web-components
- https://github.com/Shopify/polaris-react
- https://polaris-react.shopify.com/components

### Atlassian
- https://atlassian.design/get-started/develop
- https://atlassian.design/components/button/examples
- https://atlaskit.atlassian.com/packages/design-system/button/example/disabled
- https://atlassian.design/tokens/design-tokens

### Primer
- https://primer.style/
- https://github.com/primer/css
- https://github.com/primer/brand

### GOV.UK
- https://design-system.service.gov.uk/components/button/
- https://design-system.service.gov.uk/styles/layout/
- https://github.com/alphagov/govuk-frontend

### USWDS
- https://designsystem.digital.gov/documentation/developers/
- https://designsystem.digital.gov/components/button/
- https://designsystem.digital.gov/components/card/
- https://github.com/uswds/uswds

### Bootstrap
- https://getbootstrap.com/docs/5.3/layout/grid/
- https://getbootstrap.com/docs/5.3/components/card/

### Tailwind
- https://tailwindcss.com/docs/dark-mode
- https://tailwindcss.com/blog/tailwindcss-v4

### Radix
- https://www.radix-ui.com/themes/docs/components/theme
- https://www.radix-ui.com/themes/docs/components/card
- https://github.com/radix-ui/themes

### shadcn/ui
- https://ui.shadcn.com/docs
- https://ui.shadcn.com/docs/components/card
- https://github.com/shadcn-ui/ui

### 原生 CSS / W3C 标准
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
- https://drafts.csswg.org/scroll-animations-1/

### Apple Liquid Glass（仅 Apple 平台）
- https://developer.apple.com/design/human-interface-guidelines/materials
- https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass
- https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass
- https://developer.apple.com/documentation/SwiftUI/Material

---

## 附录 C - Apple Liquid Glass：诚实的 Web 近似

**不要**把随手找来的 CSS 片段当成官方 Apple Liquid Glass。

### 官方的是什么
Apple 在其人机界面指南（Human Interface Guidelines）和开发者文档中为 **Apple 平台**提供了 Liquid Glass 的说明。它是一种贯穿 Apple 平台 UI 的动态材质。Apple 的原生实现属于 Apple 平台 API 和系统组件，**不是公开的 Web CSS 包**。

相关官方文档：
- Apple Human Interface Guidelines → Materials
- Apple Developer Documentation → Liquid Glass
- Apple Developer Documentation → Adopting Liquid Glass
- SwiftUI → Material

### 非官方的是什么
Apple 没有为普通网站提供任何 `liquid-glass.css`。

Web 近似方案可以用：
- `backdrop-filter`
- 透明背景
- 分层边框
- 高光叠加
- 渐变
- 动效
- 强对比回退

但那是 **Web glassmorphism / 毛玻璃近似**，不是官方 Apple Liquid Glass，注释里要如实标注。

### 更稳妥的 Web 近似骨架

```css
.liquid-glass-web-approx {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  border-radius: 999px;
  border: 1px solid rgb(255 255 255 / .32);
  background:
    linear-gradient(135deg, rgb(255 255 255 / .30), rgb(255 255 255 / .08)),
    rgb(255 255 255 / .12);
  backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  -webkit-backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / .48),
    inset 0 -1px 0 rgb(255 255 255 / .12),
    0 18px 60px rgb(0 0 0 / .18);
}

.liquid-glass-web-approx::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background:
    radial-gradient(circle at 20% 0%, rgb(255 255 255 / .55), transparent 34%),
    linear-gradient(90deg, rgb(255 255 255 / .18), transparent 42%, rgb(255 255 255 / .14));
  pointer-events: none;
}

.liquid-glass-web-approx::after {
  content: "";
  position: absolute;
  inset: 1px;
  border-radius: inherit;
  border: 1px solid rgb(255 255 255 / .14);
  pointer-events: none;
}

@media (prefers-color-scheme: dark) {
  .liquid-glass-web-approx {
    border-color: rgb(255 255 255 / .18);
    background:
      linear-gradient(135deg, rgb(255 255 255 / .16), rgb(255 255 255 / .04)),
      rgb(15 23 42 / .42);
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / .22),
      0 18px 60px rgb(0 0 0 / .42);
  }
}

@media (prefers-reduced-transparency: reduce) {
  .liquid-glass-web-approx {
    background: rgb(255 255 255 / .96);
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
}
```

**重要：** `prefers-reduced-transparency` 的浏览器支持参差不齐，要实测。即使没有模糊，也始终保证足够的对比度。

---

**附录完。** 上面的安装命令是现实锚点。Apple Liquid Glass 骨架是已明确标注的近似方案，不是 Apple 发布的包。各设计系统的权威文档请查阅其官方文档（链接见第 2 节与附录 B）。
