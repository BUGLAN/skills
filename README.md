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

共 47 个 skill，按名称排序。简介优先取 `scripts/readme-i18n.json` 的中文简介，未收录时用 `SKILL.md` 原文。

| skill | 简介 |
| --- | --- |
| [agent-browser](agent-browser/) | 面向 AI agent 的浏览器自动化 CLI。当用户需要与网站交互时使用：打开页面、填写表单、点击按钮、截图、抓取数据、测试 Web 应用，或自动化任何浏览器任务。触发场景包括「打开某网站」「填个表单」「点这个按钮」「截个图」「抓取页面数据」「测试这个页面」「登录某站点」「自动化浏览器操作」，以及任何需要程序化网页交互的任务。 |
| [apple-design](apple-design/) | Apple 的界面设计与流动、物理化动效思路，落地到 Web。适用于构建或评审手势驱动界面、弹簧动画、拖拽与滑动与面板交互、惯性滚动与可打断过渡、半透明材质与层次、字体排印（光学尺寸、字距、行距）、减弱动效设置，以及 Apple 风格界面背后的设计基础（反馈、空间一致性、克制）。 |
| [brandkit](brandkit/) | 高端的品牌视觉套件图像生成 skill：制作品牌规范板、logo 体系、识别度看板与视觉世界展示。覆盖极简、电影感、编辑风、暗色科技、奢华、文化、安全、游戏、开发者工具、消费级应用等品牌体系。擅长有意图的 logo 概念、精细构图、留白排印、强符号含义、高级 mockup、美术指导式画面与灵活网格布局。 |
| [bug-fix](bug-fix/) | 系统化验证缺陷修复的工作流，确保修复质量并防止回归（regression）。 |
| [commit-and-push](commit-and-push/) | 按 Conventional Commits 规范分析当前 git 变更、智能暂存文件、生成中文提交信息、执行提交并推送当前分支。用于用户要求“用中文提交并 push”、提到 `/commit_and_push`、或要求沿用 git-commit 逻辑但最终自动推送时。支持：(1) 根据 diff 自动判断 type 和 scope，(2) 按逻辑分组暂存文件，(3) 生成中文提交信息，(4) 安全推送当前分支，(5) 在提交失败时根据 hook 或报错修正后重新创建新提交。 |
| [commit-with-chinese](commit-with-chinese/) | 按 Conventional Commits 规范分析当前 git 变更、智能暂存文件、生成中文提交信息并执行提交。用于用户要求“用中文提交”、提到 `/commit_with_chinese`、要求沿用 git-commit 逻辑但把提交信息改成中文时。支持：(1) 根据 diff 自动判断 type 和 scope，(2) 按逻辑分组暂存文件，(3) 生成中文标题、正文和 footer，(4) 在提交失败时根据 hook 或报错修正后重新创建新提交。 |
| [commit_and_push](commit_and_push/) | 按 Conventional Commits 规范分析当前 git 变更、智能暂存文件、生成中文提交信息、执行提交并推送当前分支。用于用户要求“用中文提交并 push”、提到 `/commit_and_push`、或要求沿用 git-commit 逻辑但最终自动推送时。支持：(1) 根据 diff 自动判断 type 和 scope，(2) 按逻辑分组暂存文件，(3) 生成中文提交信息，(4) 安全推送当前分支，(5) 在提交失败时根据 hook 或报错修正后重新创建新提交。 |
| [commit_with_chinese](commit_with_chinese/) | 按 Conventional Commits 规范分析当前 git 变更、智能暂存文件、生成中文提交信息并执行提交。用于用户要求“用中文提交”、提到 `/commit_with_chinese`、要求沿用 git-commit 逻辑但把提交信息改成中文时。支持：(1) 根据 diff 自动判断 type 和 scope，(2) 按逻辑分组暂存文件，(3) 生成中文标题、正文和 footer，(4) 在提交失败时根据 hook 或报错修正后重新创建新提交。 |
| [create-readme](create-readme/) | 为当前项目创建 README.md 文件。 |
| [delete_skills](delete_skills/) | 按自然语言指令从 skills 仓库中删除一个或多个 skill，自动写入 .skillignore 忽略名单（防止下次 push 又把它带回来），刷新 README.md 技能列表，提交并推送到远端（默认 origin master）。用于用户要求「删除/移除某个 skill」「把 X 从 skills 仓库删掉」「skills 里不要 X 了」或提到 `/delete_skills`（skill 名为 `delete-skills`）时。 |
| [design-an-interface](design-an-interface/) | 用并行子 agent 为同一个模块产出多个截然不同的接口设计。适用于用户想设计 API、探索接口方案、比较模块形态，或提到「设计两次」时。 |
| [design-md](design-md/) | 分析 Stitch 项目，并把语义化设计系统沉淀成 DESIGN.md 文件。 |
| [design-system](design-system/) | 设计令牌架构、组件规范与幻灯片生成。三层令牌（原始→语义→组件）、CSS 变量、间距与字号比例、组件规范、策略型幻灯片制作。适用于设计令牌、系统化设计、符合品牌规范的演示文稿。 |
| [design-taste-frontend](design-taste-frontend/) | 反套路的 frontend skill：落地页、作品集与改版。先读需求，推断正确的设计方向，再交付不像模板生成的界面。合适时使用真实设计系统；改版先做审计；动手前有严格自检。 |
| [design-taste-frontend-v1](design-taste-frontend-v1/) | 最初的 v1 版本 taste-skill，为依赖其确切行为的项目保留。当前默认是 design-taste-frontend（v2 实验版），是一次大改写。仅在你需要完全向后兼容时使用这个 v1 安装名。 |
| [domain-modeling](domain-modeling/) | 构建并打磨项目的领域模型。适用于讨论代码库术语、编写或修改 GLOSSARY.md，或记录、修改 ADR 时。 |
| [emil-design-eng](emil-design-eng/) | 本 skill 承载 Emil Kowalski 关于界面打磨、组件设计、动效取舍，以及让软件「手感很好」的那些看不见的细节的理念。 |
| [emil-prototype](emil-prototype/) | 按你的描述做出多个真正不同的 UI 版本，配一个可视化选择器让你现场逐个翻看，并选定最合适的那一版。仅在显式调用时运行，不会自动触发。 |
| [find-animation-opportunities](find-animation-opportunities/) | 在代码库或界面中寻找「该动却没动」的地方，并否决所有不该动的。只读；它会给出带有确切数值的动效建议，但不负责实现。适用于用户问「这里可以加点动效吗」或想「让界面更有生命力」时。要修已有动效，请改用 improve-animations 或 review-animations。 |
| [find-skills](find-skills/) | 帮助用户发现并安装 agent skill：当他们问「怎么做 X」「有没有 X 的 skill」「有没有能……的 skill」，或表达想扩展能力时使用。当用户想找某个可能已作为 skill 安装的功能时，应当使用本 skill。 |
| [frontend-design](frontend-design/) | 创建有辨识度、可直接上线的生产级前端界面，设计质量高。适用于用户要求构建 Web 组件、页面、页面产物、海报或应用（例如网站、落地页、仪表盘、React 组件、HTML/CSS 布局，或美化任意 Web UI）时。产出有创意、打磨过、避免常见 AI 味的代码与界面设计。 |
| [full-output-enforcement](full-output-enforcement/) | 覆盖 LLM 默认的截断行为：强制完整生成代码、禁止占位符，并干净处理 token 上限导致的分段。适用于任何需要完整、不删减输出的任务。 |
| [git-commit](git-commit/) | 执行 git 提交：分析 Conventional Commits 信息、智能暂存文件、生成提交信息。适用于用户要求提交改动、创建 git commit，或提到 /commit 时。支持：(1) 从改动自动判断 type 与 scope，(2) 依据 diff 生成 Conventional Commit 信息，(3) 可交互指定 type、scope 与描述，(4) 智能暂存以做逻辑分组。 |
| [gpt-taste](gpt-taste/) | 顶级 UX/UI 与进阶 GSAP 动效工程。强制用 Python 驱动真随机来制造布局变化、严格遵守 AIDA 页面结构、宽版编辑式排印（禁止 6 行换行）、无缝隙 bento 网格、严格的 GSAP ScrollTrigger（固定、堆叠、擦除）、内嵌微图，以及超大的分区间距。 |
| [grill-me](grill-me/) | 对计划或设计做持续追问式拷问，直到想清楚为止。开工前先把想法压测一遍时用。 |
| [grill-with-docs](grill-with-docs/) | 对计划或设计做持续追问式拷问，并在过程中产出文档（ADR 与词汇表）。 |
| [grilling](grilling/) | 就某个计划、决策或想法持续追问用户，直到达成共识。适用于用户想对自己的思路做压力测试，或出现任何 "grill"（拷问 / 追问）类触发措辞时。 |
| [handoff](handoff/) | 把当前对话压缩成一份交接文档，好让另一个代理接着干。 |
| [high-end-visual-design](high-end-visual-design/) | 教 AI 像高端设计机构那样做设计：给出确切的字体、间距、阴影、卡片结构与动效，让网站看起来「很贵」。同时屏蔽掉那些让 AI 设计显得廉价或大众化的默认套路。 |
| [image-to-code](image-to-code/) | 面向 Codex 的顶级「图片转代码」网站 skill。对视觉要求高的 Web 任务，必须先自行生成设计图，深入分析后再尽量一致地实现网站。在 Codex 中应优先使用大尺寸、清晰的分区图片而不是压缩过的小拼版；为分区或细节视图生成全新的独立图片而不是裁剪旧图；避免偷懒式欠生成；避免「卡片套卡片再套卡片」的界面；并让首屏保持干净、留白充足、可读，且在小笔记本上也能看全。 |
| [imagegen-frontend-mobile](imagegen-frontend-mobile/) | 顶级的移动应用图像生成 skill：产出高级、原生的 App 界面概念与流程。面向 iOS、Android 与跨平台移动产品。优先保证清晰的层级、舒适的正文可读性、多屏一致性、克制的配色、不落俗套的创意方向、有质感的表面、以图为主的构图、有品味的自定义图标以及干净的手机 mockup 取景。默认把界面放进带可见边框的精致 iPhone（或同类）mockup 中，主体视觉仍聚焦在 App 内容本身。本 skill 只生成图片，不写代码。 |
| [imagegen-frontend-web](imagegen-frontend-web/) | 顶级的前端图像方向 skill：生成高级、面向转化的网站设计参考图。关键输出规则——每一个分区生成一张独立的横向图；8 个分区的落地页就产出 8 张图；绝不把多个分区压缩进一张图。强制构图多样（不总是左文右图）、背景图自由、CTA 有变化、首屏尺度有变化（巨型、中型、极简小型）、有叙事概念主线、有值得再看一眼的细节，并且所有图片共用一套一致配色。针对落地页、营销站与产品稿优化，便于开发者或编码模型准确还原。 |
| [improve-animations](improve-animations/) | 以资深动效顾问的视角审视代码库中的动画与动效代码，产出按优先级排序的审计报告，以及供其他 agent（或更便宜的模型）执行的自包含实现方案。对源码只读——它只规划改进，不落地实施。适用于用户说「改进动效」「审计动效」「让这个应用手感更好」，或想要一份动效改造路线图而不是单个 diff 的评审时。 |
| [industrial-brutalist-ui](industrial-brutalist-ui/) | 粗粝的机械感界面：把瑞士平面排印与军用终端美学熔在一起。刚性网格、极端的字号对比、功利主义配色、模拟信号劣化效果。适合需要「解密蓝图」气质的数据密集型仪表盘、作品集或编辑型站点。 |
| [minimalist-ui](minimalist-ui/) | 干净的编辑风界面：温暖的单色调、排印对比、扁平 bento 网格、低饱和粉彩。不用渐变，不用重阴影。 |
| [opennote-ingest](opennote-ingest/) | 把 Agent 生成的 Markdown 文档入库到本机 Opennote 笔记本。当用户说「入库」「存进我的笔记」「存进 Opennote」「把这些文档归档到笔记」「剪藏到 Opennote」时使用。默认投递到 Opennote 收件箱等用户确认，绝不改写或覆盖既有笔记。 |
| [product-brainstorming](product-brainstorming/) | 作为思考搭档一起头脑风暴产品想法、探索问题空间并挑战既有假设。适用于探索新机会、为产品问题生成方案、压力测试某个想法，或产品经理需要在收敛方向前把想法说出口时。 |
| [prototype](prototype/) | 做一个用完即弃的原型来回答设计问题。适用于用户想验证某个状态模型或逻辑是否顺手，或想看看界面应该长什么样时。 |
| [pull_skills](pull_skills/) | 从远端拉取 skills 仓库最新内容，并把本机缺失的 skill 安装到本机 skills 目录（优先软链接，用户要求或系统不支持时才复制）。用于用户要求「拉取/同步 skills 到本机」「在新设备上装好 skills」或提到 `/pull_skills`（skill 名为 `pull-skills`）时。默认 origin master；仓库工作区有未提交改动时立即停止并告知用户，不做任何覆盖；本机有、仓库没有的 skill 一律不动。 |
| [push_skills](push_skills/) | 把本机 skills 目录中的 skill 同步进 skills 仓库（新增与更新都自动纳入），自动刷新 README.md 技能列表，提交并推送到远端（默认 origin master）。用于用户要求「把本机 skills 同步/推送上去」「推送到 GitHub」或提到 `/push_skills`（skill 名为 `push-skills`）时。支持：(1) 只处理含 SKILL.md 的 skill 目录，本机其它内容不关心；(2) 本机独有 skill 默认作为「新增」同步，本机更新过的 skill 默认先用 fetch 校验远端没有领先，然后自动覆盖仓库版本；(3) 远端领先或 fetch 失败时停下提示，不冒进；(4) 中文 Conventional Commits 提交；(5) 推送失败时保留本地提交并如实汇报；(6) README 简介保持全中文——缺中文时由 agent 译好写进 scripts/readme-i18n.json，绝不修改 skill 自己的 description；(7) 遵守 .skillignore 黑名单：名单内的 skill 不新增、不更新、不安装、不进 README，删除过的 skill 因此不会被重新上传。 |
| [redesign-existing-projects](redesign-existing-projects/) | 把现有网站与应用升级到高级品质：审计当前设计、识别常见的 AI 套路，并在不破坏功能的前提下套用高端设计标准。适用于任何 CSS 框架或原生 CSS。 |
| [research](research/) | 针对一个问题，以高可信度的第一手来源做调研，并把结论整理成 Markdown 文件存进仓库。适用于用户想调研某个主题、收集文档或 API 事实，或把查资料的体力活交给后台 agent 时。 |
| [review-animations](review-animations/) | 以源自 Emil Kowalski 设计工程理念的高标准评审动画与动效代码。默认倾向指出问题，通过评审才算合格。 |
| [stitch-design-taste](stitch-design-taste/) | 面向 Google Stitch 的语义化设计系统 skill：生成对 agent 友好的 DESIGN.md，强制高端、反大众化的 UI 标准——严格排印、校准过的配色、非对称布局、持续微动效，以及硬件加速的性能表现。 |
| [stitch-extract-design-md](stitch-extract-design-md/) | 直接从前端源码中提取完整的设计系统（DESIGN.md）——React、Vue、Svelte、Angular、原生 HTML/CSS 或任意 Web 框架。分析组件文件、样式表、Tailwind 配置、主题定义与设计令牌，产出内容丰富、兼容 Stitch 的设计系统文档。只要用户想从现有代码库反向推导设计系统、审计视觉语言、从源码提取设计令牌，或理解某个前端仓库的样式套路（哪怕只是说「这个应用长什么样」或「把这份代码里的设计抽出来」），都应当使用本 skill。 |
| [ui-ux-pro-max](ui-ux-pro-max/) | 面向 Web、移动端与桌面端的 UI/UX 设计智能。适用于设计、构建、评审或修复界面，涵盖页面、组件、设计系统、无障碍、交互、响应式布局、排印、配色、图表，以及具体技术栈的 UI 实现。可检索的本地数据：79 套风格（50 套启用）、192 个产品配色与推理画像、74 组字体搭配、119 条 UX 规范、105 个图标、17 个 GSAP 预设、25 种图表类型、22 个技术栈。 |
| [watchdog](watchdog/) | 使用于用户明确输入 "/watchdog" 或明确要求在代码修改完成后执行 watchdog 记录、验证、录屏、提审流程时。 |

<!-- SKILLS:END -->
