---
name: Alpine Peak
colors:
  surface: '#fcf8fa'
  surface-dim: '#dcd9db'
  surface-bright: '#fcf8fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f5'
  surface-container: '#f0edef'
  surface-container-high: '#eae7e9'
  surface-container-highest: '#e4e2e4'
  on-surface: '#1b1b1d'
  on-surface-variant: '#45464d'
  inverse-surface: '#303032'
  inverse-on-surface: '#f3f0f2'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#5c5f61'
  on-secondary: '#ffffff'
  secondary-container: '#e0e3e5'
  on-secondary-container: '#626567'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#161c22'
  on-tertiary-container: '#7e848c'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#e0e3e5'
  secondary-fixed-dim: '#c4c7c9'
  on-secondary-fixed: '#191c1e'
  on-secondary-fixed-variant: '#444749'
  tertiary-fixed: '#dde3eb'
  tertiary-fixed-dim: '#c1c7cf'
  on-tertiary-fixed: '#161c22'
  on-tertiary-fixed-variant: '#41474e'
  background: '#fcf8fa'
  on-background: '#1b1b1d'
  surface-variant: '#e4e2e4'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  body-base:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: '0'
  body-bold:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: '0'
  label-caps:
    fontFamily: Lexend
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
  stat-lg:
    fontFamily: Lexend
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  margin-mobile: 20px
  margin-desktop: 40px
---

## 品牌与风格

品牌个性是高性能、精致而可靠，为在严苛环境中追求清晰与精准的现代滑雪者而设计。视觉语言唤起山峰晶莹剔透之美，同时优先保障户外导航所必需的粗犷实用性。

设计系统运用**玻璃拟态（Glassmorphism）**营造“冰封”质感，模仿冰与压实积雪的物理特性；再辅以**高对比（High-Contrast）**理念，确保关键数据——雪道状态、天气警报——在强烈的山间日照或暴风雪的低能见度下依然清晰可读。

## 颜色

整套调色板由**深峰蓝（Deep Peak Blue）**锚定：一种深海军蓝，为白色文字与地图提供沉稳的对比。**雪粉白（Powder White）**充任主画布，让界面透出轻盈与寒意。

**安全橙（Safety Orange）**严格保留给主要 CTA、危险警示与雪道紧急封闭，确保视线第一时间锁定。**电光蓝（Electric Blue）**（即 info 状态色）用于天气更新与一般交互。雪道难度等级沿用行业标准色（绿、蓝、黑），但以高饱和度呈现，以便在白色背景上跳脱而出。

## 字体排印

字体排印系统以 **Inter** 承担核心功能文本与正文——它 x 高度出众，小字号下依然清晰。**Lexend** 用于标签与统计数字：其高度可读、富有运动感的气质，正契合速度、垂直落差这类滑雪数据的“动感”本性。

为对抗户外眩光，字重整体比一般 Web 应用更重。展示性样式用收紧的字距配粗字重，营造力量感。标签与其背景永远保持高对比配色。

## 布局与间距

该设计系统采用**流式网格（Fluid Grid）**模型，安全区宽裕。元素间距遵循严格的 4px/8px 基线韵律，以保持克制、专业的观感。

触控目标刻意放大（最小 48x48px），以照顾戴手套的用户。卡片与容器内部的 padding 保持宽裕（`lg` 或 `xl`），避免展示复杂雪道数据时界面显得拥挤。

## 层级与景深

景深靠**玻璃拟态**与背景滤镜（backdrop filter）表达，而非传统的厚重阴影。表面按透明度分层：

1. **基础层：** 实色“雪粉白”或“深峰蓝”。
2. **中间层（卡片/弹窗）：** 70% 不透明度的白色，加 20px 背景模糊，以及 1px 细“冰白（Ice）”描边（40% 不透明度的白色）。
3. **顶层（悬浮操作）：** 90% 不透明度，配一层轻微的 4px 环境阴影，把元素从模糊背景中衬出来。

由此形成“层叠寒冰”的效果：既保住视觉清晰度，又赋予 UI 高级、现代的质感。

## 形状

形状语言由现代、有机的**圆角**定义。它柔化了高对比的调色板，让应用显得亲和。

按钮、chip 等交互元素使用 `rounded-lg`（1rem）或 `rounded-xl`（1.5rem），暗示鹅卵石般的触感。地图浮层等大容器用 1rem 圆角；雪道难度的小型状态指示则可用胶囊形，一眼可辨。

## 组件

### 按钮

主按钮以实色“安全橙”或“深峰蓝”填充，配白色文字。次要操作使用高对比描边。所有按钮的最小高度必须达到 52px，保证戴手套也能顺畅操作。

### 卡片与弹窗

卡片采用玻璃拟态效果——半透明背景加 1px 白色描边。这保证下层的地图影像或照片隐约可见，维持“冰封”美学。

### 雪道状态徽章

胶囊形指示器，配高饱和度图标：绿色（Easy，初级）、蓝色（Intermediate，中级）、黑色（Expert，高级）与双黑（Double Black，极限）。图标旁必须带文字标签，确保色盲用户也能无障碍识别。

### 输入框

输入框以“云灰（Cloud Gray）”为背景，配粗底边框，聚焦时变为“电光蓝”。标签始终显示在输入框上方，确保用户在强光环境下不丢失上下文。

### 天气组件

用粗笔画图标（笔画至少 2pt）表现晴、雪、风。图标应足够大，并配 Lexend 字体标注气温与风速。
