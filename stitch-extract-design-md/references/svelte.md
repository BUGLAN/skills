# Svelte / SvelteKit 提取模式

Svelte 的样式同址程度比 Vue 更甚：每个 `.svelte` 文件都带一个默认即作用域隔离的 `<style>` 块。Svelte 项目的设计系统通常放在全局 CSS、CSS 自定义属性或共享的 theme store 里。

## 文件查找顺序

1. **`src/app.css` / `src/app.postcss`** —— 全局样式与 CSS 自定义属性。最重要的文件。

2. **`svelte.config.js`** —— 可能引用 CSS 预处理器、Tailwind 或 UnoCSS 配置。

3. **`tailwind.config.js`**（用了 Tailwind/UnoCSS 时）—— 提取方式与 React 相同。

4. **`src/lib/theme.ts` / `src/lib/tokens.ts`** —— 以 JS 对象导出的共享设计令牌。

5. **`src/routes/+layout.svelte`** —— 根布局。可见全局字体加载、背景与结构模式。

6. **组件 `<style>` 块** —— 作用域隔离的样式，揭示组件层面的模式。

## Svelte 组件样式模式

```svelte
<script>
  export let variant = 'primary'
</script>

<button class="btn btn-{variant}">
  <slot />
</button>

<style>
  .btn {
    border-radius: 8px;
    padding: 0.875rem 2rem;
    font-weight: 500;
    transition: all 250ms ease-in-out;
  }

  .btn-primary {
    background-color: var(--color-primary);
    color: white;
  }

  .btn-primary:hover {
    filter: brightness(0.9);
  }
</style>
```

**提取要点：**
- 组件 prop（如 `variant`）揭示预期中的变体体系
- `var(--*)` 引用 → 回溯到 `app.css`
- transition 取值揭示交互设计哲学

## SvelteKit 布局模式

- 路由根部的 **`+layout.svelte`** —— 全局页头、页脚与字体加载
- **`+layout.ts/js`** —— 可能加载主题数据或令牌
- **`$lib/`** 目录 —— 可复用组件与共享工具

## CSS 自定义属性策略

Svelte 项目大量使用 CSS 自定义属性做主题化：

```css
/* app.css */
:root {
  --color-primary: #294056;
  --color-bg: #FCFAFA;
  --color-surface: #F5F5F5;
  --color-text: #2C2C2C;
  --color-text-muted: #6B6B6B;

  --font-heading: 'Manrope', sans-serif;
  --font-body: 'Inter', sans-serif;

  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-full: 9999px;

  --shadow-hover: 0 2px 8px rgba(0,0,0,0.06);
  --spacing-section: 5rem;
}
```

这些变量名都极有意图，把它们当作设计系统提取的地基。

## Skeleton UI / DaisyUI / Flowbite-Svelte

如果使用了组件库：
- **Skeleton UI**：主题定义在 `tailwind.config.js`，使用 Skeleton 的设计令牌体系，寻找自定义主题配置对象。
- **DaisyUI**：主题在 `tailwind.config.js` → `daisyui.themes` 数组。
- **Flowbite-Svelte**：标准 Tailwind 主题化方式。
