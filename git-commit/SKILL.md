---
name: git-commit
description: '分析变更、智能暂存文件并生成 Conventional Commits 提交信息，执行 git commit。当用户要求提交变更、创建 git commit 或提到 "/commit" 时使用。支持：(1) 根据变更自动判断 type 与 scope，(2) 根据 diff 生成 Conventional Commits 提交信息，(3) 交互式提交，可选覆盖 type/scope/description，(4) 按逻辑分组智能暂存文件'
license: MIT
allowed-tools: Bash
---

# 使用 Conventional Commits 规范执行 Git 提交

## 概述

依据 Conventional Commits 规范创建标准化、语义化的 git 提交：分析实际 diff，判定合适的 type、scope 与提交信息。

## Conventional Commits 格式

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## 提交类型

| 类型       | 用途                           |
| ---------- | ------------------------------ |
| `feat`     | 新增功能                       |
| `fix`      | 修复 bug                       |
| `docs`     | 仅文档变更                     |
| `style`    | 格式/样式调整（不涉及逻辑）    |
| `refactor` | 代码重构（非新增功能或修复）   |
| `perf`     | 性能优化                       |
| `test`     | 新增/更新测试                  |
| `build`    | 构建系统/依赖变更              |
| `ci`       | CI/配置变更                    |
| `chore`    | 日常维护/杂项                  |
| `revert`   | 回滚提交                       |

## 破坏性变更

```
# Exclamation mark after type/scope
feat!: remove deprecated endpoint

# BREAKING CHANGE footer
feat: allow config to extend other configs

BREAKING CHANGE: `extends` key behavior changed
```

## 工作流程

### 1. 分析 diff

```bash
# If files are staged, use staged diff
git diff --staged

# If nothing staged, use working tree diff
git diff

# Also check status
git status --porcelain
```

### 2. 暂存文件（如需要）

若暂存区为空，或希望按不同方式分组变更：

```bash
# Stage specific files
git add path/to/file1 path/to/file2

# Stage by pattern
git add *.test.*
git add src/components/*

# Interactive staging
git add -p
```

**绝不提交机密信息**（.env、credentials.json、私钥）。

### 3. 生成提交信息

分析 diff，确定以下要素：

- **类型（Type）**：这次变更属于哪一类？
- **范围（Scope）**：影响哪个区域/模块？
- **描述（Description）**：一行概括变更内容（现在时、祈使语气，少于 72 字符）

### 4. 执行提交

```bash
# Single line
git commit -m "<type>[scope]: <description>"

# Multi-line with body/footer
git commit -m "$(cat <<'EOF'
<type>[scope]: <description>

<optional body>

<optional footer>
EOF
)"
```

## 最佳实践

- 每次提交只包含一个逻辑变更
- 使用现在时：写 "add"，不写 "added"
- 使用祈使语气：写 "fix bug"，不写 "fixes bug"
- 关联 issue：`Closes #123`、`Refs #456`
- 描述保持在 72 字符以内

## Git 安全守则

- 绝不修改 git config
- 未经用户明确要求，绝不运行破坏性命令（--force、hard reset）
- 除非用户要求，绝不跳过 hooks（--no-verify）
- 绝不向 main/master 强制推送
- 若提交因 hooks 失败，修复问题后创建新提交（不要 amend）
