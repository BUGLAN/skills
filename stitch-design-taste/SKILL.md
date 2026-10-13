---
name: stitch-design-taste
description: 面向 Google Stitch 的语义化设计系统技能。生成对 agent 友好的 DESIGN.md 文件，强制执行高端、反套路的 UI 标准——严谨的排版、校准过的配色、非对称布局、永续微动效，以及硬件加速性能。
---

# Stitch Design Taste — 语义化设计系统技能

## 概述
本技能生成专为 Google Stitch 屏幕生成优化过的 `DESIGN.md` 文件。它把久经考验的「反 AI 味」（anti-slop）前端工程规范，转写成 Stitch 原生的语义化设计语言——用描述性的自然语言规则搭配精确数值，让 Stitch 的 AI agent 能据此产出高端、不落俗套的界面。

生成的 `DESIGN.md` 是提示 Stitch 生成新屏幕的**唯一事实来源（single source of truth）**，确保产出对齐一套精心甄选、气场十足的设计语言。Stitch 通过**「视觉描述（Visual Descriptions）」**理解设计，并以具体的色值、排版规格与组件行为作为支撑。

## 前置条件
- 可通过 [labs.google/stitch](https://labs.google/stitch) 访问 Google Stitch
- 可选：Stitch MCP Server，用于与 Cursor、Antigravity 或 Gemini CLI 做程序化集成

## 目标
生成一份 `DESIGN.md` 文件，把以下内容编码在内：
1. **视觉氛围**——情绪基调、密度与设计哲学
2. **色彩校准**——中性色、强调色与禁用模式，均附十六进制色值
3. **排版架构**——字体栈、字号层级与反面模式
4. **组件行为**——按钮、卡片、输入框及各自的交互状态
5. **布局原则**——网格体系、间距哲学与响应式策略
6. **动效哲学**——动画引擎规格、弹簧物理与永续微交互
7. **反面模式**——明令禁止的 AI 设计俗套清单

## 分析与提炼指引

### 1. 界定氛围
评估目标项目的定位，从品味光谱中选取有感染力的形容词：
- **密度：**「美术馆般疏朗」（1–3）→「日常应用般均衡」（4–7）→「驾驶舱般紧凑」（8–10）
- **变化度：**「可预测的对称」（1–3）→「错落的非对称」（4–7）→「艺术化的纷繁」（8–10）
- **动效：**「静态克制」（1–3）→「流畅的 CSS」（4–7）→「电影级编排」（8–10）

默认基线：变化度 8、动效 6、密度 4。再根据用户描述的气质基调动态调整。

### 2. 梳理调色板
每种颜色都要给出：**描述性名称** + **十六进制色值** + **功能角色**。

**强制约束：**
- 强调色至多 1 种，饱和度低于 80%
- 严禁「AI 紫蓝霓虹」审美——不要紫色按钮光晕，不要霓虹渐变
- 以绝对中性的底色（Zinc/Slate）为基础，搭配单一的高对比强调色
- 整套输出坚持同一套配色——暖灰、冷灰不得来回摇摆
- 绝不使用纯黑（`#000000`）——改用 Off-Black、Zinc-950 或 Charcoal

### 3. 确立排版规则
- **展示标题：**字距收紧、字号克制，不靠喊。层级靠字重与颜色区分，而非一味放大
- **正文：**行距舒展，每行不超过 65 字符
- **字体选择：**高端/创意场景禁用 `Inter`。强制选用有独特气质的字体：`Geist`、`Outfit`、`Cabinet Grotesk` 或 `Satoshi`
- **衬线禁令：**通用衬线体（`Times New Roman`、`Georgia`、`Garamond`、`Palatino`）一律禁用。编辑/创意场景确需衬线时，只可选用辨识度高的现代衬线体：`Fraunces`、`Gambarino`、`Editorial New` 或 `Instrument Serif`。仪表盘与软件 UI 中衬线体永远禁用
- **仪表盘约束：**只用无衬线字体组合（`Geist` + `Geist Mono` 或 `Satoshi` + `JetBrains Mono`）
- **高密度特例：**密度超过 7 时，所有数字必须使用等宽字体

### 4. 定义 Hero 区
Hero 区是第一印象，必须富有创意、足够抓人，绝不平庸：
- **行内图片排版：**在标题的词句或字母之间直接嵌入契合语境的小图。图片以文字高度行内排布、带圆角，充当视觉标点。这是标志性创意手法
- **禁止重叠：**文字绝不压在图片或其他文字上，每个元素各占一方整洁的空间
- **禁止填充文案：**「Scroll to explore」「Swipe down」、滚动箭头图标、弹跳 chevron 一律禁用。内容自当自然吸引用户
- **非对称结构：**变化度超过 4 时，居中式 Hero 布局一律禁用
- **克制 CTA：**主 CTA 至多一个，不放「Learn more」之类的次级链接

### 5. 描述组件样式
对每类组件，描述其形状、颜色、阴影深度与交互行为：
- **按钮：**按下态提供触感回压。不要霓虹外发光，不要自定义鼠标光标
- **卡片：**仅当投影确实承载层级信息时才用。阴影色调须向背景色相靠拢。高密度布局下，用 border-top 分隔线或留白替代卡片
- **输入框/表单：**标签在输入框上方，辅助文本可选，错误文本在下方。间距遵循标准
- **加载状态：**使用与布局尺寸精确匹配的骨架屏——不用千篇一律的圆形 spinner
- **空状态：**精心构图的画面，指引用户如何填充数据
- **错误状态：**清晰、行内的错误提示

### 6. 制定布局原则
- 元素互不重叠——每个元素各占清晰的独立空间，不用绝对定位堆叠内容
- 变化度超过 4 时禁用居中 Hero——强制改用分屏、左对齐或非对称留白
- 禁用平庸的「三张等宽卡片横排」功能行——改用双列 Z 字形（Zig-Zag）、非对称网格或横向滚动
- 布局用 CSS Grid，不玩 Flexbox 数学——绝不用 `calc()` 百分比戏法
- 用 max-width 约束版心（如 1400px 居中）
- 全屏高度的区块必须用 `min-h-[100dvh]`——绝不用 `h-screen`（iOS Safari 会发生灾难性跳动）

### 7. 制定响应式规则
所有设计必须在各类视口下都正常工作：
- **移动优先折叠（< 768px）：**所有多栏布局折叠为单栏，无一例外
- **禁止横向滚动：**移动端出现横向溢出即为致命失败
- **字号缩放：**标题用 `clamp()` 缩放，正文最小 `1rem`/`14px`
- **触控目标：**所有可交互元素的最小点击区域为 `44px`
- **图片行为：**行内图片（嵌在词句间的照片）在移动端堆叠到标题下方
- **导航：**桌面端横向导航折叠为简洁的移动端菜单
- **间距：**区块纵向间距按比例缩减（`clamp(3rem, 8vw, 6rem)`）

### 8. 写入动效哲学
- **弹簧物理为默认：**`stiffness: 100, damping: 20`——质感高级、分量十足。不用线性缓动
- **永续微交互：**每个活跃组件都应具备一种无限循环状态（Pulse 脉冲、Typewriter 打字机、Float 漂浮、Shimmer 微光）
- **错峰编排：**列表绝不瞬时挂载——用级联延迟做瀑布式呈现
- **性能：**只动画 `transform` 与 `opacity`。绝不动画 `top`、`left`、`width`、`height`。颗粒/噪点滤镜只放在固定定位的伪元素上

### 9. 列出反面模式（AI 痕迹）
在 DESIGN.md 中把它们写成明确的「绝不（NEVER DO）」规则：
- 任何地方都不用 emoji
- 不用 `Inter` 字体
- 不用通用衬线体（`Times New Roman`、`Georgia`、`Garamond`）——确需衬线时只用辨识度高的现代衬线体
- 不用纯黑（`#000000`）
- 不用霓虹/外发光阴影
- 不用饱和度过高的强调色
- 大标题不滥用渐变文字
- 不用自定义鼠标光标
- 元素不重叠——始终保持整洁的空间分隔
- 不用三等分卡片布局
- 不用俗套的名字（「John Doe」「Acme」「Nexus」）
- 不用虚假的完美数值（`99.99%`、`50%`）
- 不用 AI 文案套话（「Elevate」「Seamless」「Unleash」「Next-Gen」）
- 不用填充型 UI 文案：「Scroll to explore」「Swipe down」、滚动箭头、弹跳 chevron
- 不用失效的 Unsplash 链接——改用 `picsum.photos` 或 SVG 头像
- 不用居中 Hero 区（高变化度项目）

## 输出格式（DESIGN.md 结构）

```markdown
# Design System: [Project Title]

## 1. Visual Theme & Atmosphere
(Evocative description of the mood, density, variance, and motion intensity.
Example: "A restrained, gallery-airy interface with confident asymmetric layouts
and fluid spring-physics motion. The atmosphere is clinical yet warm — like a
well-lit architecture studio.")

## 2. Color Palette & Roles
- **Canvas White** (#F9FAFB) — Primary background surface
- **Pure Surface** (#FFFFFF) — Card and container fill
- **Charcoal Ink** (#18181B) — Primary text, Zinc-950 depth
- **Muted Steel** (#71717A) — Secondary text, descriptions, metadata
- **Whisper Border** (rgba(226,232,240,0.5)) — Card borders, 1px structural lines
- **[Accent Name]** (#XXXXXX) — Single accent for CTAs, active states, focus rings
(Max 1 accent. Saturation < 80%. No purple/neon.)

## 3. Typography Rules
- **Display:** [Font Name] — Track-tight, controlled scale, weight-driven hierarchy
- **Body:** [Font Name] — Relaxed leading, 65ch max-width, neutral secondary color
- **Mono:** [Font Name] — For code, metadata, timestamps, high-density numbers
- **Banned:** Inter, generic system fonts for premium contexts. Serif fonts banned in dashboards.

## 4. Component Stylings
* **Buttons:** Flat, no outer glow. Tactile -1px translate on active. Accent fill for primary, ghost/outline for secondary.
* **Cards:** Generously rounded corners (2.5rem). Diffused whisper shadow. Used only when elevation serves hierarchy. High-density: replace with border-top dividers.
* **Inputs:** Label above, error below. Focus ring in accent color. No floating labels.
* **Loaders:** Skeletal shimmer matching exact layout dimensions. No circular spinners.
* **Empty States:** Composed, illustrated compositions — not just "No data" text.

## 5. Layout Principles
(Grid-first responsive architecture. Asymmetric splits for Hero sections.
Strict single-column collapse below 768px. Max-width containment.
No flexbox percentage math. Generous internal padding.)

## 6. Motion & Interaction
(Spring physics for all interactive elements. Staggered cascade reveals.
Perpetual micro-loops on active dashboard components. Hardware-accelerated
transforms only. Isolated Client Components for CPU-heavy animations.)

## 7. Anti-Patterns (Banned)
(Explicit list of forbidden patterns: no emojis, no Inter, no pure black,
no neon glows, no 3-column equal grids, no AI copywriting clichés,
no generic placeholder names, no broken image links.)
```

## 最佳实践
- **描述具体：**写「Deep Charcoal Ink (#18181B)」，而不是笼统的「深色文字」
- **说明用途：**讲清每个元素是干什么用的
- **保持一致：**全篇术语统一
- **精确到位：**括注确切的十六进制色值、rem 值与像素值
- **立场鲜明：**这不是中性模板——它强制推行一种特定的高端审美

## 成功要诀
1. 先定氛围——弄清气质基调，再细化设计令牌（design token）
2. 寻找规律——识别一致的间距、尺寸与样式
3. 语义命名——按用途而非外观给颜色命名
4. 考虑层级——记录视觉权重如何传达重要程度
5. 写入禁令——反面模式与正面规则同等重要

## 常见误区
- 堆砌技术行话而不加转译（写「rounded-xl」，而不是「宽裕的圆角」这样的自然描述）
- 漏写十六进制色值，或只给描述性名称
- 遗漏设计元素的功能角色
- 氛围描述过于含糊
- 无视反面模式清单——正是它们成就了高端质感
- 退回平庸「安全」的设计，而不坚守甄选的美学
