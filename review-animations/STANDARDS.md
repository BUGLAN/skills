# 动画标准参考

审查背后的精确数值、曲线与规则。发现中请引用这些值，而不是近似取值。提炼自 Emil Kowalski 的设计工程哲学。

## 它该不该动？（频率表）

| 频率 | 决策 |
| --- | --- |
| 每天 100 次以上（键盘快捷键、命令面板开关） | 不做动画。绝对不做。 |
| 每天几十次（hover 效果、列表导航） | 删除或大幅削弱 |
| 偶尔（modal、drawer、toast） | 标准动画 |
| 罕见 / 首次（新手引导、反馈、庆祝时刻） | 可以加趣味 |

**绝不给键盘触发的操作做动画**——它们每天重复成百上千次；动画会让它们显得又慢又脱节。（Raycast 没有打开/关闭动画——对每天使用几百次的东西而言，这正是正确做法。）

动效的正当目的：空间一致性、状态指示、解释说明、反馈、避免突兀变化。在高频出现的元素上说"它看起来很酷"不成立。

## 缓动

判断顺序：
- 进入或退出 → **`ease-out`**（起步快，感觉响应迅速）
- 屏幕上移动 / 形变 → **`ease-in-out`**
- hover / 颜色变化 → **`ease`**
- 匀速运动（跑马灯、进度）→ **`linear`**
- 默认 → **`ease-out`**

**UI 上绝不用 `ease-in`。** 它起步慢，恰恰拖延了用户正在注视的那一刻。200ms 的 `ease-out` *感觉上*比 200ms 的 `ease-in` 更快。

CSS 内置缓动太弱。使用有力的自定义曲线：

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);        /* strong ease-out for UI */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);    /* strong ease-in-out for on-screen movement */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);     /* iOS-like drawer curve (Ionic) */
```

曲线可在 [easing.dev](https://easing.dev/) 或 [easings.co](https://easings.co/) 上找——不要从零手搓。

## 时长

| 元素 | 时长 |
| --- | --- |
| 按钮按压反馈 | 100–160ms |
| tooltip、小型 popover | 125–200ms |
| 下拉菜单、select | 150–250ms |
| modal、drawer | 200–500ms |
| 营销 / 说明性动画 | 可以更长 |

**规则：UI 动画保持在 300ms 以内。** 180ms 的下拉菜单比 400ms 的更有响应感。更快的 spinner 让加载显得更快（实际耗时相同）。第一个之后的 tooltip 立即出现（跳过延迟和动画）会让工具栏显得更快。

## 物理感

- **绝不用 `scale(0)`。** 从 `scale(0.9–0.97)` + `opacity: 0` 开始。现实世界里没有东西凭空出现。
- **popover 要感知起始方位。** 从触发元素缩放，而不是从中心：
  ```css
  .popover { transform-origin: var(--transform-origin); } /* Base UI */
  ```
  **modal 例外**——它们出现在视口中央，保留 `transform-origin: center`。
- **按钮按压反馈。** `:active` 时加 `transform: scale(0.97)`，配 `transition: transform 160ms ease-out`。幅度要细微（0.95–0.98）。适用于任何可按压元素。

## Spring

Spring 之所以感觉自然，是因为它模拟物理；没有固定时长——动画按参数自行收敛到位。适用于：带惯性的拖拽、"有生命感"的元素（灵动岛）、可中断手势、装饰性鼠标跟随。

```js
// Apple-style (easier to reason about) — recommended
{ type: "spring", duration: 0.5, bounce: 0.2 }

// Traditional physics (more control)
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }
```

bounce 保持细微（0.1–0.3）；大多数 UI 避免用 bounce——留给拖拽关闭和俏皮交互。Spring 被中断时会保持速度（keyframes 则从零重启），因此特别适合用户可能中途反向的手势。

鼠标交互：用 `useSpring` 做插值，而不是把数值直接绑到鼠标位置（直接绑定 = 呆板造作，没有惯性）。仅当动效纯属装饰时才这样做。

## 可中断性

CSS **transitions** 可以在动画中途被中断并重新定向；**keyframes** 则从零重启。对任何高频触发的东西（不断添加的 toast、开关），transitions 更顺滑。

```css
/* Interruptible — good for dynamic UI */
.toast { transition: transform 400ms ease; }

/* Not interruptible — avoid for dynamic UI */
@keyframes slideIn { from { transform: translateY(100%); } to { transform: translateY(0); } }
```

用 `@starting-style` 实现无需 JS 的入场：

```css
.toast {
  opacity: 1; transform: translateY(0);
  transition: opacity 400ms ease, transform 400ms ease;
  @starting-style { opacity: 0; transform: translateY(100%); }
}
```

兼容旧环境的回退方案：`useEffect(() => setMounted(true), [])` + `data-mounted` 属性。

## 不对称时长

用户决策之处放慢，系统响应之处加快。

```css
.overlay { transition: clip-path 200ms ease-out; }            /* release: fast */
.button:active .overlay { transition: clip-path 2s linear; }  /* press: slow, deliberate */
```

## 性能

- **只对 `transform` 和 `opacity` 做动画**——它们跳过 layout/paint，在 GPU 上运行。`padding`/`margin`/`height`/`width`/`top`/`left` 会触发全部三个渲染步骤。
- **不要通过父元素上的 CSS 变量驱动子元素 transform**——这会为所有子元素重算样式。直接在元素上设置 `transform`。
  ```js
  element.style.setProperty('--swipe-amount', `${d}px`); // bad: recalc on all children
  element.style.transform = `translateY(${d}px)`;        // good: only this element
  ```
- **Framer Motion 简写属性并非硬件加速。** `x`/`y`/`scale` 经由 rAF 在主线程上运行，高负载下会掉帧。使用完整 transform 字符串：
  ```jsx
  <motion.div animate={{ x: 100 }} />                          // drops frames under load
  <motion.div animate={{ transform: "translateX(100px)" }} />  // hardware accelerated
  ```
- **高负载下 CSS 动画胜过 JS**——它们不在主线程上运行；基于 rAF 的动画在浏览器加载/执行脚本/绘制时会卡顿。预先确定的动效用 CSS，动态/可中断的用 JS。
- **WAAPI** 以 CSS 的性能提供 JS 的控制力（硬件加速、可中断、无需任何库）：
  ```js
  element.animate([{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
    { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' });
  ```

## transform 与 clip-path

- **`translate` 的百分比**相对于元素自身尺寸——`translateY(100%)` 移动元素自身的高度，与具体尺寸无关（Sonner/Vaul 定位 toast/drawer 正是如此）。优先于写死的 px。
- **`scale()` 会连同子元素一起缩放**（字体、图标、内容）——这正好是按压反馈可利用的特性。
- **3D**：`rotateX/Y` + `transform-style: preserve-3d` 无需 JS 即可实现景深/环绕/翻转。
- **`clip-path: inset(t r b l)`** 是强大的动画工具：每个值从对应一侧向内裁切。用途：滚动显现（`inset(0 0 100% 0)` → `inset(0 0 0 0)`）、长按删除遮罩、无缝的标签页颜色过渡（复制一份并裁切激活副本）、对比滑块。

## 手势与拖拽

- **凭惯性关闭**：不要要求划过某个距离阈值——计算速度（`Math.abs(distance)/elapsedMs`），大于 `~0.11` 即关闭。轻快一甩就应足以触发。
- **边界阻尼**：越过自然边界后，拖得越远移动量越小（真实物体停止前会先减速）。
- 拖拽一开始就**捕获指针（pointer capture）**，指针移出边界后拖拽仍能继续。
- **多点触控防护**：拖拽开始后忽略额外的触点（`if (isDragging) return`）——避免跳变。
- **用摩擦力代替硬停**——允许带渐增阻力的过冲拖拽，而不是一堵看不见的墙。

## 掩饰不完美的 crossfade

当 crossfade 在调过缓动/时长之后仍显出两个叠加的状态，就在过渡期间加一点轻微的 `filter: blur(2px)`，把两者融为一次可感知的变化。blur 保持在 20px 以内（重度 blur 开销大，Safari 尤甚）。

## Stagger

成组元素入场时加 stagger；条目之间间隔 30–80ms。更长的延迟显得拖沓。stagger 是装饰性的——它播放期间绝不阻塞交互。

```css
.item { opacity: 0; transform: translateY(8px); animation: fadeIn 300ms ease-out forwards; }
.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
@keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
```

## 无障碍

```css
@media (prefers-reduced-motion: reduce) {
  .element { animation: fade 0.2s ease; } /* keep opacity/color, drop transform-based motion */
}
@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.05); } /* gate hover motion — touch fires false hovers on tap */
}
```

```jsx
const reduce = useReducedMotion();
const closedX = reduce ? 0 : '-100%';
```

Reduced motion 意味着更少、更温和的动画，而不是零——保留有助于理解过渡的 transition，去掉位移/位置变化。

## 调试（手感拿不准时，建议在审查中推荐）

- **慢动作**：把时长放大 2–5 倍，或用 DevTools 动画检查器。检查颜色 crossfade 是否干净、缓动是否戛然而止、`transform-origin` 是否正确、协同变化的属性是否同步。
- **逐帧**：Chrome DevTools 的 Animations 面板能暴露协同属性之间的时机漂移。
- **真机**测手势（drawer、滑动）——连上手机，通过 IP 访问 dev server，用 Safari 远程开发工具。
- **隔天再看**——开发期间看不见的瑕疵之后会浮出水面。

## 协调

让动效匹配组件的个性：俏皮的产品可以更弹；专业仪表盘应当干脆利落。Sonner 之所以感觉对，部分原因是缓动、时长、设计乃至名字彼此和谐——略慢一点，用 `ease` 而不是 `ease-out`，以显得优雅。列表进出时的 opacity + height 靠反复试错；没有公式——调到感觉对为止。
