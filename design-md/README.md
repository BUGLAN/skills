# Stitch 设计系统文档技能

## 安装

```bash
npx skills add google-labs-code/stitch-skills --skill design-md --global
```

## 示例提示词

```text
Analyze my Furniture Collection project's Home screen and generate a comprehensive DESIGN.md file documenting the design system.
```

## 技能结构

本仓库遵循 **Agent Skills** 开放标准。每个 skill 均自成一体，包含各自的逻辑、工作流与参考资料。

```text
design-md/
├── SKILL.md           — Core instructions & workflow
├── examples/          — Sample DESIGN.md outputs
└── README.md          — This file
```

## 工作原理

技能被激活后，agent 会按一套结构化的设计分析流水线工作：

1. **检索**：通过 Stitch MCP Server 获取项目屏幕、HTML 代码与设计元数据。
2. **提取**：识别设计令牌（design token），包括颜色、字体排印、间距与组件模式。
3. **转译**：把技术性的 CSS/Tailwind 数值转换为描述性的自然设计语言。
4. **综合**：按照语义设计系统格式生成完整的 DESIGN.md。
5. **对齐**：确保产出遵循 Stitch Effective Prompting Guide 的原则，以获得最佳屏幕生成效果。
