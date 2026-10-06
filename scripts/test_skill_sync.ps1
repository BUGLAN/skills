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

function Read-Utf8([string]$path) {
  return [System.IO.File]::ReadAllText($path, (New-Object System.Text.UTF8Encoding($false)))
}

function Write-Utf8([string]$path, [string]$text) {
  [System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))
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

Write-Host "`n=== T1: push --on-conflict=ask 遇到同名不同 -> 停止提示 (dry-run) ===" -ForegroundColor Cyan
$r = Run-Engine @('push', '--repo', $repoA, '--dir', $homeA, '--on-conflict=ask', '--dry-run')
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

Write-Host "`n=== T14: pull --dry-run 不触碰仓库/远端 ===" -ForegroundColor Cyan
Add-Content (Join-Path $homeA 'gamma\SKILL.md') "`ngamma v2"
$r = Run-Engine @('push', '--repo', $repoA, '--dir', $homeA, '--on-conflict=overwrite')
Check 'T14 先在 repoA 产生一个新提交并推送' ($r.code -eq 0)
$headBefore = (& git -C $repoB rev-parse HEAD).Trim()
$originBefore = (& git -C $repoB rev-parse origin/master).Trim()
Check 'T14 前提：远端领先于 repoB' ($headBefore -ne (& git -C $bare rev-parse master).Trim())
$r = Run-Engine @('pull', '--repo', $repoB, '--dir', $skillsB, '--dry-run')
Check 'T14 exit=0' ($r.code -eq 0)
Check 'T14 未改动 repoB HEAD' ((& git -C $repoB rev-parse HEAD).Trim() -eq $headBefore)
Check 'T14 未 fetch 远端 (origin/master 未前移)' ((& git -C $repoB rev-parse origin/master).Trim() -eq $originBefore)
Check 'T14 输出说明不访问远端' ($r.out -match '不访问远端')
Check 'T14 未安装/未改动本机链接' ((Get-Item (Join-Path $skillsB 'gamma')).Target -notmatch 'v2')

Write-Host "`n=== T15: push 自动生成/刷新 README ===" -ForegroundColor Cyan
$repoC = Join-Path $W 'repoC'
& git clone -q $bare $repoC | Out-Null
& git -C $repoC config user.email 'test@example.com'
& git -C $repoC config user.name 'test'
$homeF = Join-Path $W 'homeF\.agents\skills'
New-Skill (Join-Path $homeF 'zeta') 'zeta body'
New-Item -ItemType Directory -Force -Path (Join-Path $homeF 'eta') | Out-Null
Set-Content -Path (Join-Path $homeF 'eta\SKILL.md') -Value "---`nname: eta`ndescription: 带竖线 a|b 的简介`n---`n`nbody`n" -Encoding utf8
$longDesc = ('这是一段很长的中文简介，用于验证 README 不做截断。' * 8) + '结尾专属标记XYZ'
New-Item -ItemType Directory -Force -Path (Join-Path $homeF 'theta') | Out-Null
Set-Content -Path (Join-Path $homeF 'theta\SKILL.md') -Value "---`nname: theta`ndescription: $longDesc`n---`n`nbody`n" -Encoding utf8
$r = Run-Engine @('push', '--repo', $repoC, '--dir', $homeF)
Check 'T15 exit=0' ($r.code -eq 0)
$readmePath = Join-Path $repoC 'README.md'
Check 'T15 README 已生成' (Test-Path $readmePath)
$readme = Read-Utf8 $readmePath
Check 'T15 顶部含 push/pull/delete 三个命令' (($readme -match '/push_skills') -and ($readme -match '/pull_skills') -and ($readme -match '/delete_skills'))
Check 'T15 含标记区' (($readme -match '<!-- SKILLS:START -->') -and ($readme -match '<!-- SKILLS:END -->'))
Check 'T15 收录 zeta 与 eta' (($readme -match '\[zeta\]') -and ($readme -match '\[eta\]'))
Check 'T15 表格里的竖线被转义' ($readme -match 'a\\\|b')
Check 'T15 长简介不截断(尾部标记可见)' ($readme -match '结尾专属标记XYZ')
Check 'T15 长简介完整保留' ($readme -match [regex]::Escape($longDesc))
Check 'T15 提示英文简介' ($r.out -match '显示的还是英文简介')
Check 'T15 点名哪些 skill 需要补中文简介' ($r.out -match '补中文：.*zeta')
Check 'T15 提交里包含 README.md' ((& git -C $repoC show --name-only --pretty=format: HEAD) -match 'README.md')
Check 'T15 远端已有 README' ((& git -C $bare show 'master:README.md') -match '\[zeta\]')

Write-Host "`n=== T15b: README 幂等(无变更时不提交) ===" -ForegroundColor Cyan
$r = Run-Engine @('push', '--repo', $repoC, '--dir', $homeF)
Check 'T15b exit=0' ($r.code -eq 0)
Check 'T15b 报告无变更' ($r.out -match '没有需要同步的变更')

Write-Host "`n=== T15c: readme-i18n.json 提供中文简介(不动 SKILL.md) ===" -ForegroundColor Cyan
$i18nDir = Join-Path $repoC 'scripts'
New-Item -ItemType Directory -Force -Path $i18nDir | Out-Null
Set-Content -Path (Join-Path $i18nDir 'readme-i18n.json') -Value '{"zeta": {"zh": "泽塔：映射表里的中文简介", "src": "deadbeef0000"}}' -Encoding utf8
$r = Run-Engine @('readme', '--repo', $repoC)
Check 'T15c readme 刷新成功' ($r.code -eq 0)
$readme = Read-Utf8 $readmePath
Check 'T15c README 用映射表的中文简介' ($readme -match '泽塔：映射表里的中文简介')
Check 'T15c 原文变过则提示中文简介可能过期' ($r.out -match '可能过期')
Check 'T15c zeta 不再出现在待补中文列表' (-not ($r.out -match '补进映射表：.*zeta'))
Check 'T15c SKILL.md 原文未被动过' ((Read-Utf8 (Join-Path $homeF 'zeta\SKILL.md')) -match 'description: test skill')
& git -C $repoC add -A | Out-Null
& git -C $repoC commit -q -m 'chore: 添加中文简介映射表(测试)' | Out-Null
& git -C $repoC push -q origin master | Out-Null
Check 'T15c 测试仓库回到干净且与远端同步' ((& git -C $repoC status --porcelain).Length -eq 0)

Write-Host "`n=== T16: 本机更新过的 skill 自动覆盖并上传(auto) ===" -ForegroundColor Cyan
Add-Content (Join-Path $homeF 'zeta\SKILL.md') "`nzeta v2"
$r = Run-Engine @('push', '--repo', $repoC, '--dir', $homeF)
Check 'T16 exit=0(不再因内容不同而停下)' ($r.code -eq 0)
Check 'T16 远端已是更新后的内容' ((& git -C $bare show 'master:zeta/SKILL.md') -match 'zeta v2')
Check 'T16 提交信息为中文更新类型' ((& git -C $repoC log -1 --pretty=%s) -match 'chore\(skills\): 同步本机 skills 更新')
Check 'T16 输出说明了自动纳入' ($r.out -match '本机更新过的 skill 将覆盖仓库版本')

Write-Host "`n=== T17: 远端领先时停下, 拉平后可 push ===" -ForegroundColor Cyan
& git -C $repoB pull -q --ff-only origin master | Out-Null
Set-Content (Join-Path $repoB 'ahead.txt') 'from another device' -Encoding utf8
& git -C $repoB add -A | Out-Null
& git -C $repoB commit -q -m 'chore: 模拟另一台设备的提交' | Out-Null
& git -C $repoB push -q origin master | Out-Null
$headC = (& git -C $repoC rev-parse HEAD).Trim()
Add-Content (Join-Path $homeF 'zeta\SKILL.md') "`nzeta v3"
$r = Run-Engine @('push', '--repo', $repoC, '--dir', $homeF)
Check 'T17 exit=2(远端领先)' ($r.code -eq 2)
Check 'T17 未产生提交' ((& git -C $repoC rev-parse HEAD).Trim() -eq $headC)
Check 'T17 提示先 pull' ($r.out -match 'pull_skills')
$r = Run-Engine @('pull', '--repo', $repoC, '--dir', $homeF)
Check 'T17 pull 已拉平远端' ((& git -C $repoC rev-parse HEAD).Trim() -eq (& git -C $bare rev-parse master).Trim())
Check 'T17 pull 不覆盖本机已更新的 zeta, 故返回 2' ($r.code -eq 2)
Check 'T17 本机 zeta 仍是 v3' ((Read-Utf8 (Join-Path $homeF 'zeta\SKILL.md')) -match 'zeta v3')
$r = Run-Engine @('push', '--repo', $repoC, '--dir', $homeF)
Check 'T17 拉平后 auto push 成功' ($r.code -eq 0)
Check 'T17 远端已含 zeta v3' ((& git -C $bare show 'master:zeta/SKILL.md') -match 'zeta v3')

Write-Host "`n=== T18: delete 删除仓库 skill 并推送 ===" -ForegroundColor Cyan
$r = Run-Engine @('delete', '--repo', $repoC, '--dir', $homeF, 'gamma')
Check 'T18 删除已安装为链接的 skill: exit=0' ($r.code -eq 0)
Check 'T18 仓库目录已删' (-not (Test-Path (Join-Path $repoC 'gamma')))
Check 'T18 远端已无 gamma' ((Bare-Files $bare) -notmatch 'gamma/SKILL.md')
Check 'T18 本机悬空链接已清理' (-not (Test-Path (Join-Path $homeF 'gamma')))
Check 'T18 README 已移除 gamma' (-not ((Read-Utf8 $readmePath) -match '\[gamma\]'))
Check 'T18 提交信息为删除类型' ((& git -C $repoC log -1 --pretty=%s) -match 'chore\(skills\): 删除 skills')

$r = Run-Engine @('delete', '--repo', $repoC, '--dir', $homeF, 'zeta')
Check 'T18 删除本机为实体目录的 skill: exit=0' ($r.code -eq 0)
Check 'T18 仓库 zeta 已删' (-not (Test-Path (Join-Path $repoC 'zeta')))
Check 'T18 本机实体目录保留' (Test-Path (Join-Path $homeF 'zeta\SKILL.md'))
Check 'T18 输出警告会被 push 带回' ($r.out -match '重新带回仓库')
Check 'T18 README 已移除 zeta' (-not ((Read-Utf8 $readmePath) -match '\[zeta\]'))

$headBefore = (& git -C $repoC rev-parse HEAD).Trim()
$r = Run-Engine @('delete', '--repo', $repoC, '--dir', $homeF, 'nonexistent-skill')
Check 'T18 不存在的名字 exit=1' ($r.code -eq 1)
Check 'T18 未删除任何东西' ((& git -C $repoC rev-parse HEAD).Trim() -eq $headBefore)
Check 'T18 列出仓库现有 skill' ($r.out -match '仓库现有 skill')

$r = Run-Engine @('delete', '--repo', $repoC, '--dir', $homeF, 'eta', '--also-local')
Check 'T18 --also-local: exit=0' ($r.code -eq 0)
Check 'T18 --also-local 仓库已删' (-not (Test-Path (Join-Path $repoC 'eta')))
Check 'T18 --also-local 本机已删' (-not (Test-Path (Join-Path $homeF 'eta')))

Write-Host "`n=== T19: readme 子命令(校验/保留手写内容) ===" -ForegroundColor Cyan
$r = Run-Engine @('readme', '--repo', $repoC, '--check')
Check 'T19 一致时 exit=0' ($r.code -eq 0)
Add-Content -Path $readmePath -Value "`n<!-- hand-written note 12345 -->" -Encoding utf8
$r = Run-Engine @('readme', '--repo', $repoC, '--check')
Check 'T19 标记之外的手写内容不影响' ($r.code -eq 0)
$tampered = (Read-Utf8 $readmePath) -replace '\| \[alpha\]\(', '| [ghost]('
Write-Utf8 $readmePath $tampered
$r = Run-Engine @('readme', '--repo', $repoC, '--check')
Check 'T19 标记之内被篡改时 exit=2' ($r.code -eq 2)
$r = Run-Engine @('readme', '--repo', $repoC)
Check 'T19 刷新 exit=0' ($r.code -eq 0)
$after = Read-Utf8 $readmePath
Check 'T19 表格已修复(alpha 回来)' ($after -match '\[alpha\]')
Check 'T19 手写内容仍在' ($after -match 'hand-written note 12345')

Write-Host ""
Write-Host ("RESULT: pass={0} fail={1}" -f $script:pass, $script:fail) -ForegroundColor Yellow
if ($script:fail -gt 0) { exit 1 } else { exit 0 }
