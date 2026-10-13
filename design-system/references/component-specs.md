# 组件规格

核心组件的详细规格，涵盖状态与变体。

## Button

### 变体

| 变体 | 背景 | 文字 | 边框 | 适用场景 |
|------|------|------|------|----------|
| default | primary | white | none | 主要操作 |
| secondary | gray-100 | gray-900 | none | 次要操作 |
| outline | transparent | foreground | border | 三级操作 |
| ghost | transparent | foreground | none | 弱化操作 |
| link | transparent | primary | none | 导航 |
| destructive | red-600 | white | none | 危险操作 |

### 尺寸

| 尺寸 | 高度 | 水平内边距 | 垂直内边距 | 字号 | 图标尺寸 |
|------|------|------------|------------|------|----------|
| sm | 32px | 12px | 6px | 14px | 16px |
| default | 40px | 16px | 8px | 14px | 18px |
| lg | 48px | 24px | 12px | 16px | 20px |
| icon | 40px | 0 | 0 | - | 18px |

### 状态

| 状态 | 背景 | 文字 | 不透明度 | 光标 |
|------|------|------|----------|------|
| default | token | token | 1 | pointer |
| hover | darker | token | 1 | pointer |
| active | darkest | token | 1 | pointer |
| focus | token | token | 1 | pointer |
| disabled | muted | muted-fg | 0.5 | not-allowed |
| loading | token | token | 0.7 | wait |

### 结构图解

```
┌─────────────────────────────────────┐
│  [icon]  Label Text  [icon]         │
└─────────────────────────────────────┘
     ↑                      ↑
  leading icon         trailing icon
```

---

## Input

### 变体

| 变体 | 说明 |
|------|------|
| default | 标准文本输入框 |
| textarea | 多行文本 |
| select | 下拉选择 |
| checkbox | 布尔开关 |
| radio | 单选 |
| switch | 开关切换 |

### 尺寸

| 尺寸 | 高度 | 内边距 | 字号 |
|------|------|--------|------|
| sm | 32px | 8px 12px | 14px |
| default | 40px | 8px 12px | 14px |
| lg | 48px | 12px 16px | 16px |

### 状态

| 状态 | 边框 | 背景 | 焦点环 |
|------|------|------|--------|
| default | gray-300 | white | none |
| hover | gray-400 | white | none |
| focus | primary | white | primary/20% |
| error | red-500 | white | red/20% |
| disabled | gray-200 | gray-100 | none |

### 结构图解

```
Label (optional)
┌─────────────────────────────────────┐
│ [icon] Placeholder/Value   [action] │
└─────────────────────────────────────┘
Helper text or error message
```

---

## Card

### 变体

| 变体 | 阴影 | 边框 | 适用场景 |
|------|------|------|----------|
| default | sm | 1px | 标准卡片 |
| elevated | lg | none | 突出内容 |
| outline | none | 1px | 轻量容器 |
| interactive | sm→md | 1px | 可点击卡片 |

### 结构图解

```
┌─────────────────────────────────────┐
│ Card Header                         │
│   Title                             │
│   Description                       │
├─────────────────────────────────────┤
│ Card Content                        │
│   Main content area                 │
│                                     │
├─────────────────────────────────────┤
│ Card Footer                         │
│   Actions                           │
└─────────────────────────────────────┘
```

### 间距

| 区域 | 内边距 |
|------|--------|
| header | 24px 24px 0 |
| content | 24px |
| footer | 0 24px 24px |
| gap | 16px |

---

## Badge

### 变体

| 变体 | 背景 | 文字 |
|------|------|------|
| default | primary | white |
| secondary | gray-100 | gray-900 |
| outline | transparent | foreground |
| destructive | red-600 | white |
| success | green-600 | white |
| warning | yellow-500 | gray-900 |

### 尺寸

| 尺寸 | 内边距 | 字号 | 高度 |
|------|--------|------|------|
| sm | 4px 8px | 11px | 20px |
| default | 4px 10px | 12px | 24px |
| lg | 6px 12px | 14px | 28px |

---

## Alert

### 变体

| 变体 | 图标 | 背景 | 边框 |
|------|------|------|------|
| default | info | gray-50 | gray-200 |
| destructive | alert | red-50 | red-200 |
| success | check | green-50 | green-200 |
| warning | warning | yellow-50 | yellow-200 |

### 结构图解

```
┌─────────────────────────────────────┐
│ [icon]  Title                    [×]│
│         Description text            │
└─────────────────────────────────────┘
```

---

## Dialog

### 尺寸

| 尺寸 | 最大宽度 | 适用场景 |
|------|----------|----------|
| sm | 384px | 简单确认 |
| default | 512px | 标准对话框 |
| lg | 640px | 复杂表单 |
| xl | 768px | 数据密集对话框 |
| full | 100% - 32px | 移动端全屏 |

### 结构图解

```
┌───────────────────────────────────────┐
│ Dialog Header                      [×]│
│   Title                               │
│   Description                         │
├───────────────────────────────────────┤
│ Dialog Content                        │
│   Scrollable if needed                │
│                                       │
├───────────────────────────────────────┤
│ Dialog Footer                         │
│                     [Cancel] [Confirm]│
└───────────────────────────────────────┘
```

---

## Table

### 行状态

| 状态 | 背景 | 适用场景 |
|------|------|----------|
| default | white | 普通行 |
| hover | gray-50 | 鼠标悬停 |
| selected | primary/10% | 选中行 |
| striped | gray-50/white | 交替条纹 |

### 单元格对齐

| 内容类型 | 对齐方式 |
|----------|----------|
| 文本 | 左对齐 |
| 数字 | 右对齐 |
| 状态/徽章 | 居中 |
| 操作 | 右对齐 |

### 间距

| 元素 | 数值 |
|------|------|
| 单元格内边距 | 12px 16px |
| 表头内边距 | 12px 16px |
| 行高（紧凑） | 40px |
| 行高（默认） | 48px |
| 行高（宽松） | 56px |
