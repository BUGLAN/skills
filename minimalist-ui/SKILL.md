---
name: minimalist-ui
description: 干净的编辑风界面。暖调单色配色、字体排印对比、扁平 bento 网格、柔和粉彩色。不用渐变，不用重阴影。
---

# 协议：高端实用极简主义 UI 架构师

## 1. 协议概览
名称：高端实用极简主义与编辑风 UI
描述：一套高级前端工程指令，用于生成高度精致、极致极简、"文档式"的 web 界面，对标顶级 workspace 类产品。本协议严格执行：高对比度暖调单色配色、定制字体排印层级、精心设计的结构性宏观留白、bento 网格布局，以及点缀克制粉彩色的超扁平组件架构，并主动拒绝流于俗套的通用 SaaS 设计趋势。

## 2. 绝对负面清单（禁用元素）
AI 必须严格避开以下千篇一律的 web 开发默认做法：
- 禁用 "Inter"、"Roboto"、"Open Sans" 字体。
- 禁用 "Lucide"、"Feather" 或标准 "Heroicons" 等通用细线图标库。
- 禁用 Tailwind 默认的重投影（如 `shadow-md`、`shadow-lg`、`shadow-xl`）。阴影要么几乎不存在，要么深度定制为极度弥散、低不透明度（< 0.05）。
- 大型元素或区块不得使用主色背景（如不得出现亮蓝、亮绿或亮红的 hero 区块）。
- 禁用渐变、霓虹色与 3D 玻璃拟态（导航栏的轻微模糊除外）。
- 大型容器、卡片或主按钮不得使用 `rounded-full`（胶囊形）。
- 代码、标记、正文、标题、alt 文本中一律不得出现 emoji。应以得体的图标或简洁的 SVG 基础图形替代。
- 禁用 "John Doe"、"Acme Corp"、"Lorem Ipsum" 之类的通用占位名。应使用贴合语境的真实内容。
- 禁用 AI 文案套话："Elevate"、"Seamless"、"Unleash"、"Next-Gen"、"Game-changer"、"Delve"。文案要平实、具体。

## 3. 字体排印架构
界面必须依靠极致的字体对比与高端字体选型来确立编辑风基调。
- 主无衬线字体（正文、UI、按钮）：使用干净、几何感强或自带个性的系统原生字体。目标值：`font-family: 'SF Pro Display', 'Geist Sans', 'Helvetica Neue', 'Switzer', sans-serif`。
- 编辑风衬线字体（hero 标题与引文）：目标值：`font-family: 'Lyon Text', 'Newsreader', 'Playfair Display', 'Instrument Serif', serif`。字距收紧（`letter-spacing: -0.02em` 至 `-0.04em`），行高收紧（`1.1`）。
- 等宽字体（代码、按键、元数据）：目标值：`font-family: 'Geist Mono', 'SF Mono', 'JetBrains Mono', monospace`。
- 文本颜色：正文绝不用纯黑（`#000000`）。应使用近黑/炭色（`#111111` 或 `#2F3437`），并配以宽松的 `1.6` 行高保证易读性。次要文本用柔和灰（`#787774`）。

## 4. 调色板（暖调单色 + 局部粉彩）
颜色是稀缺资源，只用于传达语义或做细微点缀。
- 画布 / 背景：纯白 `#FFFFFF`，或暖骨白/米白 `#F7F6F3` / `#FBFBFA`。
- 主要表面（卡片）：`#FFFFFF` 或 `#F9F9F8`。
- 结构边框 / 分隔线：极浅灰 `#EAEAEA` 或 `rgba(0,0,0,0.06)`。
- 点缀色：只允许使用高度去饱和、带褪色感的粉彩色，用于标签、行内代码背景或淡色图标背景。
  - 淡红：`#FDEBEC`（文字：`#9F2F2D`）
  - 淡蓝：`#E1F3FE`（文字：`#1F6C9F`）
  - 淡绿：`#EDF3EC`（文字：`#346538`）
  - 淡黄：`#FBF3DB`（文字：`#956400`）

## 5. 组件规格
- Bento 功能网格：
  - 采用不对称的 CSS Grid 布局。
  - 卡片必须严格为 `border: 1px solid #EAEAEA`。
  - 圆角必须利落：`8px`，至多 `12px`。
  - 内边距必须宽裕（如 `24px` 至 `40px`）。
- 主 CTA（按钮）：
  - 纯色背景 `#111111`，文字 `#FFFFFF`。
  - 轻微圆角（`4px` 至 `6px`）。不用 box-shadow。
  - 悬停状态：颜色细微加深为 `#333333`，或做微缩放 `transform: scale(0.98)`。
- 标签与状态徽章：
  - 胶囊形（`border-radius: 9999px`），极小字号（`text-xs`），大写并放宽字距（`letter-spacing: 0.05em`）。
  - 背景必须使用上文定义的柔和粉彩色。
- 折叠面板（FAQ）：
  - 去掉所有容器框，条目之间仅以 `border-bottom: 1px solid #EAEAEA` 分隔。
  - 切换状态使用干净利落的 `+` 与 `-` 图标。
- 按键微组件：
  - 用 `<kbd>` 标签把快捷键渲染成实体按键：`border: 1px solid #EAEAEA`、`border-radius: 4px`、`background: #F7F6F3`，并使用等宽字体。
- 仿 OS 窗口边框：
  - 在做软件 mockup 时，包一层极简容器：白色顶栏，内含三个浅灰色小圆点（复刻 macOS 窗口控制按钮）。

## 6. 图标与图像指令
- 系统图标：使用 "Phosphor Icons"（Bold 或 Fill 字重）或 "Radix UI Icons"，营造偏技术感、笔画略粗的美学。所有图标的描边宽度必须统一。
- 插画：白底上的单色一笔连线墨稿，笔触随性，其中点缀一个偏移放置、填充柔和粉彩色的几何形状。
- 摄影：使用高质量、去饱和的暖调图片。叠加细微覆盖层（`opacity: 0.04` 的暖色颗粒）让照片融入单色配色。绝不用过度饱和的图库照片。缺少真实素材时，使用可靠的占位服务，如 `https://picsum.photos/seed/{context}/1200/800`。
- Hero 与区块背景：区块不应显得空洞扁平。可用极低不透明度的全宽背景图、柔和径向光斑（`radial-gradient`，暖色调，`opacity: 0.03`）或极简几何线条纹理增加纵深，同时不破坏干净的整体气质。

## 7. 细腻动效与微动画
动效应不着痕迹——存在，却从不喧宾夺主。追求的是安静的精致，而非视觉奇观。
- 滚动入场：元素进入视口时轻柔淡入。用 `translateY(12px)` + `opacity: 0`，在 `600ms` 内以 `cubic-bezier(0.16, 1, 0.3, 1)` 缓动完成。用 `IntersectionObserver` 实现，绝不用 `window.addEventListener('scroll')`。
- 悬停状态：卡片上浮，阴影极其细微地变化（`box-shadow` 在 `200ms` 内从 `0 0 0` 过渡到 `0 2px 8px rgba(0,0,0,0.04)`）。按钮在 `:active` 时以 `scale(0.98)` 响应。
- 交错呈现：列表与网格项以级联延迟依次入场（`animation-delay: calc(var(--index) * 80ms)`）。绝不让所有内容同时出现。
- 背景氛围动效：可选。一枚移动极缓慢的径向渐变色块（`animation-duration: 20s+`，`opacity: 0.02-0.04`）在 hero 区块后方漂移。必须置于 `position: fixed; pointer-events: none` 的图层上，绝不放在滚动容器内。
- 性能：只通过 `transform` 和 `opacity` 做动画。禁用触发布局的属性（`top`、`left`、`width`、`height`）。`will-change: transform` 须节制使用，且只加在正在动画的元素上。

## 8. 执行协议
当任务涉及编写前端代码（HTML、React、Tailwind、Vue）或设计布局时：
1. 先建立宏观留白。区块之间使用大量纵向内边距（如 Tailwind 的 `py-24` 或 `py-32`）。
2. 把主要排版内容的宽度约束在 `max-w-4xl` 或 `max-w-5xl`。
3. 立即套用定制字体排印层级与单色系颜色变量。
4. 确保每张卡片、每条分隔线、每处边框都严格遵守 `1px solid #EAEAEA` 规则。
5. 为所有主要内容块添加滚动入场动画。
6. 确保各区块借助图像、氛围渐变或细微纹理形成视觉纵深——不留空洞扁平的背景。
7. 交付的代码应原生体现这种高端、克制、编辑式的美学，无需再手工调整。
