# 切换器（The Picker）

切换器的外观**不是一个设计决策**——它本身就是本规范。下面的标记、CSS 和接线逻辑逐字照抄；每次运行唯一会变的，只有变体的名称和数量。它在所有项目中保持完全一致，因此看起来永远是底座的外壳，而绝不会像被评审的设计的一部分。不要用项目的 token、字体或颜色给它重新定型。

它是一个悬浮的深色胶囊，位于底部居中。深色玻璃放在任何页面上——浅色或深色——都能成立，这正是它不做主题适配的原因。

## 标记

先放滑动高亮 span，然后每个变体一个按钮，一条发丝级分隔线，最后是重播按钮（仅当至少一个变体有值得重触发的动效时才渲染）：

```html
<nav class="proto-picker" aria-label="Prototype variants">
  <span class="proto-picker-highlight" aria-hidden="true"></span>
  <button class="proto-picker-item" data-active aria-current="true">Quiet</button>
  <button class="proto-picker-item">Editorial</button>
  <button class="proto-picker-item">Playful</button>
  <span class="proto-picker-divider" aria-hidden="true"></span>
  <button class="proto-picker-item proto-picker-replay" aria-label="Replay animation (R)">↻</button>
</nav>
```

在框架中，保留类名和结构，只改渲染语法。

## 样式

```css
.proto-picker {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2147483647;
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 4px;
  border-radius: 999px;
  background: rgba(10, 10, 10, 0.82);
  -webkit-backdrop-filter: blur(12px) saturate(1.4);
  backdrop-filter: blur(12px) saturate(1.4);
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.08) inset,
    0 8px 24px rgba(0, 0, 0, 0.24),
    0 2px 6px rgba(0, 0, 0, 0.12);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 13px;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  user-select: none;
  -webkit-user-select: none;
}

.proto-picker-highlight {
  position: absolute;
  top: 4px;
  left: 0;
  height: 28px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  will-change: transform;
}

/* The slide is enabled only after first paint (data-ready), so load doesn't animate. */
.proto-picker[data-ready] .proto-picker-highlight {
  transition:
    transform 250ms cubic-bezier(0.23, 1, 0.32, 1),
    width 250ms cubic-bezier(0.23, 1, 0.32, 1);
}

@media (prefers-reduced-motion: reduce) {
  .proto-picker[data-ready] .proto-picker-highlight { transition: none; }
}

.proto-picker-item {
  position: relative; /* sits above the highlight */
  display: flex;
  align-items: center;
  height: 28px;
  padding: 0 12px;
  border: 0;
  border-radius: 999px;
  background: transparent;
  color: rgba(255, 255, 255, 0.55);
  font: inherit;
  cursor: pointer;
  transition: color 150ms ease-out;
}

.proto-picker-item:hover {
  color: rgba(255, 255, 255, 0.85);
}

.proto-picker-item:active {
  transform: scale(0.97);
}

.proto-picker-item:focus-visible {
  outline: 2px solid rgba(255, 255, 255, 0.4);
  outline-offset: 2px;
}

.proto-picker-item[data-active] {
  color: #fff;
}

.proto-picker-divider {
  width: 1px;
  height: 16px;
  margin: 0 4px;
  background: rgba(255, 255, 255, 0.12);
}

.proto-picker-replay {
  padding: 0 10px;
  font-size: 14px;
}

.proto-picker[data-position="top"] {
  bottom: auto;
  top: 24px;
}
```

## 规则

- **逐字照抄。** 这些数值就是规范。不用项目字体，不用品牌色，不做主题切换，不加多余的阴影或边框。
- **高亮会滑动，变体切换保持即时。** 激活胶囊在按钮之间做动画（250ms，强 ease-out），作为切换器自身的空间反馈——但正在预览的变体依旧无过渡地直接切换。`width` 过渡是对 transform/opacity 法则的一次有意豁免：该元素高 28px、绝对定位、没有任何布局依赖者，绘制成本可以忽略不计。
- **唯一允许的修改：** 如果某个变体占据了屏幕底部居中的位置（toast 堆叠、底部抽屉、dock），就设置 `data-position="top"`，让切换器永不遮挡作品。除此之外，它的任何部分都不许挪动或改变。
- **重播按钮按需渲染。** 只有当至少一个变体带有值得重触发的入场或状态动画时，才渲染重播按钮及其分隔线；纯静态对比用更短的胶囊即可。

## 行为契约

无论底座如何渲染，契约固定不变：

- 数字键 `1–N` 和 `←`/`→` 切换变体；`R` 重播。焦点位于 input、textarea、select 或 contenteditable 中，或按住修饰键时，忽略按键事件。
- 点击某一项即切换到它；任何时刻都有且仅有一项携带 `data-active` 和 `aria-current="true"`，高亮随之滑动到位。
- 选择通过 URL 参数（`?v=2`）在刷新后保留，缺省回退到变体 1。高亮初始就位时不带动画（`data-ready` 在首次绘制之后添加）。
- 切换会重新挂载变体（入场动画因此重跑）；重播键只重新挂载、不切换。

## 参考接线

独立 HTML 分支下逐字照抄；在框架中保持同样的行为，但用惯用方式表达（用状态代替 `innerHTML`，用带 key 的重挂载代替 `requestAnimationFrame`，用 refs 加 layout effect 测量高亮）。

```js
// `variants` is an array of render functions, one per variant, in picker order.
const stage = document.getElementById('stage');
const picker = document.querySelector('.proto-picker');
const highlight = picker.querySelector('.proto-picker-highlight');
const items = [...picker.querySelectorAll('.proto-picker-item:not(.proto-picker-replay)')];
const replay = picker.querySelector('.proto-picker-replay');
let current = 0;

function moveHighlight() {
  const el = items[current];
  highlight.style.width = el.offsetWidth + 'px';
  highlight.style.transform = `translateX(${el.offsetLeft}px)`;
}

function mount(i) {
  stage.innerHTML = '';
  // Clear first, render next frame, so entrance animations re-run.
  requestAnimationFrame(() => { stage.innerHTML = variants[i](); });
}

function setActive(i) {
  if (i < 0 || i >= variants.length) return;
  current = i;
  items.forEach((el, j) => {
    el.toggleAttribute('data-active', j === i);
    if (j === i) el.setAttribute('aria-current', 'true');
    else el.removeAttribute('aria-current');
  });
  moveHighlight();
  const url = new URL(location);
  url.searchParams.set('v', i + 1);
  history.replaceState(null, '', url);
  mount(i);
}

items.forEach((el, i) => el.addEventListener('click', () => setActive(i)));
replay?.addEventListener('click', () => mount(current));
window.addEventListener('resize', moveHighlight);

document.addEventListener('keydown', (e) => {
  if (/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) || e.target.isContentEditable) return;
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  const num = parseInt(e.key, 10);
  if (num >= 1 && num <= variants.length) setActive(num - 1);
  else if (e.key === 'ArrowRight') setActive((current + 1) % variants.length);
  else if (e.key === 'ArrowLeft') setActive((current - 1 + variants.length) % variants.length);
  else if (e.key === 'r' || e.key === 'R') mount(current);
});

setActive((parseInt(new URLSearchParams(location.search).get('v'), 10) || 1) - 1);
// Enable the slide only after first paint, so load doesn't animate.
requestAnimationFrame(() => requestAnimationFrame(() => picker.setAttribute('data-ready', '')));
```
