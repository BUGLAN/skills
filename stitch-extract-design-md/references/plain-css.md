# 纯 CSS / SASS / Less 提取模式

适用于没有 JavaScript 框架的项目——静态站点、WordPress 主题、原生 HTML/CSS，或重度依赖 CSS 预处理器的项目。

## 文件查找顺序

1. **`index.html` / `*.html`** —— 检查 `<link>` 标签和 `<style>` 块，找出样式表引用、内联样式与字体加载。

2. **主样式表**（`style.css`、`main.css`、`app.css`）—— 最核心的 CSS 文件。关注自定义属性、基础样式与字体排印。

3. **`_variables.scss` / `_tokens.scss` / `variables.less`** —— 承载设计令牌的预处理器变量文件。

4. **`_mixins.scss`** —— 可复用的样式模式，能揭示设计惯例。

5. **组件/模块样式表** —— 各 UI 组件独立的 CSS 文件。

## CSS 自定义属性（现代 CSS）

现代原生 CSS 项目常用自定义属性定义设计系统：

```css
:root {
  /* Colors */
  --color-primary: #294056;
  --color-bg: #FCFAFA;
  --color-surface: #F5F5F5;
  --color-text: #2C2C2C;
  --color-text-secondary: #6B6B6B;
  --color-border: #E0E0E0;
  --color-success: #10B981;
  --color-error: #EF4444;

  /* Typography */
  --font-heading: 'Manrope', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-size-base: 1rem;
  --line-height-body: 1.7;

  /* Spacing */
  --spacing-xs: 0.5rem;
  --spacing-sm: 1rem;
  --spacing-md: 2rem;
  --spacing-lg: 4rem;
  --spacing-xl: 6rem;

  /* Shapes */
  --radius-button: 8px;
  --radius-card: 12px;

  /* Shadows */
  --shadow-card: 0 2px 8px rgba(0,0,0,0.06);
}
```

这是最干净的事实来源。直接提取，并为每个令牌命名。

## SASS/SCSS 令牌模式

```scss
// _variables.scss
$colors: (
  'primary': #294056,
  'background': #FCFAFA,
  'surface': #F5F5F5,
  'text': #2C2C2C,
  'text-muted': #6B6B6B,
);

$font-stack-heading: 'Manrope', sans-serif;
$font-stack-body: 'Inter', sans-serif;

$breakpoints: (
  'mobile': 768px,
  'tablet': 1024px,
  'desktop': 1280px,
);

$spacers: (
  'section': 5rem,
  'component': 2rem,
  'element': 1rem,
);
```

SASS map 本质上就是设计令牌字典，把所有值都提取出来。

## Less 变量模式

```less
@primary-color: #294056;
@bg-color: #FCFAFA;
@text-color: #2C2C2C;
@font-heading: 'Manrope', sans-serif;
@border-radius-base: 8px;
```

提取方法相同——把每个变量映射到描述性名称和角色。

## 静态站点与 WordPress

针对静态站点或 WordPress 主题：

- **WordPress**：检查 `style.css` 头部注释中的主题元数据；样式表在 `wp-content/themes/<name>/assets/css/` 下；`functions.php` 可能以 enqueue 方式引入 Google Fonts。
- **Jekyll/Hugo**：检查 `_sass/` 或 `assets/css/` 目录。
- **静态 HTML**：一切都在 CSS 文件和 `<style>` 块里。

## 内联样式扫描

对内联样式繁多的项目（遗留代码库、邮件模板）：

在 HTML 文件中搜索 `style="..."` 属性，把不重复的取值按属性类型分组：

```
background-color: #FCFAFA, #F5F5F5, #294056
color: #2C2C2C, #6B6B6B, white
border-radius: 8px, 12px
font-family: 'Manrope', 'Inter'
```

随后去重并指派角色。

## 颜色提取策略

没有显式令牌体系时，就得在所有样式表里搜寻颜色。搜索这些属性：

```
background-color:
background:
color:
border-color:
border:
outline-color:
box-shadow:
fill:
stroke:
```

收集所有不重复的 hex、`rgb()`、`rgba()` 与 `hsl()` 值。按相近程度分组（色阶接近的归为一组），再依据上下文（哪些选择器在用它们）指派角色。

## 响应式模式

在所有样式表里找 `@media` 查询。常见模式：

```css
@media (max-width: 768px) { ... }   /* Mobile-first breakpoint */
@media (min-width: 1024px) { ... }  /* Desktop enhancement */
@media (prefers-color-scheme: dark) { ... } /* Dark mode support */
```

记录所有断点，以及各断点下的内容策略（栏数变化、padding 调整、导航形态转换）。
