# React / Next.js / Tailwind 提取模式

本参考覆盖最常见的前端技术栈（stack）：React 组件搭配 Tailwind CSS（可选配 CSS Modules、styled-components 或 Emotion）。

## 文件查找顺序

按优先级顺序读下列文件——优先级越高的文件，越能反映意图中的设计系统；优先级越低的文件，越能反映实际交付的样子：

1. **`tailwind.config.js` / `tailwind.config.ts`** —— 全场最重要的文件。自定义的 `theme.extend.colors`、`fontFamily`、`spacing`、`borderRadius` 与 `screens` 就是设计系统的定义。

2. **`globals.css` / `global.css` / `index.css`** —— CSS 自定义属性（`--*`）、`@layer` 指令、`@font-face` 声明与基础样式。

3. **`theme.ts` / `theme.js` / `tokens.ts`** —— 显式的设计令牌文件。导出的对象可能被 Tailwind 配置或 CSS-in-JS Provider 消费。

4. **`src/app/layout.tsx` 或 `src/App.tsx`** —— 根布局。可见全局字体设置（经 `next/font` 或 `<link>`）、body 背景与整体结构。

5. **组件文件（`*.tsx` / `*.jsx`）** —— 挑 5-8 个有代表性的组件，理解用法模式。

## Tailwind 配置提取

Tailwind 配置结构化、机器可读，直接提取：

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#294056',      // → "Deep Muted Teal-Navy" — Primary CTA
        background: '#FCFAFA',   // → "Warm Barely-There Cream" — Page BG
      },
      fontFamily: {
        sans: ['Manrope', 'sans-serif'],
      },
      borderRadius: {
        card: '12px',
        button: '8px',
      },
      spacing: {
        section: '5rem',
      }
    }
  }
}
```

把每个自定义值映射到描述性名称和角色。

## CSS 自定义属性

在全局 CSS 中寻找 `:root` 或 `html` 块：

```css
:root {
  --color-primary: #294056;
  --color-bg: #FCFAFA;
  --font-heading: 'Manrope', sans-serif;
  --radius-card: 12px;
  --spacing-section: 5rem;
}
```

这些是显式声明的令牌——把变量名当作其预期角色的线索。

## Next.js 字体模式

Next.js 用 `next/font` 做优化字体加载：

```tsx
import { Inter, Playfair_Display } from 'next/font/google'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const playfair = Playfair_Display({ subsets: ['latin'], variable: '--font-display' })
```

`variable` 的命名暗示了用途：`--font-display` 用于标题，`--font-inter` 用于正文。

## 组件扫描策略

不必逐个读完所有组件，聚焦这几类典型即可：

| 组件类型 | 提取什么 |
|:---|:---|
| 布局 / 外壳 | max-width、padding、栅格结构 |
| 按钮 / CTA | 圆角、颜色、hover 状态、padding |
| 卡片 | 阴影、描边、圆角、内部间距 |
| 导航 / 页头 | 字体处理、激活状态 |
| 表单 / 输入框 | 描边、聚焦状态、padding |
| Hero / 落地页区块 | 间距、字号阶梯、对齐 |

对每一类，看 `className` prop 里的 Tailwind 类名，或 `styled()` / `css()` 调用中的 CSS-in-JS 取值。

## CSS-in-JS 模式（styled-components / Emotion）

如果项目用 CSS-in-JS，去找 theme provider：

```tsx
// ThemeProvider wrapping the app
const theme = {
  colors: {
    primary: '#294056',
    background: '#FCFAFA',
  },
  fonts: {
    heading: 'Manrope, sans-serif',
  },
  radii: {
    card: '12px',
    button: '8px',
  }
}
```

这个 theme 对象*就是*设计系统，直接提取。

## 组件库集成

如果项目用了 Chakra UI、Material UI、Ant Design 或 shadcn/ui：

- **Chakra**：寻找 `extendTheme()` 调用——它们覆写了默认值。
- **MUI**：寻找 `createTheme()`——对调色板、字体排印与间距的覆写。
- **Ant Design**：寻找 `ConfigProvider` 的 theme prop 或 `theme.ts` 覆写。
- **shadcn/ui**：颜色以 CSS 自定义属性的形式定义在 `globals.css`；样式配置见 `components.json`。

这些覆写才是设计系统——默认值只是组件库的通用样式，记录即可，不必着墨。

## 响应式模式

检查 Tailwind 的 `screens` 配置，并在组件里留意响应式类前缀（`sm:`、`md:`、`lg:`、`xl:`）：

```js
screens: {
  sm: '640px',   // Mobile landscape
  md: '768px',   // Tablet
  lg: '1024px',  // Desktop
  xl: '1280px',  // Large desktop
  '2xl': '1536px'
}
```

再看 `container` 配置和布局组件上的 `max-width` 模式，判断内容宽度策略。
