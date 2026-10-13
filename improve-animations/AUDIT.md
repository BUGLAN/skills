# 动效审计手册

八个审计类别：每类要查什么，以及在发现与计划中应引用的精确目标值。浓缩自 Emil Kowalski 的设计工程哲学（[emilkowal.ski](https://emilkowal.ski/)）。凡本文出现的数值，一律照抄，不许近似。

## 1. 目的与频率

每个动画都必须回答"为什么要动？"——为了空间一致性、状态指示、反馈、解释，或避免突兀的变化。高频出现的元素上，"看起来很酷"不构成目的。

| 频率 | 决策 |
| --- | --- |
| 每天 100+ 次（键盘快捷键、命令面板开关） | 不加动画。永远不加。 |
| 每天数十次（hover 效果、列表导航） | 移除或大幅削减 |
| 偶尔（模态框、抽屉、toast） | 标准动画 |
| 罕见 / 首次（新手引导、反馈、庆祝时刻） | 可以增添愉悦感 |

排查重点：键盘触发的操作上加了动画；命令面板带开合过渡（Raycast 就没有——这是对的）；列表项或高频触发的 hover 状态上的装饰性动效。最有力的修复往往是**直接删掉动画**。

## 2. 缓动与时长

缓动的决策顺序：

- 进场或退场 → **`ease-out`**（起步快，显得响应迅速）
- 屏幕内移动 / 形变 → **`ease-in-out`**
- hover / 颜色变化 → **`ease`**
- 匀速运动（跑马灯、进度条） → **`linear`**
- 默认 → **`ease-out`**

**UI 上出现 `ease-in` 永远是一条发现**——它起步慢，恰恰拖延了用户正盯着的那一刻。CSS 内置缓动对有意图的运动来说太弱；计划应引入有力的自定义曲线（以 token 形式提供，遵循仓库既有约定）：

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);        /* strong ease-out for UI */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);    /* strong ease-in-out for on-screen movement */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);     /* iOS-like drawer curve */
```

时长预算——**UI 动画保持在 300ms 以内**：

| 元素 | 时长 |
| --- | --- |
| 按钮按压反馈 | 100–160ms |
| Tooltip、小型 popover | 125–200ms |
| 下拉菜单、select | 150–250ms |
| 模态框、抽屉 | 200–500ms |
| 营销 / 讲解型动画 | 可以更长 |

排查重点：任何位置出现 `ease-in`；进场动画直接用裸 `ease`/`linear`；UI 元素时长超过 300ms；工具栏中每个 tooltip 都带延迟加动画（第一个之后都应即刻出现）。

## 3. 物理感与起点

- **绝不用 `scale(0)`**——现实世界里没有东西会凭空出现。目标值：`scale(0.9–0.97)` + `opacity: 0`。
- **popover / 下拉菜单 / tooltip 从触发元素缩放展开**，而不是从中心：
  ```css
  .popover { transform-origin: var(--transform-origin); } /* Base UI */
  ```
  **模态框例外**——它居中出现，`transform-origin: center` 在此处是正确的。不要把它报成问题。
- **按压反馈**：在 `:active` 上加 `transform: scale(0.97)`，配合 `transition: transform 160ms ease-out`。幅度保持克制（0.95–0.98）。

排查重点：`scale(0)`；没有初始 transform 的纯淡入进场；锚定触发元素的组件却用 `transform-origin: center`（或未设置）；可按压元素却无按压反馈。

## 4. 可中断性

CSS **transition** 会在动画中途从当前状态重新瞄准目标；**keyframes** 则从零重启。凡是会被快速连续触发、或运动中途可逆的元素（toast 堆叠、开关切换、拖拽、展开/收起），都必须用 transition 或 spring。

- 不用 JS 的进场方案：`@starting-style`（旧环境后备方案：在 `useEffect` 里设置 `data-mounted` 属性）。
- 手势驱动的运动应当用 spring——被打断时它能继承当前速度。
- spring 配置，Apple 风格（推荐）：`{ type: "spring", duration: 0.5, bounce: 0.2 }`。bounce 保持克制（0.1–0.3）；明显的回弹留给拖拽关闭和俏皮时刻。
- **非对称时序**：需要刻意的阶段（按压、长按、危险操作确认）动画放慢；系统的响应则要干脆利落。按下与松开时序完全对称是一条发现。

排查重点：toast / 开关 / 高频触发 UI 上使用 `@keyframes`；手势处理器用固定时长的 keyframes 做补间；拖拽关闭缺少基于速度的判定（以 `Math.abs(distance)/elapsedMs > ~0.11` 判定关闭，而不是只看距离阈值）；拖到边界时生硬急停，而非摩擦力渐增。

## 5. 性能

- **只对 `transform` 和 `opacity` 做动画。** `width`/`height`/`margin`/`padding`/`top`/`left` 会触发 layout + paint + composite。
- **`transition: all`** 会把意料之外的属性一并拉入动画，且脱离 GPU 加速——永远是一条发现。
- **Framer Motion 的 `x`/`y`/`scale` 简写没有硬件加速**——它们跑在主线程上，负载一高就掉帧。目标写法：完整的 transform 字符串，`animate={{ transform: "translateX(100px)" }}`。
- **不要用父元素上的 CSS 变量驱动子元素 transform**——这会让所有子元素重算样式。直接在元素自身上设置 `transform`。
- 高负载下，CSS（以及 WAAPI）优于基于 rAF 的 JS——预先确定的运动用 CSS，动态与手势驱动的运动用 JS / spring。
- 过渡期间的 `filter: blur()` 控制在 20px 以内——重度模糊开销很大，Safari 尤其明显。

排查重点：`transition: all`；被动画的布局属性；繁忙页面上使用 Framer Motion 简写属性；用 `setProperty('--x', …)` 驱动子元素 transform；rAF 循环干了 CSS 本可胜任的事。

## 6. 无障碍

```css
@media (prefers-reduced-motion: reduce) {
  .element { animation: fade 0.2s ease; } /* keep opacity/color, drop movement */
}
@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.05); } /* touch fires false hovers on tap */
}
```

减弱动态效果意味着更少、更柔和的动画，**而不是零动画**——保留有助于理解的过渡，去掉位置移动。JS 中用 `useReducedMotion()`，并对 transform 值做分支处理。

排查重点：位移动画完全没有 `prefers-reduced-motion` 处理；未加门槛的 `:hover` 动效；reduced-motion 实现一刀切，把所有反馈全部砍掉。

## 7. 一致性与 token

- 动效要贴合产品性格——俏皮的产品可以更弹，仪表盘则要保持利落。各组件性格不一致是一条发现。
- 曲线与时长应当沉淀为共享 token。五处手写、几乎相同却不完全一致的 cubic-bezier，是一条该收敛的发现。
- 本该用 **30–80ms stagger** 的组进场，却让所有元素同时出现。stagger 属于装饰——绝不能阻塞交互。
- 交叉淡化若出现两个状态的叠影、显得突兀，可在过渡期间叠加一层轻微的 `filter: blur(2px)` 来掩盖。

排查重点：近乎相同的缓动 / 时长重复出现；利落的应用里混进一个弹性过足的组件；列表 / 网格进场没有 stagger；交叉淡化出现明显叠影。

## 8. 错失的机会

增补类——本可以动却没动的地方：

- 状态变化生硬跳变（内容切换、布局跳动），一段简短的过渡本可避免这种突兀。
- 空间上相关联的 UI（从某个触发处展开的面板），却没有交代来向的运动。
- 罕见的高情绪时刻（首次使用、成功、庆祝）被呈现得毫无愉悦感，而这些场合本就允许花这份预算。
- 实现这些效果的工具：`translate` 百分比（`translateY(100%)` = 元素自身高度）与 `clip-path: inset()` 揭示——不要硬编码像素偏移。

最多报告寥寥数条，且必须落在你实际观察到的体验断点上——不是愿望清单。
