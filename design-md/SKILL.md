---
name: design-md
description: 分析 Stitch 项目，把语义设计系统（semantic design system）综合成 DESIGN.md 文件
allowed-tools:
  - "stitch*:*"
  - "Read"
  - "Write"
  - "web_fetch"
---

# Stitch DESIGN.md 技能

你是一名资深设计系统负责人（Design Systems Lead）。你的目标是：分析所提供的技术资产，将其综合为一套“语义设计系统”（Semantic Design System），并写入名为 `DESIGN.md` 的文件。

## 概述

本技能帮助你创建 `DESIGN.md` 文件：它作为“事实来源”（source of truth），供你在提示 Stitch 生成新屏幕时参照，确保新屏幕与既有设计语言完美契合。Stitch 依靠“视觉描述”（Visual Descriptions）并辅以具体色值来理解设计。

## 前置条件

- 可访问 Stitch MCP Server
- 一个至少含有一个已完成设计屏幕的 Stitch 项目
- 可查阅 Stitch Effective Prompting Guide：https://stitch.withgoogle.com/docs/learn/prompting/

## 目标

`DESIGN.md` 文件将作为“事实来源”，供你在提示 Stitch 生成新屏幕时参照，确保新屏幕与既有设计语言完美契合。Stitch 依靠“视觉描述”并辅以具体色值来理解设计。

## 检索与网络获取

要分析 Stitch 项目，需使用 Stitch MCP Server 工具获取屏幕元数据与设计资产：

1. **发现命名空间**：运行 `list_tools` 找到 Stitch MCP 的前缀，后续所有调用都使用该前缀（如 `mcp_stitch:`）。

2. **查找项目**（未提供 Project ID 时）：
   - 调用 `[prefix]:list_projects` 并传入 `filter: "view=owned"`，获取用户的所有项目
   - 根据标题或 URL 模式定位目标项目
   - 从 `name` 字段提取 Project ID（如 `projects/13534454087919359824`）

3. **查找屏幕**（未提供 Screen ID 时）：
   - 调用 `[prefix]:list_screens` 并传入 `projectId`（只传数字 ID，不带完整路径）
   - 浏览各屏幕标题，定位目标屏幕（如 “Home”、“Landing Page”）
   - 从屏幕的 `name` 字段提取 Screen ID

4. **获取元数据**：
   - 调用 `[prefix]:get_screen`，同时传入 `projectId` 与 `screenId`（两者都只传数字 ID）
   - 返回完整的屏幕对象，包括：
     - `screenshot.downloadUrl` - 设计的视觉参考图
     - `htmlCode.downloadUrl` - 完整的 HTML/CSS 源码
     - `width`、`height`、`deviceType` - 屏幕尺寸与目标平台
     - 项目元数据，其中的 `designTheme` 包含颜色与风格信息

5. **下载资产**：
   - 使用 `web_fetch` 或 `read_url_content` 从 `htmlCode.downloadUrl` 下载 HTML 代码
   - 可按需从 `screenshot.downloadUrl` 下载截图作为视觉参考
   - 解析 HTML，提取 Tailwind 类名、自定义 CSS 与组件模式

6. **提取项目元数据**：
   - 调用 `[prefix]:get_project`，传入项目的 `name`（完整路径：`projects/{id}`），以获取：
     - `designTheme` 对象，含配色模式、字体、圆角与自定义颜色
     - 项目级的设计准则与描述
     - 设备类型偏好与布局原则

## 分析与综合指令

### 1. 提取项目身份信息（JSON）
- 找到项目标题
- 找到具体的 Project ID（如从 JSON 的 `name` 字段中获取）

### 2. 界定整体氛围（图片/HTML）
评估截图与 HTML 结构，把握整体“气质”。用富有画面感的形容词描述基调（如 “Airy（通透）”、“Dense（紧凑）”、“Minimalist（极简）”、“Utilitarian（务实）”）。

### 3. 映射调色板（Tailwind 配置/JSON）
识别系统中的关键颜色。每种颜色都要给出：
- 一个能传达其性格的描述性自然语言名称（如 “Deep Muted Teal-Navy（深灰调青蓝）”）
- 括号内标注的精确 hex 色值，以保证准确（如 “#294056”）
- 明确的功能角色（如 “用于主要操作”）

### 4. 转译几何与形状（CSS/Tailwind）
把技术性的 `border-radius` 与布局数值转化为具象化的描述：
- 把 `rounded-full` 描述为 “Pill-shaped（药丸形）”
- 把 `rounded-lg` 描述为 “Subtly rounded corners（圆角含蓄）”
- 把 `rounded-none` 描述为 “Sharp, squared-off edges（棱角利落）”

### 5. 描述纵深与层次
说明 UI 如何处理图层关系。描述阴影的有无与质感（如 “Flat（扁平无影）”、“Whisper-soft diffused shadows（轻若耳语的弥散阴影）”或 “Heavy, high-contrast drop shadows（浓重的高对比投影）”）。

## 输出准则

- **语言**：通篇只使用描述性的设计术语与自然语言
- **格式**：按照下述结构生成一份整洁的 Markdown 文件
- **精确性**：颜色既给出描述性名称，也附上精确的 hex 色值
- **语境**：解释设计决策背后的“为什么”，而非仅仅“是什么”

## 输出格式（DESIGN.md 结构）

```markdown
# Design System: [Project Title]
**Project ID:** [Insert Project ID Here]

## 1. Visual Theme & Atmosphere
(Description of the mood, density, and aesthetic philosophy.)

## 2. Color Palette & Roles
(List colors by Descriptive Name + Hex Code + Functional Role.)

## 3. Typography Rules
(Description of font family, weight usage for headers vs. body, and letter-spacing character.)

## 4. Component Stylings
* **Buttons:** (Shape description, color assignment, behavior).
* **Cards/Containers:** (Corner roundness description, background color, shadow depth).
* **Inputs/Forms:** (Stroke style, background).

## 5. Layout Principles
(Description of whitespace strategy, margins, and grid alignment.)
```

## 用法示例

以 Furniture Collection 项目为例使用本技能：

1. **获取项目信息：**
   ```
   Use the Stitch MCP Server to get the Furniture Collection project
   ```

2. **获取 Home 页面屏幕详情：**
   ```
   Retrieve the Home page screen's code, image, and screen object information
   ```

3. **参考最佳实践：**
   ```
   Review the Stitch Effective Prompting Guide at:
   https://stitch.withgoogle.com/docs/learn/prompting/
   ```

4. **分析并综合：**
   - 从屏幕中提取所有相关的设计令牌
   - 把技术数值转译为描述性语言
   - 按照 DESIGN.md 结构组织信息

5. **生成文件：**
   - 在项目目录下创建 `DESIGN.md`
   - 严格遵循规定格式
   - 确保所有颜色代码准确无误
   - 使用富有画面感、对设计师友好的语言

## 最佳实践

- **善用描述**：避免 “blue”、“rounded” 这类泛泛之词，要写 “Ocean-deep Cerulean (#0077B6)（深海蔚蓝）”或 “Gently curved edges（弧线柔和）”
- **讲清功能**：始终说明每个设计元素的用途
- **保持一致**：全篇沿用同一套术语
- **唤起画面**：让读者透过描述看见设计
- **力求精确**：在自然语言描述之后，用括号附上精确数值（hex 色值、像素值）

## 成功要诀

1. **先看全局**：先理解整体审美，再深入细节
2. **寻找规律**：识别一致的间距、尺寸与样式模式
3. **语义化思考**：按用途而非外观为颜色命名
4. **关注层级**：记录视觉权重与重要程度是如何传达的
5. **对照指南**：借用 Stitch Effective Prompting Guide 中的语言与模式

## 常见误区

- ❌ 直接堆砌技术行话而不加转译（如写 “rounded-xl” 而不是 “generously rounded corners（圆角宽绰）”）
- ❌ 遗漏颜色代码，或只写描述性名称
- ❌ 忘记说明设计元素的功能角色
- ❌ 氛围描述过于空泛
- ❌ 忽视阴影、间距规律等细微设计细节
