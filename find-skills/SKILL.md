---
name: find-skills
description: 当用户问「怎么做 X」「帮我找个 X 的 skill」「有没有能做 X 的 skill」，或表示想扩展 agent 能力时，帮助用户发现并安装 agent skills。当用户寻找的功能可能已存在对应的可安装 skill 时，应使用本 skill。
---

# 查找 Skills

本 skill 帮助你从开放的 agent skills 生态中发现并安装 skills。

## 何时使用本 skill

当用户出现以下情况时，使用本 skill：

- 询问「X 怎么做」，而 X 可能是已有现成 skill 的常见任务
- 说「帮我找个 X 的 skill」或「有没有做 X 的 skill」
- 询问「你能做 X 吗」，而 X 属于某种专项能力
- 表示有兴趣扩展 agent 能力
- 想搜索工具、模板或工作流
- 提到希望在某个特定领域（设计、测试、部署等）获得帮助

## Skills CLI 是什么？

Skills CLI（`npx skills`）是开放 agent skills 生态的包管理器。skill 是模块化的软件包，通过专门的知识、工作流和工具来扩展 agent 能力。

**核心命令：**

- `npx skills find [query]` - 交互式或按关键词搜索 skills
- `npx skills add <package>` - 从 GitHub 或其他来源安装 skill
- `npx skills check` - 检查 skill 更新
- `npx skills update` - 更新所有已安装的 skills

**浏览 skills：** https://skills.sh/

## 如何帮助用户查找 skills

### 第 1 步：弄清需求

用户求助时，先识别三点：

1. 领域（如 React、测试、设计、部署）
2. 具体任务（如编写测试、制作动画、审查 PR）
3. 该任务是否足够常见、很可能已有现成 skill

### 第 2 步：先查排行榜

在运行 CLI 搜索之前，先查看 [skills.sh 排行榜](https://skills.sh/)，确认该领域是否已有知名 skill。排行榜按总安装量排序，让最受欢迎、久经考验的选项一目了然。

例如，Web 开发领域的头部 skills 包括：

- `vercel-labs/agent-skills` — React、Next.js、Web 设计（每项均 100K+ 安装）
- `anthropics/skills` — 前端设计、文档处理（100K+ 安装）

### 第 3 步：搜索 skills

如果排行榜没有覆盖用户的需求，就运行 find 命令：

```bash
npx skills find [query]
```

例如：

- 用户问「怎么让我的 React 应用更快？」→ `npx skills find react performance`
- 用户问「能帮我做 PR 审查吗？」→ `npx skills find pr review`
- 用户问「我需要创建一个 changelog」→ `npx skills find changelog`

### 第 4 步：推荐前先验证质量

**不要仅凭搜索结果就推荐某个 skill。** 务必核实：

1. **安装量** — 优先选择 1K+ 安装的 skills；低于 100 的要格外谨慎。
2. **来源声誉** — 官方来源（`vercel-labs`、`anthropics`、`microsoft`）比陌生作者更可信。
3. **GitHub stars** — 查看来源仓库；来自 <100 stars 仓库的 skill 应保持怀疑。

### 第 5 步：向用户展示候选

找到相关 skills 后，向用户展示以下信息：

1. skill 名称及其用途
2. 安装量与来源
3. 可直接运行的安装命令
4. 在 skills.sh 上了解更多详情的链接

回复示例：

```
I found a skill that might help! The "react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.
(185K installs)

To install it:
npx skills add vercel-labs/agent-skills@react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### 第 6 步：主动提出安装

如果用户想继续，你可以代为安装：

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` 表示全局安装（用户级），`-y` 跳过确认提示。

## 常见 skill 分类

搜索时可以参考这些常见分类：

| 分类        | 示例查询                                 |
| ----------- | ---------------------------------------- |
| Web 开发    | react, nextjs, typescript, css, tailwind |
| 测试        | testing, jest, playwright, e2e           |
| DevOps      | deploy, docker, kubernetes, ci-cd        |
| 文档        | docs, readme, changelog, api-docs        |
| 代码质量    | review, lint, refactor, best-practices   |
| 设计        | ui, ux, design-system, accessibility     |
| 效率        | workflow, automation, git                |

## 提升搜索效果的技巧

1. **关键词要具体**：搜「react testing」比只搜「testing」效果好
2. **尝试同义替换**：「deploy」搜不到时，改试「deployment」或「ci-cd」
3. **关注热门来源**：许多 skills 来自 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills`

## 找不到 skills 时

如果没有找到相关 skills：

1. 说明没有找到现成的 skill
2. 主动提出用自身通用能力直接完成该任务
3. 建议用户用 `npx skills init` 创建自己的 skill

示例：

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```
