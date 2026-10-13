# Vue / Nuxt 提取模式

Vue 项目的样式架构别具一格：样式常与组件同置于 `<style>` 块内，Nuxt 又叠加了一层约定式目录。

## 文件查找顺序

1. **`nuxt.config.ts` / `nuxt.config.js`** —— 可能包含全局 CSS 路径、字体配置和 Tailwind/UnoCSS 模块配置。

2. **`assets/css/main.css`**（或类似文件）—— 全局样式、CSS 自定义属性与字体引入。

3. **`tailwind.config.js`**（用了 Tailwind 时）—— 同 React；直接提取自定义主题值。

4. **`plugins/vuetify.ts`**（用了 Vuetify 时）—— 主题定义，含自定义调色板与字体排印。

5. **组件 `<style>` 块** —— 与组件同址的样式（scoped 或全局）。

## 单文件组件（SFC）模式

Vue 组件把模板、脚本与样式打包在一起：

```vue
<template>
  <div class="card">
    <h2 class="card__title">{{ title }}</h2>
  </div>
</template>

<style scoped>
.card {
  background: var(--color-surface);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.card__title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
}
</style>
```

**关键提取点：**
- `var(--*)` 引用 → 回溯到全局 CSS 找实际取值
- `scoped` 样式 → 组件私有，但能看出一致的模式
- BEM 命名（`.card__title`）→ 暗示组件层级

## Vuetify 主题提取

Vuetify 项目显式定义设计系统：

```ts
// plugins/vuetify.ts
export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#294056',
          secondary: '#6B6B6B',
          background: '#FCFAFA',
          surface: '#F5F5F5',
          error: '#EF4444',
          success: '#10B981',
        }
      }
    }
  }
})
```

这就是设计系统的声明。把每个键映射到功能角色和描述性名称。

## Quasar / PrimeVue / Element Plus

这些组件库各有自己的主题体系：

- **Quasar**：`quasar.config.js` → `framework.config.brand` 存放颜色
- **PrimeVue**：`assets/` 下的 CSS 主题，或主题预设配置
- **Element Plus**：`element-variables.scss` 中的 SCSS 变量

找到覆写文件——项目独有的取值就在那里。

## CSS 作用域行为

Vue 的 `scoped` 属性通过 data 属性实现 CSS 隔离。扫描模式时要看多个组件，找出反复出现的取值（相同的 `border-radius`、相近的 `padding`、一致的颜色引用）。跨 scoped 样式反复出现的模式，就是设计系统惯例。

## Nuxt 特有模式

- **`app.vue`** 或 **`layouts/default.vue`** —— 根布局，可见全局背景、字体加载与整体结构。
- **`assets/`** —— 全局 CSS、字体与图片。
- **`composables/`** —— 可能有 `useTheme` 或 `useDesignTokens`。
- **`nuxt.config.ts`** 的 `css` 数组 —— 列出会自动注入每个页面的全局样式表。
