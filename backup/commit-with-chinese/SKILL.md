---
name: commit-with-chinese
description: 按 Conventional Commits 规范分析当前 git 变更、智能暂存文件、生成中文提交信息并执行提交。用于用户要求“用中文提交”、提到 `/commit_with_chinese`、要求沿用 git-commit 逻辑但把提交信息改成中文时。支持：(1) 根据 diff 自动判断 type 和 scope，(2) 按逻辑分组暂存文件，(3) 生成中文标题、正文和 footer，(4) 在提交失败时根据 hook 或报错修正后重新创建新提交。
---

# 中文提交

## 概述

使用 Conventional Commits 规范完成一次中文 git 提交。先分析真实 diff，再决定提交类型、作用域和中文描述，最后执行 `git commit`。

## 工作流

### 1. 检查工作区状态

先确认当前仓库状态，判断是否已有暂存内容：

```bash
git status --porcelain
git diff --staged
git diff
```

规则：

- 如果已经有暂存内容，优先基于 `git diff --staged` 生成提交信息。
- 如果没有暂存内容，基于工作区 diff 判断应该提交哪些文件。
- 不要把无关改动混进同一个提交。
- 不要提交密钥、凭证、`.env` 或其他敏感文件。

### 2. 需要时整理暂存区

如果尚未暂存，或者当前暂存分组不合理，先整理暂存区，再继续生成提交信息。

常用命令：

```bash
git add path/to/file1 path/to/file2
git add *.test.*
git add src/components/*
git add -p
```

规则：

- 只把同一逻辑改动放进同一个提交。
- 如果当前改动明显包含多个逻辑主题，优先建议拆分提交。
- 除非用户明确要求，否则不要修改 git 配置。

### 3. 生成中文 Conventional Commit 信息

提交格式：

```text
<type>[optional scope]: <中文描述>

[optional body]

[optional footer(s)]
```

根据 diff 判断以下内容：

- `type`：改动属于什么类型。
- `scope`：影响到的模块、目录或功能域。
- `description`：一句中文摘要，使用现在时、祈使语气，尽量控制在 72 个字符以内。

常见 `type` 对照：

| Type       | 含义 |
| ---------- | ---- |
| `feat`     | 新功能 |
| `fix`      | 缺陷修复 |
| `docs`     | 仅文档变更 |
| `style`    | 代码格式或样式调整，不涉及逻辑 |
| `refactor` | 重构，不新增功能也不修复缺陷 |
| `perf`     | 性能优化 |
| `test`     | 新增或更新测试 |
| `build`    | 构建系统或依赖调整 |
| `ci`       | CI 或自动化配置调整 |
| `chore`    | 维护性杂项改动 |
| `revert`   | 回滚提交 |

要求：

- `type` 和 `scope` 保持 Conventional Commits 规范，通常继续使用英文标识。
- `description`、正文、footer 说明改用中文。
- 中文描述要直接说明结果，不要写成含糊的“update stuff”一类表述。
- 如果存在破坏性变更，使用 `!` 或 `BREAKING CHANGE:` footer。

破坏性变更示例：

```text
feat(api)!: 调整配置继承行为

BREAKING CHANGE: `extends` 字段的解析顺序已改变
```

### 4. 执行提交

单行提交：

```bash
git commit -m "<type>[scope]: <中文描述>"
```

多行提交：

```bash
git commit -m "$(cat <<'EOF'
<type>[scope]: <中文描述>

<中文正文>

<中文 footer>
EOF
)"
```

规则：

- 优先给出最终会执行的提交信息，再执行提交。
- 如果仓库 hook 报错，先根据错误修复问题，再创建新的提交。
- 不要用 `--no-verify` 跳过 hook，除非用户明确要求。
- 不要 amend 旧提交，除非用户明确要求。

## 最佳实践

- 一个提交只做一件逻辑上完整的事。
- 中文描述尽量简洁，突出行为和结果。
- 正文用来补充原因、背景、兼容性说明，不要重复标题。
- 需要关联 issue 时，footer 中可写 `Closes #123`、`Refs #456`。

## Git 安全规则

- 不要修改全局或仓库级 git config。
- 不要执行破坏性命令，例如 `--force`、`reset --hard`。
- 不要在未经确认的情况下提交敏感文件。
- 如果提交失败，不要掩盖错误，先解释失败原因并修复后再重新提交。
