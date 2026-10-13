---
name: design-system
description: 令牌架构、组件规格与幻灯片生成。三层令牌（primitive→semantic→component）、CSS 变量、间距/字阶比例、组件规格、策略化幻灯片创作。适用于设计令牌、系统化设计、符合品牌规范的演示文稿。
argument-hint: "[component or token]"
license: MIT
metadata:
  author: claudekit
  version: "1.0.0"
---

# 设计系统

令牌架构、组件规格、系统化设计、幻灯片生成。

## 适用场景

- 创建设计令牌（design token）
- 定义组件状态
- 搭建 CSS 变量体系
- 制定间距/字阶比例
- 设计到开发的交接
- 配置 Tailwind 主题
- **生成幻灯片/演示文稿**

## 令牌架构

加载：`references/token-architecture.md`

### 三层结构

```
Primitive (raw values)
       ↓
Semantic (purpose aliases)
       ↓
Component (component-specific)
```

**示例：**
```css
/* Primitive */
--color-blue-600: #2563EB;

/* Semantic */
--color-primary: var(--color-blue-600);

/* Component */
--button-bg: var(--color-primary);
```

## 脚本路径

本 skill 及其 `references/` 中的脚本路径均相对于本 SKILL.md 所在目录，而非项目目录：`scripts/<file>` 指本 skill 自带的 `scripts/` 文件夹，`../<skill>/scripts/<file>` 指与之并列安装的兄弟子 skill。请基于该目录拼接完整路径（skill 加载时，Claude Code 会将其报告为该 skill 的 base 目录），并让工作目录保持在项目根目录——脚本会以此为基准读写 `docs/brand-guidelines.md`、`assets/design-tokens.json`、`src/` 等项目文件。

## 快速上手

**生成令牌：**
```bash
node scripts/generate-tokens.cjs --config tokens.json -o tokens.css
```

**校验用法：**
```bash
node scripts/validate-tokens.cjs --dir src/
```

## 参考资料

| 主题 | 文件 |
|------|------|
| 令牌架构 | `references/token-architecture.md` |
| 原始令牌 | `references/primitive-tokens.md` |
| 语义令牌 | `references/semantic-tokens.md` |
| 组件令牌 | `references/component-tokens.md` |
| 组件规格 | `references/component-specs.md` |
| 状态与变体 | `references/states-and-variants.md` |
| Tailwind 集成 | `references/tailwind-integration.md` |

## 组件规格模式

| 属性 | 默认 | 悬停 | 按下 | 禁用 |
|------|------|------|------|------|
| 背景 | primary | primary-dark | primary-darker | muted |
| 文字 | white | white | white | muted-fg |
| 边框 | none | none | none | muted-border |
| 阴影 | sm | md | none | none |

## 脚本

| 脚本 | 用途 |
|------|------|
| `generate-tokens.cjs` | 从 JSON 令牌配置生成 CSS |
| `validate-tokens.cjs` | 检查代码中的硬编码值 |
| `search-slides.py` | BM25 检索 + 上下文推荐 |
| `slide-token-validator.py` | 校验幻灯片 HTML 的令牌合规性 |
| `fetch-background.py` | 从 Pexels/Unsplash 获取图片 |

## 模板

| 模板 | 用途 |
|------|------|
| `design-tokens-starter.json` | 内置三层结构的 JSON 起步配置 |

## 集成

**与 brand 协同：**从品牌色彩/字型中提取 primitive 令牌
**与 ui-styling 协同：**组件令牌 → Tailwind 配置

**依赖 skill：**brand、ui-styling
**主要 Agent：**ui-ux-designer、frontend-developer

## 幻灯片系统

基于设计令牌 + Chart.js + 上下文决策系统，产出符合品牌规范的演示文稿。

### 事实来源

| 文件 | 用途 |
|------|------|
| `docs/brand-guidelines.md` | 品牌识别、语气与色彩 |
| `assets/design-tokens.json` | 令牌定义（primitive→semantic→component） |
| `assets/design-tokens.css` | CSS 变量（在幻灯片中引入） |
| `assets/css/slide-animations.css` | CSS 动画库 |

### 幻灯片检索（BM25）

```bash
# Basic search (auto-detect domain)
python scripts/search-slides.py "investor pitch"

# Domain-specific search
python scripts/search-slides.py "problem agitation" -d copy
python scripts/search-slides.py "revenue growth" -d chart

# Contextual search (Premium System)
python scripts/search-slides.py "problem slide" --context --position 2 --total 9
python scripts/search-slides.py "cta" --context --position 9 --prev-emotion frustration
```

### 决策系统 CSV

| 文件 | 用途 |
|------|------|
| `data/slide-strategies.csv` | 15 种 deck 结构 + 情绪弧线 + sparkline 节拍 |
| `data/slide-layouts.csv` | 25 种布局 + 组件变体 + 动画 |
| `data/slide-layout-logic.csv` | 目标 → 布局 + break_pattern 标记 |
| `data/slide-typography.csv` | 内容类型 → 字阶 |
| `data/slide-color-logic.csv` | 情绪 → 色彩处理 |
| `data/slide-backgrounds.csv` | 幻灯片类型 → 图片类别（Pexels/Unsplash） |
| `data/slide-copy.csv` | 25 种文案公式（PAS、AIDA、FAB） |
| `data/slide-charts.csv` | 25 种图表类型及 Chart.js 配置 |

### 上下文决策流程

```
1. Parse goal/context
        ↓
2. Search slide-strategies.csv → Get strategy + emotion beats
        ↓
3. For each slide:
   a. Query slide-layout-logic.csv → layout + break_pattern
   b. Query slide-typography.csv → type scale
   c. Query slide-color-logic.csv → color treatment
   d. Query slide-backgrounds.csv → image if needed
   e. Apply animation class from slide-animations.css
        ↓
4. Generate HTML with design tokens
        ↓
5. Validate with slide-token-validator.py
```

### 打破模式（Duarte Sparkline）

高端 deck 会在不同情绪间交替，以持续抓住观众：
```
"What Is" (frustration) ↔ "What Could Be" (hope)
```

系统会在 1/3 与 2/3 两个位置安排模式切换。

### 幻灯片要求

**所有幻灯片必须：**
1. 引入 `assets/design-tokens.css`——它是唯一事实来源
2. 使用 CSS 变量：`var(--color-primary)`、`var(--slide-bg)` 等
3. 图表必须使用 Chart.js（不要用纯 CSS 柱条）
4. 提供导航（键盘方向键、点击、进度条）
5. 内容居中对齐
6. 聚焦说服与转化

### Chart.js 集成

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

<canvas id="revenueChart"></canvas>
<script>
new Chart(document.getElementById('revenueChart'), {
    type: 'line',
    data: {
        labels: ['Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            data: [5, 12, 28, 45],
            borderColor: '#FF6B6B',  // Use brand coral
            backgroundColor: 'rgba(255, 107, 107, 0.1)',
            fill: true,
            tension: 0.4
        }]
    }
});
</script>
```

### 令牌合规

```css
/* CORRECT - uses token */
background: var(--slide-bg);
color: var(--color-primary);
font-family: var(--typography-font-heading);

/* WRONG - hardcoded */
background: #0D0D0D;
color: #FF6B6B;
font-family: 'Space Grotesk';
```

### 参考实现

包含全部功能的完整示例：
```
assets/designs/slides/claudekit-pitch-251223.html
```

### 命令

```bash
/slides:create "10-slide investor pitch for ClaudeKit Marketing"
```

## 最佳实践

1. 组件中绝不使用原始 hex 值——一律引用令牌
2. 语义层让主题切换（亮色/暗色）成为可能
3. 组件令牌支持逐组件定制
4. 使用 HSL 格式，便于控制透明度
5. 为每个令牌写明用途
6. **幻灯片必须引入 design-tokens.css，并只通过 var() 取值**
