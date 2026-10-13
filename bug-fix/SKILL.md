---
name: bug-fix
description: "系统化的 bug 修复验证工作流，确保修复质量并防止回归..."
version: 1.0.0
tags: []
progressive_disclosure:
  entry_point:
    summary: "Systematic workflow for verifying bug fixes to ensure quality and prevent regres..."
    when_to_use: "When working with bug-fix or related functionality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Bug 修复验证

系统化的 bug 修复验证工作流，确保修复质量、防止回归。

## 适用场景

在以下情况使用本技能：
- 修复一个已上报的 bug
- 为 bug 修复创建 PR
- 需要记录 bug 修复的验证过程
- 想确保修复不会引入回归
- 需要一套结构化的 bug 解决流程

## Bug 修复验证为何重要

### 它解决的问题
- ❌ 修复症状而非根因
- ❌ 修旧 bug 时引入新 bug
- ❌ 边界情况测试不充分
- ❌ 无法证明 bug 确实已修复
- ❌ 修复思路缺乏文档记录

### 收益
- ✅ 确认 bug 真正修复（而非被掩盖）
- ✅ 记录根因分析
- ✅ 用测试防止回归
- ✅ 为相关方提供清晰证据
- ✅ 加深团队对代码库的理解

## Bug 修复工作流

### 第 1 步：修复前先复现

**关键**：没有先复现，就不要动手修复。

#### 复现清单
- [ ] 记录精确的复现步骤
- [ ] 用截图记录错误信息/异常行为
- [ ] 记录复现频率（100% 必现、偶发等）
- [ ] 涉及 UI 或复杂交互时录制视频
- [ ] 确认受影响的版本/环境
- [ ] 记录用户已发现的临时规避方法
- [ ] 在干净环境中验证 bug 是否存在（而不只是本地）

#### 复现记录模板
```markdown
## Bug Reproduction

### Steps to Reproduce
1. Navigate to `/dashboard`
2. Click "Export Data" button
3. Select date range: Jan 1 - Dec 31
4. Click "Generate Report"

### Expected Behavior
- Report downloads as CSV file
- File contains all transactions for date range
- Download completes in < 5 seconds

### Actual Behavior
- Error appears: "Failed to generate report"
- Console error: `TypeError: Cannot read property 'map' of undefined`
- No file downloads
- Issue occurs 100% of the time

### Environment
- Browser: Chrome 120.0.6099.109
- OS: macOS 14.2
- User Role: Admin
- Data Size: ~10,000 transactions

### Screenshots
![Error message](screenshots/export-error.png)
![Console error](screenshots/console-error.png)
```

### 第 2 步：根因分析

排查重点在于 bug 为什么会发生，而不只是发生了什么。

#### 排查步骤
1. **检查错误日志**：查看服务器日志、浏览器控制台、错误监控
2. **追踪代码路径**：从触发点一路跟踪到出错位置
3. **定位崩溃点**：找到 bug 发生的确切行/函数
4. **理解上下文**：代码为什么会这样表现？
5. **检查近期变更**：是否由最近的 commit 引入？
6. **审查相关代码**：其他地方是否存在类似模式？

#### 根因记录
```markdown
## Root Cause Analysis

### Investigation
- Error occurs in `generateReport()` function at line 45
- Function assumes `transactions` array always exists
- When date range returns no results, backend returns `null`
- Frontend doesn't handle `null` case, tries to call `.map()` on `null`

### Root Cause
- Missing null check before array operations
- Backend API doesn't return consistent data structure (sometimes `[]`, sometimes `null`)
- No validation of API response shape

### Why This Wasn't Caught
- Unit tests only covered happy path (data exists)
- Integration tests didn't test empty result scenario
- Backend inconsistency not documented in API contract
```

### 第 3 步：实施修复

修复根因，而非症状。

#### 修复准则
- **最小改动**：只修必须修的
- **防御式编码**：补充校验/守卫
- **遵循既有模式**：沿用现有的错误处理模式
- **类型安全**：借助类型防止同类 bug
- **文档**：为不直观的修复加注释

#### 修复示例
```typescript
// BEFORE (Bug)
function generateReport(transactions) {
  return transactions.map(t => ({
    date: t.date,
    amount: t.amount,
  }));
}

// AFTER (Fixed)
function generateReport(transactions) {
  // Guard against null/undefined from backend
  if (!transactions || !Array.isArray(transactions)) {
    console.warn('No transactions to export');
    return [];
  }

  return transactions.map(t => ({
    date: t.date,
    amount: t.amount,
  }));
}
```

### 第 4 步：验证修复

通过系统化测试证明 bug 已被修复。

#### 验证清单
- [ ] 按原复现步骤重新操作
- [ ] 确认 bug 不再出现
- [ ] 测试修复周边的边界情况
- [ ] 确认没有引入新错误
- [ ] 确认修复在多环境有效（dev、staging）
- [ ] 校验修复行为符合预期

#### 验证记录
```markdown
## Fix Verification

### Testing Performed
1. ✅ Followed original reproduction steps - bug no longer occurs
2. ✅ Tested with empty date range - shows "No data to export" message
3. ✅ Tested with valid date range - exports successfully
4. ✅ Tested with large dataset (50k+ transactions) - works correctly
5. ✅ Tested in Chrome, Firefox, Safari - all working
6. ✅ Tested on staging environment - fix confirmed

### Edge Cases Tested
- Empty result set → Shows appropriate message
- Null response from API → Handled gracefully
- Single transaction → Exports correctly
- Malformed transaction data → Logs error, doesn't crash

### No New Issues
- ✅ No console errors
- ✅ No memory leaks
- ✅ No performance degradation
- ✅ Other export features still work
```

### 第 5 步：添加测试防止回归

**关键**：每个 bug 修复都必须附带测试。

#### 测试要求
- [ ] 能复现原 bug 的测试（修复后应通过）
- [ ] 覆盖排查过程中发现的边界情况
- [ ] bug 涉及多个组件时补集成测试
- [ ] 需要应对新场景时更新既有测试

#### 测试示例
```typescript
describe('generateReport', () => {
  // Test that reproduces original bug
  it('should handle null transactions gracefully', () => {
    const result = generateReport(null);
    expect(result).toEqual([]);
    expect(console.warn).toHaveBeenCalledWith('No transactions to export');
  });

  // Edge cases
  it('should handle undefined transactions', () => {
    const result = generateReport(undefined);
    expect(result).toEqual([]);
  });

  it('should handle empty array', () => {
    const result = generateReport([]);
    expect(result).toEqual([]);
  });

  it('should handle single transaction', () => {
    const transactions = [{ date: '2025-01-01', amount: 100 }];
    const result = generateReport(transactions);
    expect(result).toHaveLength(1);
    expect(result[0]).toEqual({ date: '2025-01-01', amount: 100 });
  });

  // Original happy path (should still work)
  it('should transform multiple transactions correctly', () => {
    const transactions = [
      { date: '2025-01-01', amount: 100 },
      { date: '2025-01-02', amount: 200 },
    ];
    const result = generateReport(transactions);
    expect(result).toHaveLength(2);
  });
});
```

### 第 6 步：在 PR 中记录

为 bug 修复撰写完整的 PR 描述。

#### Bug 修复 PR 模板
```markdown
## Bug Fix: [Brief Description]

**Ticket**: #123 / ENG-456 / JIRA-789

### Problem
[Clear description of the bug]

### Reproduction Steps (Before Fix)
1. [Step 1]
2. [Step 2]
3. [Error occurs]

**Expected**: [What should happen]
**Actual**: [What happened instead]

### Root Cause
[Detailed explanation of why bug occurred]

- Where: `src/utils/report.ts`, line 45
- Why: Null check missing before array operation
- Impact: Affects all users trying to export with empty date ranges

### Solution
[Explanation of how fix works]

- Added null/undefined check before array operations
- Return empty array instead of crashing
- Added user-facing warning message
- Updated API response handling to be more defensive

### Fix Verification (After)
1. ✅ Followed reproduction steps - bug no longer occurs
2. ✅ Tested edge cases (null, undefined, empty array)
3. ✅ Tested across browsers (Chrome, Firefox, Safari)
4. ✅ Verified on staging environment
5. ✅ No new console errors or warnings

### Test Coverage
- Added unit tests for null/undefined handling
- Added tests for empty array edge case
- Updated integration tests for export feature
- All existing tests still passing

**Coverage**: +15 lines covered, 0 lines uncovered

### Regression Prevention
- [x] Tests added that would catch this bug if reintroduced
- [x] Similar patterns checked in codebase (found 2, fixed in this PR)
- [x] Documentation updated to note API response inconsistency

### Screenshots/Evidence
**Before (Bug)**:
![Error state](screenshots/before-error.png)

**After (Fixed)**:
![Success state](screenshots/after-success.png)
![Empty state](screenshots/after-empty.png)

### Deployment Notes
- No migrations required
- No environment variable changes
- Safe to deploy immediately
- Rollback: Revert this commit

### Related Issues
- Closes #123
- Related to #456 (similar null handling issue)
```

## 常见误区

### 排查阶段
- ❌ 不经验证就主观认定原因
- ❌ 修症状不修根因
- ❌ 不排查其他地方是否有同类 bug
- ❌ 跳过干净环境复现

### 实施阶段
- ❌ 做超出修复范围的改动
- ❌ 在 bug 修复 PR 中重构无关代码
- ❌ 修 bug 时顺手加功能
- ❌ 未处理已发现的全部边界情况

### 验证阶段
- ❌ 修复后只测正常路径
- ❌ 不在多环境下测试
- ❌ 跳过回归测试
- ❌ 不记录测试内容

### 文档阶段
- ❌ PR 描述含糊（只写"已修复 bug"）
- ❌ 不解释根因
- ❌ 缺少修复前后的对比证据
- ❌ 未链接原始 bug 报告

## Bug 修复质量标准

### 最低要求
- ✅ 找到并记录根因
- ✅ 修复最小且聚焦
- ✅ 添加测试防止回归
- ✅ 验证有据可查
- ✅ 未引入新 bug
- ✅ 在所有支持的环境下可用

### 卓越指标
- ✅ 排查并修复了同类模式
- ✅ 测试了多个边界情况
- ✅ 评估了性能影响
- ✅ 团队知识共享（更新 wiki/文档）
- ✅ 提出预防措施建议

## 自动化支持

### Bug 修复 PR 模板

创建 `.github/PULL_REQUEST_TEMPLATE/bug_fix.md`：
```markdown
## Bug Fix

**Ticket**: [Ticket number/link]

### Problem
[Description of bug]

### Reproduction Steps (Before Fix)
1.
2.
3.

**Expected**:
**Actual**:

### Root Cause
[Explanation of why bug occurred]

### Solution
[How fix works]

### Verification (After)
- [ ] Original reproduction steps no longer trigger bug
- [ ] Edge cases tested
- [ ] Tested in multiple browsers/environments
- [ ] No new errors or warnings

### Test Coverage
- [ ] Tests added for bug scenario
- [ ] Tests added for edge cases
- [ ] All existing tests passing

### Screenshots
**Before**: [Screenshot]
**After**: [Screenshot]
```

### 用于 Bug 修复 PR 的 GitHub Actions

```yaml
name: Bug Fix Verification
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  verify-bug-fix:
    if: contains(github.event.pull_request.labels.*.name, 'bug')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check PR description
        run: |
          PR_BODY="${{ github.event.pull_request.body }}"
          if [[ ! "$PR_BODY" =~ "Root Cause" ]]; then
            echo "::error::Bug fix PR must document root cause"
            exit 1
          fi
          if [[ ! "$PR_BODY" =~ "Verification" ]]; then
            echo "::error::Bug fix PR must document verification steps"
            exit 1
          fi

      - name: Run tests
        run: npm test

      - name: Check test coverage
        run: |
          COVERAGE=$(npm test -- --coverage --json | jq '.total.lines.pct')
          if (( $(echo "$COVERAGE < 90" | bc -l) )); then
            echo "::warning::Test coverage is below 90%"
          fi
```

## 成功标准

### 修复完成的判定标准
- ✅ bug 无法再复现
- ✅ 根因已弄清并记录
- ✅ 修复最小且聚焦
- ✅ 测试防止回归
- ✅ 边界情况已处理
- ✅ 在所有环境下可用
- ✅ PR 文档完整
- ✅ 未引入新问题

## 相关技能

- `universal-verification-pre-merge` - 合并前验证清单
- `universal-verification-screenshot` - UI bug 的可视化验证
- `universal-debugging-systematic-debugging` - 系统化调试方法论
- `universal-debugging-root-cause-tracing` - 根因分析技术
- `universal-testing-testing-anti-patterns` - 应避免的测试反模式
