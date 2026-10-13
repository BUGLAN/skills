# 状态与变体

组件状态定义与变体模式。

## 交互状态

### 状态定义

| 状态 | 触发条件 | 视觉变化 |
|------|----------|----------|
| default | 无 | 基础外观 |
| hover | 鼠标悬停 | 颜色轻微加深 |
| focus | Tab/点击 | 显示焦点环 |
| active | 鼠标按下 | 颜色最深 |
| disabled | disabled 属性 | 降低不透明度 |
| loading | 异步操作 | Spinner + 降低不透明度 |

### 状态优先级

多个状态同时生效时，优先级从高到低依次为：

1. disabled
2. loading
3. active
4. focus
5. hover
6. default

### 状态过渡

```css
/* Standard transition for interactive elements */
.interactive {
  transition-property: color, background-color, border-color, box-shadow;
  transition-duration: var(--duration-fast);
  transition-timing-function: ease-in-out;
}
```

| 过渡项 | 时长 | 缓动 |
|--------|------|------|
| 颜色变化 | 150ms | ease-in-out |
| 背景 | 150ms | ease-in-out |
| 变换（transform） | 200ms | ease-out |
| 不透明度 | 150ms | ease |
| 阴影 | 200ms | ease-out |

## 焦点状态

### 焦点环规格

```css
/* Standard focus ring */
.focusable:focus-visible {
  outline: none;
  box-shadow: 0 0 0 var(--ring-offset) var(--color-background),
              0 0 0 calc(var(--ring-offset) + var(--ring-width)) var(--ring-color);
}
```

| 属性 | 值 |
|------|-----|
| 焦点环宽度 | 2px |
| 焦点环偏移 | 2px |
| 焦点环颜色 | primary (blue-500) |
| 偏移底色 | background |

### 容器焦点（focus-within）

```css
/* Container focus when child is focused */
.container:focus-within {
  border-color: var(--color-ring);
}
```

## 禁用状态

### 视觉处理

```css
.disabled {
  opacity: var(--opacity-disabled); /* 0.5 */
  pointer-events: none;
  cursor: not-allowed;
}
```

| 属性 | 禁用时的值 |
|------|------------|
| 不透明度 | 50% |
| 指针事件（pointer-events） | none |
| 光标 | not-allowed |
| 背景 | muted |
| 颜色 | muted-foreground |

### 无障碍

- 需要语义化禁用时，使用 `aria-disabled="true"`
- 表单元素直接使用 `disabled` 属性
- 保持足够的对比度（至少 3:1）

## 加载状态

### Spinner 位置

| 组件 | Spinner 位置 |
|------|--------------|
| Button | 替换图标或居中显示 |
| Input | 尾部位置 |
| Card | 居中覆盖层 |
| Page | 视口中央 |

### 加载态处理

```css
.loading {
  position: relative;
  pointer-events: none;
}

.loading::after {
  content: '';
  /* spinner styles */
}

.loading > * {
  opacity: 0.7;
}
```

## 错误状态

### 视觉指示

```css
.error {
  border-color: var(--color-error);
  color: var(--color-error);
}

.error:focus-visible {
  box-shadow: 0 0 0 2px var(--color-background),
              0 0 0 4px var(--color-error);
}
```

| 元素 | 错误处理 |
|------|----------|
| 输入框边框 | red-500 |
| 输入框焦点环 | red/20% |
| 辅助文本 | red-600 |
| 图标 | red-500 |

### 错误提示

- 置于输入框下方
- 使用错误色
- 配图标以保障无障碍
- 输入合法后即清除

## 变体模式

### 颜色变体

```css
/* Pattern for color variants */
.component {
  --component-bg: var(--color-primary);
  --component-fg: var(--color-primary-foreground);
  background: var(--component-bg);
  color: var(--component-fg);
}

.component.secondary {
  --component-bg: var(--color-secondary);
  --component-fg: var(--color-secondary-foreground);
}

.component.destructive {
  --component-bg: var(--color-destructive);
  --component-fg: var(--color-destructive-foreground);
}
```

### 尺寸变体

```css
/* Pattern for size variants */
.component {
  --component-height: 40px;
  --component-padding: var(--space-4);
  --component-font: var(--font-size-sm);
}

.component.sm {
  --component-height: 32px;
  --component-padding: var(--space-3);
  --component-font: var(--font-size-xs);
}

.component.lg {
  --component-height: 48px;
  --component-padding: var(--space-6);
  --component-font: var(--font-size-base);
}
```

## 无障碍要求

### 色彩对比度

| 元素 | 最低对比度 |
|------|------------|
| 普通文本 | 4.5:1 |
| 大号文本（18px 以上） | 3:1 |
| UI 组件 | 3:1 |
| 焦点指示 | 3:1 |

### 状态指示

- 绝不仅靠颜色传达状态
- 辅以图标、文字或图案
- 确保焦点可见
- 播报加载状态

### ARIA 状态

```html
<!-- Disabled -->
<button disabled aria-disabled="true">Submit</button>

<!-- Loading -->
<button aria-busy="true" aria-describedby="loading-text">
  <span id="loading-text" class="sr-only">Loading...</span>
</button>

<!-- Error -->
<input aria-invalid="true" aria-describedby="error-msg">
<span id="error-msg" role="alert">Error message</span>
```
