# Skills

我的跨设备 agent skills 中央仓库：本机 skills 由 `/push_skills` 汇入并推送到 GitHub，
新设备用 `/pull_skills` 拉取安装（优先软链接），`/delete_skills` 按自然语言从仓库移除 skill。

## 用法

| 命令 | 作用 |
| --- | --- |
| `/push_skills` | 本机 skills → 仓库 → `origin master`；新增与更新自动纳入，README 自动刷新 |
| `/pull_skills` | 远端 → 仓库 → 本机；工作区有未提交改动时立即停止并告知，优先软链接安装（Windows 回落 junction） |
| `/delete_skills` | 用自然语言指定一个或多个 skill，从仓库删除并推送，README 同步刷新 |

引擎是 [`scripts/skill_sync.py`](scripts/skill_sync.py)，只依赖 Python 3 标准库。

```bash
git clone https://github.com/BUGLAN/skills.git
python3 scripts/skill_sync.py pull      # 新设备：装好本机缺失的 skill
python3 scripts/skill_sync.py push      # 本机有新增/更新：同步回仓库并推送
python3 scripts/skill_sync.py status    # 只读诊断
python3 scripts/skill_sync.py readme    # 按仓库当前内容重新生成技能列表
```

## 技能列表

<!-- SKILLS:START -->

共 47 个 skill，按名称排序。

| skill | 简介 |
| --- | --- |
| [agent-browser](agent-browser/) | Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons,… |
| [apple-design](apple-design/) | Apple's approach to interface design and fluid, physical motion, translated for the web. … |
| [brandkit](brandkit/) | Premium brand-kit image generation skill for creating high-end brand-guidelines boards, logo systems, identity decks, and visual-world presentations. … |
| [bug-fix](bug-fix/) | Systematic workflow for verifying bug fixes to ensure quality and prevent regres... |
| [commit-and-push](commit-and-push/) | 按 Conventional Commits 规范分析当前 git 变更、智能暂存文件、生成中文提交信息、执行提交并推送当前分支。用于用户要求“用中文提交并 push”、提到 `/commit_and_push`、或要求沿用 git-commit 逻辑但最终自动推送时。 … |
| [commit-with-chinese](commit-with-chinese/) | 按 Conventional Commits 规范分析当前 git 变更、智能暂存文件、生成中文提交信息并执行提交。用于用户要求“用中文提交”、提到 `/commit_with_chinese`、要求沿用 git-commit 逻辑但把提交信息改成中文时。 … |
| [commit_and_push](commit_and_push/) | 按 Conventional Commits 规范分析当前 git 变更、智能暂存文件、生成中文提交信息、执行提交并推送当前分支。用于用户要求“用中文提交并 push”、提到 `/commit_and_push`、或要求沿用 git-commit 逻辑但最终自动推送时。 … |
| [commit_with_chinese](commit_with_chinese/) | 按 Conventional Commits 规范分析当前 git 变更、智能暂存文件、生成中文提交信息并执行提交。用于用户要求“用中文提交”、提到 `/commit_with_chinese`、要求沿用 git-commit 逻辑但把提交信息改成中文时。 … |
| [create-readme](create-readme/) | Create a README.md file for the project |
| [delete_skills](delete_skills/) | 按自然语言指令从 skills 仓库中删除一个或多个 skill，提交并推送到远端（默认 origin master），同时刷新 README.md 技能列表。 … |
| [design-an-interface](design-an-interface/) | Generate multiple radically different interface designs for a module using parallel sub-agents. … |
| [design-md](design-md/) | Analyze Stitch projects and synthesize a semantic design system into DESIGN.md files |
| [design-system](design-system/) | Token architecture, component specifications, and slide generation. Three-layer tokens (primitive→semantic→component), CSS variables, spacing/typograp… |
| [design-taste-frontend](design-taste-frontend/) | Anti-slop frontend skill for landing pages, portfolios, and redesigns. The agent reads the brief, infers the right design direction, and ships interfa… |
| [design-taste-frontend-v1](design-taste-frontend-v1/) | The original v1 taste-skill, preserved for projects depending on its exact behavior. … |
| [domain-modeling](domain-modeling/) | 构建并打磨项目的领域模型。适用于讨论代码库术语、编写或修改 GLOSSARY.md，或记录、修改 ADR 时。 |
| [emil-design-eng](emil-design-eng/) | This skill encodes Emil Kowalski's philosophy on UI polish, component design, animation decisions, and the invisible details that make software feel g… |
| [emil-prototype](emil-prototype/) | Build multiple genuinely different versions of a UI piece you describe, rendered behind a visual picker so you can flip through them live and promote… |
| [find-animation-opportunities](find-animation-opportunities/) | Search a codebase or UI for places that don't animate but should, and reject everything that shouldn't. … |
| [find-skills](find-skills/) | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or e… |
| [frontend-design](frontend-design/) | Create distinctive, production-grade frontend interfaces with high design quality. … |
| [full-output-enforcement](full-output-enforcement/) | Overrides default LLM truncation behavior. Enforces complete code generation, bans placeholder patterns, and handles token-limit splits cleanly. … |
| [git-commit](git-commit/) | Execute git commit with conventional commit message analysis, intelligent staging, and message generation. … |
| [gpt-taste](gpt-taste/) | Elite UX/UI & Advanced GSAP Motion Engineer. Enforces Python-driven true randomization for layout variance, strict AIDA page structure, wide editorial… |
| [grill-me](grill-me/) | 对计划或设计做持续追问式拷问，直到想清楚为止。开工前先把想法压测一遍时用。 |
| [grill-with-docs](grill-with-docs/) | 对计划或设计做持续追问式拷问，并在过程中产出文档（ADR 与词汇表）。 |
| [grilling](grilling/) | 就某个计划、决策或想法持续追问用户，直到达成共识。适用于用户想对自己的思路做压力测试，或出现任何 "grill"（拷问 / 追问）类触发措辞时。 |
| [handoff](handoff/) | 把当前对话压缩成一份交接文档，好让另一个代理接着干。 |
| [high-end-visual-design](high-end-visual-design/) | Teaches the AI to design like a high-end agency. Defines the exact fonts, spacing, shadows, card structures, and animations that make a website feel e… |
| [image-to-code](image-to-code/) | Elite website image-to-code skill for Codex. For visually important web tasks, it must first generate the design image(s) itself, deeply analyze them,… |
| [imagegen-frontend-mobile](imagegen-frontend-mobile/) | Elite mobile app image-generation skill for creating premium, app-native screen concepts and flows. … |
| [imagegen-frontend-web](imagegen-frontend-web/) | Elite frontend image-direction skill for generating premium, conversion-aware website design references. … |
| [improve-animations](improve-animations/) | Survey a codebase's animation and motion code as a senior motion advisor, then produce a prioritized audit and self-contained implementation plans for… |
| [industrial-brutalist-ui](industrial-brutalist-ui/) | Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics. … |
| [minimalist-ui](minimalist-ui/) | Clean editorial-style interfaces. Warm monochrome palette, typographic contrast, flat bento grids, muted pastels. No gradients, no heavy shadows. |
| [opennote-ingest](opennote-ingest/) | 把 Agent 生成的 Markdown 文档入库到本机 Opennote 笔记本。当用户说「入库」「存进我的笔记」「存进 Opennote」「把这些文档归档到笔记」「剪藏到 Opennote」时使用。默认投递到 Opennote 收件箱等用户确认，绝不改写或覆盖既有笔记。 |
| [product-brainstorming](product-brainstorming/) | Brainstorm product ideas, explore problem spaces, and challenge assumptions as a thinking partner. … |
| [prototype](prototype/) | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explor… |
| [pull_skills](pull_skills/) | 从远端拉取 skills 仓库最新内容，并把本机缺失的 skill 安装到本机 skills 目录（优先软链接，用户要求或系统不支持时才复制）。用于用户要求「拉取/同步 skills 到本机」「在新设备上装好 skills」或提到 `/pull_skills`（skill 名为 `pull-skil… |
| [push_skills](push_skills/) | 把本机 skills 目录中的 skill 同步进 skills 仓库（新增与更新都自动纳入），自动刷新 README.md 技能列表，提交并推送到远端（默认 origin master）。 … |
| [redesign-existing-projects](redesign-existing-projects/) | Upgrades existing websites and apps to premium quality. Audits current design, identifies generic AI patterns, and applies high-end design standards w… |
| [research](research/) | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. … |
| [review-animations](review-animations/) | Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy. … |
| [stitch-design-taste](stitch-design-taste/) | Semantic Design System Skill for Google Stitch. Generates agent-friendly DESIGN.md files that enforce premium, anti-generic UI standards — strict typo… |
| [stitch-extract-design-md](stitch-extract-design-md/) | Extract a comprehensive design system (DESIGN.md) directly from frontend source code — React, Vue, Svelte, Angular, plain HTML/CSS, or any web framewo… |
| [ui-ux-pro-max](ui-ux-pro-max/) | UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing interfaces, including… |
| [watchdog](watchdog/) | 使用于用户明确输入 "/watchdog" 或明确要求在代码修改完成后执行 watchdog 记录、验证、录屏、提审流程时。 |

<!-- SKILLS:END -->
