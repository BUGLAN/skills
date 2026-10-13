# Angular 提取模式

Angular 项目的样式方式结构化、惯例繁多。设计系统通常栖身于 SCSS/CSS 文件，全局主题与组件级样式分离清晰。

## 文件查找顺序

1. **`angular.json`** —— 在 `projects.*.architect.build.options.styles` 下列出全局样式文件。这些是入口 CSS/SCSS 文件。

2. **`src/styles.scss` / `src/styles.css`** —— 全局样式表。CSS 自定义属性、字体引入和基础样式都住在这里。

3. **`src/theme.scss` / `src/theme/`** —— 显式的主题目录。自定义 Material/组件调色板。

4. **Tailwind 配置（`tailwind.config.js` 或 Tailwind v4 的 `@theme {}`）** —— Tailwind v3 读 `tailwind.config.js`；Tailwind v4 则在全局 CSS/SCSS（如 `src/styles.css` 或 `src/assets/tailwind.css`）中检查 `@theme {}` 块、`@custom-variant` 与 `@plugin 'tailwindcss-primeui'`，找出 CSS 自定义属性令牌（`--color-*`、`--font-*`、`--text-*`、`--breakpoint-*`）。

5. **`src/app/app.component.scss`** —— 根组件样式，可看出全局布局模式。

6. **组件 `.scss` / `.css` 文件** —— 与组件同址的样式（默认经 ViewEncapsulation 做作用域隔离）。

7. **外部模板 `.html` 文件（`src/app/**/*.component.html`）** —— 对使用 Tailwind 工具类（`bg-*`、`text-*`、`p-*`、`rounded-*`）或结构性类绑定（`[ngClass]`、`[class.*]`）的 Angular 17+ standalone 组件至关重要。只要样式用到工具类，就务必检查 `.html` 模板。

## Angular Material 主题提取

Angular Material 是最常用的组件库。其主题基于 SCSS：

```scss
// src/theme.scss
@use '@angular/material' as mat;

$primary-palette: mat.m2-define-palette(mat.$m2-teal-palette, 800);
$accent-palette: mat.m2-define-palette(mat.$m2-blue-grey-palette);
$warn-palette: mat.m2-define-palette(mat.$m2-red-palette);

$theme: mat.m2-define-light-theme((
  color: (
    primary: $primary-palette,
    accent: $accent-palette,
    warn: $warn-palette,
  ),
  typography: mat.m2-define-typography-config(
    $font-family: 'Manrope, sans-serif',
    $headline-1: mat.m2-define-typography-level(3.5rem, 4rem, 600),
    $headline-5: mat.m2-define-typography-level(1.5rem, 2rem, 500),
    $body-1: mat.m2-define-typography-level(1rem, 1.7, 400),
  ),
));

@include mat.all-component-themes($theme);
```

**要提取什么：**
- 调色板选择 → 映射到功能色角色
- 字体排印配置 → 直接对应层级章节
- 亮色还是暗色主题 → 归入氛围

若为 Angular Material 3（基于 MDC），则寻找使用新令牌体系的 `mat.define-theme()`，它依赖 `--mat-*` CSS 自定义属性。

## SCSS 变量模式

许多 Angular 项目用 SCSS 变量承载令牌：

```scss
// _variables.scss
$color-primary: #294056;
$color-background: #FCFAFA;
$color-surface: #F5F5F5;
$color-text: #2C2C2C;

$font-heading: 'Manrope', sans-serif;
$font-body: 'Inter', sans-serif;

$radius-button: 8px;
$radius-card: 12px;

$breakpoint-mobile: 768px;
$breakpoint-desktop: 1024px;

$spacing-section: 5rem;
$spacing-component: 2rem;
```

这些是显式的设计令牌，直接映射即可。

## ViewEncapsulation 与样式作用域

Angular 默认对样式做作用域隔离（类似 Vue 的 `scoped`）。扫描组件样式时：

- 留意 `:host` 选择器——它作用于组件的根元素
- `::ng-deep`（已废弃但仍有人用）——穿透封装的样式
- 跨组件反复出现的取值，即设计系统惯例

## PrimeNG / Nebular / NG-ZORRO

如果使用了组件库：
- **PrimeNG（v17/v18/v19+）**：在 `src/app.config.ts` 中寻找新版主题配置（如 `providePrimeNG({ theme: { preset: Aura, options: { darkModeSelector: '.app-dark' } } })`）。同时检查 CSS 资源里是否通过 `@plugin 'tailwindcss-primeui'` 集成了 Tailwind v4，并检查 PrimeNG 令牌定义的 CSS 自定义属性（`--primary-color`、`--surface-*`）。
- **Nebular**：`styles.scss` 中的 `nb-theme()`，配自定义主题对象。
- **NG-ZORRO（Angular 版 Ant Design）**：`ng-zorro-antd.less` 变量，或 `angular.json` 中的自定义主题配置。

## 现代 Angular（v17 - v19）的 Standalone 组件与控制流

在现代 Angular 仓库中：
- **Standalone 组件（`@Component({ standalone: true })`）**：组件不再经由 NgModule，而是直接自行导入依赖。查看组件元数据里的 `templateUrl` 与 `styleUrl(s)`，定位模板与样式文件。
- **控制流（`@if`、`@for`、`@switch`）**：分析组件密度与间距规则时，注意 `.html` 模板中条件布局和列表的组织方式。
- **Signals 与 Zoneless（`signal()`、`input()`、`computed()`、`provideZonelessChangeDetection()`）**：动态样式或主题切换常由绑定到 `[class.dark]` 或模板中自定义 CSS 类的 signal 驱动。留意 `app.config.ts` 里的全局 Provider。

## 响应式模式

检查：
- `styles.scss` 与组件样式中的 `@media` 查询
- 组件里对 Angular CDK `BreakpointObserver` 的使用
- 若配置了 Tailwind，还有其响应式前缀
- 模板中的 Angular Flex-Layout 指令（`fxLayout`、`fxFlex`）
