# test_skill_sync.ps1 —— scripts/skill_sync.py 的沙箱端到端测试（Windows / PowerShell）
#
# 全部操作都在临时目录里进行（$env:TEMP\skill-sync-test\work），不会碰真实仓库与本机 skills 目录。
# 用法：pwsh -NoProfile -File scripts/test_skill_sync.ps1
# 退出码：0 全通过；1 有失败项。

$ErrorActionPreference = 'Continue'
$T = Split-Path -Parent $PSCommandPath
$W = Join-Path $env:TEMP 'skill-sync-test\work'
$ENGINE_SRC = Join-Path $T 'skill_sync.py'
$script:fail = 0
$script:pass = 0

if (-not (Test-Path $ENGINE_SRC)) { Write-Host "找不到引擎：$ENGINE_SRC" -ForegroundColor Red; exit 1 }

function Check([string]$name, $cond) {
  if ($cond) { Write-Host ("PASS  " + $name) -ForegroundColor Green; $script:pass++ }
  else { Write-Host ("FAIL  " + $name) -ForegroundColor Red; $script:fail++ }
}

function New-Skill([string]$dir, [string]$marker) {
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $name = Split-Path -Leaf $dir
  $body = "---`nname: $name`ndescription: test skill`n---`n`n$marker`n"
  Set-Content -Path (Join-Path $dir 'SKILL.md') -Value $body -Encoding utf8
}

function Run-Engine([string[]]$EngineArgs) {
  $out = & python $ENGINE_SRC @EngineArgs 2>&1 | Out-String
  return @{ code = $LASTEXITCODE; out = $out }
}

function Bare-Files([string]$bare) {
  return (& git -C $bare ls-tree -r --name-only master) -join "`n"
}

# ---------------------------------------------------------------- setup
if (Test-Path $W) { Remove-Item -Recurse -Force $W }
New-Item -ItemType Directory -Force -Path $W | Out-Null

$bare = Join-Path $W 'remote.git'
& git init --bare -b master $bare | Out-Null

$repoA = Join-Path $W 'repoA'
& git init -b master $repoA | Out-Null
& git -C $repoA config user.email 'test@example.com'
& git -C $repoA config user.name 'test'
& git -C $repoA remote add origin $bare
New-Item -ItemType Directory -Force -Path (Join-Path $repoA 'scripts') | Out-Null
Copy-Item $ENGINE_SRC (Join-Path $repoA 'scripts\skill_sync.py')
New-Skill (Join-Path $repoA 'alpha') 'repo-version'
& git -C $repoA add -A | Out-Null
& git -C $repoA commit -m 'chore: init' | Out-Null
& git -C $repoA push -u origin master | Out-Null

$homeA = Join-Path $W 'homeA\.agents\skills'
New-Skill (Join-Path $homeA 'alpha') 'local-version-edited'
New-Skill (Join-Path $homeA 'beta') 'beta-body'
New-Skill (Join-Path $homeA 'gamma') 'gamma-local-only'
New-Item -ItemType Directory -Force -Path (Join-Path $homeA 'notaskill') | Out-Null
Set-Content (Join-Path $homeA 'notaskill\readme.txt') 'not a skill' -Encoding utf8
Set-Content (Join-Path $homeA 'loose.txt') 'loose file' -Encoding utf8

Write-Host "`n=== T1: push 遇到同名不同 -> 停止提示 (dry-run) ===" -ForegroundColor Cyan
$r = Run-Engine @('push', '--repo', $repoA, '--dir', $homeA, '--dry-run')
Check 'T1 exit=2 (blocked)' ($r.code -eq 2)
Check 'T1 列出 alpha 变化' ($r.out -match 'alpha')
Check 'T1 列出 beta 新增' ($r.out -match 'beta')
Check 'T1 提示 overwrite/skip' ($r.out -match 'on-conflict=overwrite')
Check 'T1 未提交任何东西' ((& git -C $repoA rev-parse --short HEAD) -eq (& git -C $bare rev-parse --short master))

Write-Host "`n=== T2: --only-tracked 只更新仓库已有 ===" -ForegroundColor Cyan
$r = Run-Engine @('push', '--repo', $repoA, '--dir', $homeA, '--on-conflict=overwrite', '--only-tracked', '--dry-run')
Check 'T2 exit=0' ($r.code -eq 0)
Check 'T2 beta 被跳过' ($r.out -match 'only-tracked 已跳过')
Check 'T2 不写仓库' ((& git -C $bare ls-tree -r --name-only master) -notmatch 'beta')

Write-Host "`n=== T3: --only-tracked 真跑 -> 只覆盖 alpha ===" -ForegroundColor Cyan
$r = Run-Engine @('push', '--repo', $repoA, '--dir', $homeA, '--on-conflict=overwrite', '--only-tracked')
Check 'T3 exit=0' ($r.code -eq 0)
$files = Bare-Files $bare
Check 'T3 远端 alpha 已是本机版本' ((& git -C $bare show 'master:alpha/SKILL.md') -match 'local-version-edited')
Check 'T3 远端仍无 beta' ($files -notmatch 'beta')
Check 'T3 远端仍无 gamma' ($files -notmatch 'gamma')

Write-Host "`n=== T4: 默认 push 把本机新增带上去 ===" -ForegroundColor Cyan
$r = Run-Engine @('push', '--repo', $repoA, '--dir', $homeA, '--on-conflict=overwrite')
Check 'T4 exit=0' ($r.code -eq 0)
$files = Bare-Files $bare
Check 'T4 远端已有 beta' ($files -match 'beta/SKILL.md')
Check 'T4 远端已有 gamma' ($files -match 'gamma/SKILL.md')
Check 'T4 非 skill 目录未被带上 (notaskill)' ($files -notmatch 'notaskill')
Check 'T4 散落文件未被带上 (loose.txt)' ($files -notmatch 'loose')
Check 'T4 提交信息为中文 Conventional Commits' ((& git -C $repoA log -1 --pretty=%s) -match '^(feat|chore)\(skills\):')

Write-Host "`n=== T5: 再 push 应无变更 ===" -ForegroundColor Cyan
$r = Run-Engine @('push', '--repo', $repoA, '--dir', $homeA, '--on-conflict=overwrite')
Check 'T5 exit=0' ($r.code -eq 0)
Check 'T5 报告无变更' ($r.out -match '没有需要同步的变更')

Write-Host "`n=== T6: pull 到新设备 (自动解析本机目录, 软链安装) ===" -ForegroundColor Cyan
$repoB = Join-Path $W 'repoB'
& git clone -q $bare $repoB | Out-Null
& git -C $repoB config user.email 'test@example.com'
& git -C $repoB config user.name 'test'
$homeB = Join-Path $W 'homeB'
New-Item -ItemType Directory -Force -Path $homeB | Out-Null
$origProfile = $env:USERPROFILE
$env:USERPROFILE = $homeB
$r = Run-Engine @('pull', '--repo', $repoB)
$env:USERPROFILE = $origProfile
Check 'T6 exit=0' ($r.code -eq 0)
$skillsB = Join-Path $homeB '.agents\skills'
Check 'T6 自动选中 ~/.agents/skills' ($r.out -match '\.agents')
Check 'T6 alpha 已安装' (Test-Path (Join-Path $skillsB 'alpha\SKILL.md'))
Check 'T6 beta 已安装' (Test-Path (Join-Path $skillsB 'beta\SKILL.md'))
Check 'T6 gamma 已安装' (Test-Path (Join-Path $skillsB 'gamma\SKILL.md'))
$linkType = (Get-Item (Join-Path $skillsB 'alpha')).LinkType
Check "T6 安装方式是链接 (LinkType=$linkType)" ($linkType -eq 'Junction' -or $linkType -eq 'SymbolicLink')
Check 'T6 链接内容等于仓库版本' ((Get-Content (Join-Path $skillsB 'alpha\SKILL.md') -Raw) -match 'local-version-edited')

Write-Host "`n=== T7: pull 遇到未提交改动 -> 立即停止 ===" -ForegroundColor Cyan
& cmd /c rmdir "`"$(Join-Path $skillsB 'beta')`"" | Out-Null
Check 'T7 先移除 beta 以便观察是否被装回' (-not (Test-Path (Join-Path $skillsB 'beta')))
Set-Content (Join-Path $repoB 'scratch.txt') 'dirty' -Encoding utf8
$r = Run-Engine @('pull', '--repo', $repoB, '--dir', $skillsB)
Check 'T7 exit=2 (blocked)' ($r.code -eq 2)
Check 'T7 报告未提交改动' ($r.out -match '未提交改动')
Check 'T7 未安装任何东西' (-not (Test-Path (Join-Path $skillsB 'beta')))

Write-Host "`n=== T8: 干净后 pull 补齐缺失 ===" -ForegroundColor Cyan
Remove-Item (Join-Path $repoB 'scratch.txt') -Force
$r = Run-Engine @('pull', '--repo', $repoB, '--dir', $skillsB)
Check 'T8 exit=0' ($r.code -eq 0)
Check 'T8 beta 被补齐' (Test-Path (Join-Path $skillsB 'beta\SKILL.md'))

Write-Host "`n=== T9: --copy 安装 + 本机改动漂移检测 ===" -ForegroundColor Cyan
$homeC = Join-Path $W 'homeC\.agents\skills'
$r = Run-Engine @('pull', '--repo', $repoB, '--dir', $homeC, '--copy')
Check 'T9 exit=0' ($r.code -eq 0)
Check 'T9 复制安装 (非链接)' ($null -eq (Get-Item (Join-Path $homeC 'alpha')).LinkType)
Add-Content (Join-Path $homeC 'alpha\SKILL.md') "`nlocal drift"
$r = Run-Engine @('pull', '--repo', $repoB, '--dir', $homeC)
Check 'T9 漂移时 exit=2 且不覆盖' (($r.code -eq 2) -and ((Get-Content (Join-Path $homeC 'alpha\SKILL.md') -Raw) -match 'local drift'))
$r = Run-Engine @('pull', '--repo', $repoB, '--dir', $homeC, '--force')
Check 'T9 --force 后 exit=0' ($r.code -eq 0)
Check 'T9 --force 已覆盖为本仓库版本' (-not ((Get-Content (Join-Path $homeC 'alpha\SKILL.md') -Raw) -match 'local drift'))

Write-Host "`n=== T10: 本机独有 skill 全程不动 ===" -ForegroundColor Cyan
$homeD = Join-Path $W 'homeD\.agents\skills'
New-Skill (Join-Path $homeD 'delta-local-only') 'delta'
$r = Run-Engine @('pull', '--repo', $repoB, '--dir', $homeD)
Check 'T10 exit=0' ($r.code -eq 0)
Check 'T10 delta 仍在且内容未变' ((Get-Content (Join-Path $homeD 'delta-local-only\SKILL.md') -Raw) -match 'delta')
Check 'T10 报告列为本机独有' ($r.out -match 'delta-local-only')

Write-Host "`n=== T11: push 不吞掉仓库里无关的未提交改动 ===" -ForegroundColor Cyan
Set-Content (Join-Path $repoA 'unrelated.txt') 'keep me' -Encoding utf8
Set-Content (Join-Path $repoA 'scripts\note.md') 'also unrelated' -Encoding utf8
Add-Content (Join-Path $homeA 'beta\SKILL.md') "`nbeta v2"
$r = Run-Engine @('push', '--repo', $repoA, '--dir', $homeA, '--on-conflict=overwrite')
Check 'T11 exit=0' ($r.code -eq 0)
$head = (& git -C $repoA show --name-only --pretty=format: HEAD) -join "`n"
Check 'T11 提交只含被同步的 skill' (($head -match 'beta/SKILL.md') -and ($head -notmatch 'unrelated'))
Check 'T11 无关改动仍未提交' ((& git -C $repoA status --porcelain) -match 'unrelated')

Write-Host "`n=== T12: 引擎自定位仓库 + status 只读 + JSON ===" -ForegroundColor Cyan
$out = & python (Join-Path $repoA 'scripts\skill_sync.py') status --dir $homeA 2>&1 | Out-String
Check 'T12 引擎自定位到 repoA' ($out -match [regex]::Escape($repoA))
$before = (& git -C $repoA rev-parse --short HEAD)
$r = Run-Engine @('status', '--repo', $repoA, '--dir', $homeA)
Check 'T12 status exit=0' ($r.code -eq 0)
Check 'T12 status 未改动 git' ((& git -C $repoA rev-parse --short HEAD) -eq $before)
$r = Run-Engine @('push', '--repo', $repoA, '--dir', $homeA, '--json', '--dry-run')
$jsonOk = $false
try { $obj = $r.out | ConvertFrom-Json; $jsonOk = ($obj.command -eq 'push') } catch { $jsonOk = $false }
Check 'T12 --json 可解析' $jsonOk

Write-Host "`n=== T13: 引擎报错路径 (仓库不存在 / 分支不符) ===" -ForegroundColor Cyan
$r = Run-Engine @('push', '--repo', (Join-Path $W 'nope'), '--dir', $homeA)
Check 'T13 假仓库 exit=1' ($r.code -eq 1)
& git -C $repoA checkout -q -b feature-x
$r = Run-Engine @('push', '--repo', $repoA, '--dir', $homeA)
Check 'T13 分支不符 exit=2' ($r.code -eq 2)
& git -C $repoA checkout -q master

Write-Host ""
Write-Host ("RESULT: pass={0} fail={1}" -f $script:pass, $script:fail) -ForegroundColor Yellow
if ($script:fail -gt 0) { exit 1 } else { exit 0 }
