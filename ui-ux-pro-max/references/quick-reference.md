# 速查手册 —— 全部 10 个分类的完整规则集

做 UI 审查/审计时，或需要某个分类超出 SKILL.md 优先级表之外的完整清单时，加载本文件。每条规则也逐字收录在 `data/ux-guidelines.csv` / `data/app-interface.csv` 中，并可通过 `--domain ux` / `--domain web` 检索到——本文件是一份静态索引，便于快速浏览，省去一次检索往返。

## 速查

### 1. 无障碍（严重）

- `color-contrast` - 常规文本对比度最低 4.5:1（大号文本 3:1）；出自 Material Design
- `focus-states` - 交互元素要有可见焦点环（2–4px；Apple HIG、MD）
- `alt-text` - 有含义的图片要有描述性 alt 文本
- `aria-labels` - 纯图标按钮要有 aria-label；原生端用 accessibilityLabel（Apple HIG）
- `icon-context` - 语义取决于用途：可见文字旁的装饰性图标从无障碍树中隐藏；有含义的图标要有文字替代；图标控件要有可访问名称及适用状态
- `keyboard-nav` - Tab 顺序与视觉顺序一致；完整支持键盘操作（Apple HIG）
- `form-labels` - label 要配 for 属性
- `skip-links` - 为键盘用户提供跳到主内容的链接
- `heading-hierarchy` - h1→h6 依次递进，不跳级
- `color-not-only` - 不要只靠颜色传达信息（辅以图标/文字）
- `dynamic-type` - 支持系统字号缩放；文字变大时不出现截断（Apple Dynamic Type、MD）
- `reduced-motion` - 尊重 prefers-reduced-motion；用户要求时减弱/关闭动画（Apple Reduced Motion API、MD）
- `voiceover-sr` - 提供有意义的 accessibilityLabel/accessibilityHint；VoiceOver/读屏的朗读顺序合乎逻辑（Apple HIG、MD）
- `escape-routes` - 弹窗与多步流程要提供取消/返回（Apple HIG）
- `keyboard-shortcuts` - 保留系统与无障碍快捷键；为拖放提供键盘替代（Apple HIG）
- `focus-not-obscured` - 吸顶 UI、浮层与横幅不得遮挡键盘焦点控件（WCAG 2.2 AA）
- `focus-not-obscured-enhanced` - 聚焦组件要完整可见（WCAG 2.2 AAA）
- `focus-appearance` - 核查焦点指示区域与 3:1 状态对比度；仅“可见”还不够（WCAG 2.2 AAA）
- `dragging-alternative` - 每个由页面定义的拖拽操作都要有单指针与键盘替代（WCAG 2.2 AA）
- `web-target-size` - Web 指针目标需 24×24 CSS px 或有据可查的例外；不得用原生单位顶替（WCAG 2.2 AA）
- `consistent-help` - 重复出现的帮助入口在一组页面中保持相同的相对顺序（WCAG 2.2 A）
- `redundant-entry` - 同一流程内复用已填过的信息，除非确有必要重新输入（WCAG 2.2 A）
- `accessible-authentication` - 允许密码管理器与粘贴；提供无需认知负担的认证路径（WCAG 2.2 最低要求，AA）。数据集中不含增强版 AAA 条款
- `auto-rotation-controls` - 轮播与动态内容要有暂停/停止控件，聚焦或开启 reduced motion 时必须停止（WAI）
- `contextual-live-badge-updates` - 计数/状态变化要以完整、带上下文的短语播报且不移动焦点；选用一个合适的 live/status 区域，仅在必要时才用原子更新

### 2. 触控与交互（严重）

- `touch-target-size` - 最小 44×44pt（Apple）/ 48×48dp（Material）；必要时把命中区扩到视觉边界之外
- `touch-spacing` - 触控目标之间至少留 8px/8dp 间距（Apple HIG、MD）
- `hover-vs-tap` - 主交互用 click/tap；不要只依赖 hover
- `loading-buttons` - 异步操作期间禁用按钮；显示 spinner 或进度
- `error-feedback` - 错误信息清晰且贴近问题所在
- `cursor-pointer` - 可点元素加 cursor-pointer（Web）
- `gesture-conflicts` - 主内容避免横向滑动；优先纵向滚动
- `tap-delay` - 用 touch-action: manipulation 消除 300ms 延迟（Web）
- `standard-gestures` - 一致使用平台标准手势；不要重新定义（如侧滑返回、双指缩放）（Apple HIG）
- `system-gestures` - 不阻塞系统手势（控制中心、返回侧滑等）（Apple HIG）
- `press-feedback` - 按下要有视觉反馈（ripple/高亮；MD 状态层）
- `haptic-feedback` - 确认与重要操作才用触感反馈；避免滥用（Apple HIG）
- `gesture-alternative` - 不要只靠手势交互；关键操作始终提供可见控件
- `safe-area-awareness` - 主要触控目标远离刘海、灵动岛、手势条与屏幕边缘
- `no-precision-required` - 避免要求在小图标或细边上做到像素级精准点按
- `swipe-clarity` - 滑动操作要有明确的可供性或提示（箭头、标签、引导）
- `drag-threshold` - 开始拖拽前设位移阈值，避免误触发拖拽

### 3. 性能（高）

- `image-optimization` - 用 WebP/AVIF、响应式图片（srcset/sizes）；非关键资源懒加载
- `image-dimension` - 声明 width/height 或用 aspect-ratio，防止布局偏移（Core Web Vitals：CLS）
- `font-loading` - 用 font-display: swap/optional 避免不可见文本（FOIT）；预留空间减少布局偏移（MD）
- `font-preload` - 只预加载关键字体；不要对每个字重都滥用 preload
- `critical-css` - 优先首屏 CSS（内联关键 CSS 或提前加载样式表）
- `lazy-loading` - 非 hero 组件用动态导入/路由级拆分懒加载
- `bundle-splitting` - 按路由/功能拆分代码（React Suspense / Next.js dynamic），降低首屏加载与 TTI
- `third-party-scripts` - 第三方脚本用 async/defer 加载；审计并移除不必要的（MD）
- `reduce-reflows` - 避免频繁的布局读写；先批量读 DOM 再批量写
- `content-jumping` - 为异步内容预留空间，避免内容跳动（Core Web Vitals：CLS）
- `lazy-load-below-fold` - 首屏之外的图片与重型媒体用 loading="lazy"
- `virtualize-lists` - 超过 50 项的列表做虚拟化，提升内存效率与滚动性能
- `main-thread-budget` - 每帧工作量控制在约 16ms 内以稳住 60fps；重活移出主线程（HIG、MD）
- `progressive-loading` - 超过 1 秒的操作用骨架屏/shimmer，不用长时间阻塞的 spinner（Apple HIG）
- `input-latency` - 点按/滚动的输入延迟控制在约 100ms 内（Material 响应性标准）
- `tap-feedback-speed` - 点按后 100ms 内给出视觉反馈（Apple HIG）
- `debounce-throttle` - 高频事件（scroll、resize、input）用 debounce/throttle
- `offline-support` - 提供离线状态提示与基础兜底（PWA / 移动端）
- `network-fallback` - 慢网络提供降级模式（低分辨率图片、更少动画）

### 4. 风格选择（高）

- `style-match` - 风格与产品类型匹配（用 `--design-system` 获取建议）
- `consistency` - 所有页面风格一致
- `no-emoji-icons` - 用 SVG 图标（Heroicons、Lucide），不用 emoji
- `color-palette-from-product` - 配色取自产品/行业（检索 `--domain color`）
- `effects-match-style` - 阴影、模糊、圆角与所选风格一致（glass / flat / clay 等）
- `platform-adaptive` - 尊重平台惯例（iOS HIG vs Material）：导航、控件、字体、动效
- `state-clarity` - hover/按下/禁用状态视觉可辨，同时不偏离整体风格（Material 状态层）
- `elevation-consistent` - 卡片、底部面板、弹窗使用一致的 elevation/阴影刻度；避免随机的阴影值
- `dark-mode-pairing` - 明暗两套变体一起设计，保证品牌、对比度与风格一致
- `icon-style-consistent` - 全产品使用同一图标集/视觉语言（描边宽度、圆角）
- `system-controls` - 优先原生/系统控件而非完全自绘；只有品牌需要时才定制（Apple HIG）
- `blur-purpose` - 模糊用于暗示背后内容已被弱化（弹窗、底部面板），不做装饰（Apple HIG）
- `primary-action` - 每屏只有一个主 CTA；次级操作在视觉上居次（Apple HIG）

### 5. 布局与响应式（高）

- `viewport-meta` - width=device-width initial-scale=1（绝不禁用缩放）
- `mobile-first` - 先做移动端设计，再扩展到平板与桌面
- `breakpoint-consistency` - 使用体系化断点（如 375 / 768 / 1024 / 1440）
- `readable-font-size` - 移动端正文最小 16px（避免 iOS 自动放大）
- `line-length-control` - 移动端每行 35–60 字符；桌面端 60–75 字符
- `horizontal-scroll` - 移动端无横向滚动；确保内容不超视口宽度
- `spacing-scale` - 使用 4pt/8dp 递增间距体系（Material Design）
- `touch-density` - 组件间距对触控友好：不局促，也不引发误触
- `container-width` - 桌面端容器 max-width 一致（max-w-6xl / 7xl）
- `z-index-management` - 定义分层 z-index 刻度（如 0 / 10 / 20 / 40 / 100 / 1000）
- `fixed-element-offset` - 固定导航栏/底栏要为底层内容预留安全间距
- `scroll-behavior` - 避免干扰主滚动体验的嵌套滚动区域
- `viewport-units` - 移动端优先用 min-h-dvh 而非 100vh
- `orientation-support` - 横屏下布局保持可读、可操作
- `content-priority` - 移动端先呈现核心内容；次级内容折叠或隐藏
- `visual-hierarchy` - 用尺寸、间距、对比度建立层级——不要只靠颜色
- `compact-label-overflow` - 按语义选择 badge、状态标签、过滤 chip 或可移除值；关键标签保持可用，不可避免的截断要向指针与键盘用户交代
- `chip-collection-reflow` - 先换行收纳、再缩小标签；`+n` 溢出摘要要做成可操作的展开入口，而不是把值藏起来

### 6. 字体与色彩（中）

- `line-height` - 正文行高用 1.5-1.75
- `line-length` - 每行控制在 65-75 字符
- `font-pairing` - 标题与正文的字体气质相配
- `font-scale` - 字号阶梯一致（如 12 14 16 18 24 32）
- `contrast-readability` - 浅背景配深文字（如白底配 slate-900）
- `text-styles-system` - 使用平台字体体系：iOS 11 Dynamic Type 样式 / Material 5 字体角色（display、headline、title、body、label）（HIG、MD）
- `weight-hierarchy` - 用 font-weight 强化层级：标题 Bold（600–700），正文 Regular（400），标签 Medium（500）（MD）
- `color-semantic` - 定义语义化色彩 token（primary、secondary、error、surface、on-surface），组件里不写裸 hex（Material 色彩系统）
- `color-dark-mode` - 深色模式用降饱和/更亮的色调变体，而非简单反色；对比度单独测试（HIG、MD）
- `color-accessible-pairs` - 前景/背景配对须达到 4.5:1（AA）或 7:1（AAA）；用工具核验（WCAG、MD）
- `color-not-decorative-only` - 功能色（错误红、成功绿）必须搭配图标/文字；避免只靠颜色表意（HIG、MD）
- `truncation-strategy` - 能换行不截断；确需截断时用省略号，并通过 tooltip/展开提供全文（Apple HIG）
- `letter-spacing` - 尊重各平台默认字距；正文避免过紧的字距（HIG、MD）
- `number-tabular` - 数据列、价格、计时器用等宽/表格数字（tabular figures），防止布局偏移
- `whitespace-balance` - 有目的地留白：聚拢相关项、区隔不同区块；避免视觉杂乱（Apple HIG）
- `heading-line-balance` - 短标题可用平衡换行这一由浏览器掌控的渐进式启发策略；保持自然换行的可读性，绝不用一刀切的不断行空格把结尾词强行并拢
- `long-token-wrapping` - 配合 `overflow-wrap: anywhere` 与可收缩的 flex/grid 文本子元素，让 URL、ID 和用户内容自然折行；不要对普通正文使用 `word-break: break-all`

### 7. 动画（中）

- `duration-timing` - 依据距离、复杂度、平台与用户语境选择共享动效 token；验证反馈依旧跟手，不要把某一段时长当成万能
- `transform-performance` - 只动 transform/opacity；避免动画 width/height/top/left
- `loading-states` - 反馈与预期等待时长、平台/组件指引相匹配；近瞬完成的任务别闪加载指示，长时间等待也别毫无解释
- `excessive-motion` - 每个视图最多动画 1-2 个关键元素
- `easing` - 进场用减速，退场用加速；真正匀速的进度或旋转才用线性
- `motion-meaning` - 每个动画都要表达因果关系，而不是纯装饰（Apple HIG）
- `state-transition` - 状态变化（hover / active / 展开 / 折叠 / 弹窗）应平滑过渡，不要生硬跳变
- `continuity` - 页面/屏幕转场保持空间连续性（共享元素、定向滑动）（Apple HIG）
- `parallax-subtle` - 视差克制使用；必须尊重 reduced-motion，且不引发方向迷失（Apple HIG）
- `spring-physics` - 想要自然质感，优先弹簧/物理曲线，而非线性或 cubic-bezier（Apple HIG 流畅动画）
- `exit-faster-than-enter` - 退场动画比进场短（约为进场的 60–70%），显得干脆利落（MD motion）
- `stagger-sequence` - 列表/网格项按每项 30–50ms 错峰入场；不要一拥而上，也不要拖沓（MD）
- `shared-element-transition` - 屏幕间用共享元素/hero 转场保持视觉连续（MD、HIG）
- `interruptible` - 动画必须可打断；用户点按/手势立即取消进行中的动画（Apple HIG）
- `no-blocking-animation` - 动画期间绝不阻塞输入；UI 必须保持可交互（Apple HIG）
- `fade-crossfade` - 同一容器内的内容替换用 crossfade（MD）
- `scale-feedback` - 可点卡片/按钮按下时轻微缩放（0.95–1.05），松开恢复（HIG、MD）
- `gesture-feedback` - 拖拽、滑动、双指缩放必须实时跟随手指给出视觉响应（MD Motion）
- `hierarchy-motion` - 用位移/缩放方向表达层级：自下方进场 = 进入更深层，向上方退场 = 返回上一层（MD）
- `motion-consistency` - 全局统一时长/缓动 token；所有动画共享同一节奏与质感
- `opacity-threshold` - 淡出元素不要久停在 0.2 以下透明度；要么淡净，要么保持可见
- `modal-motion` - 弹窗/底部面板应从触发源头动效出现（缩放+淡入或滑入），以保留空间线索（HIG、MD）
- `navigation-direction` - 前进导航向左/上动效，后退向右/下——方向逻辑保持一致（HIG）
- `layout-shift-avoid` - 动画不得引发布局重排或 CLS；位置变化用 transform
- `cancellable-state-transitions` - 快速连续的状态变化必须安全地取消/顶替先前的微交互，明确落到新的最终状态，且绝不依赖 animation-end 事件保证正确性

### 8. 表单与反馈（中）

- `input-labels` - 每个输入框有可见标签（不能只有 placeholder）
- `error-placement` - 具体错误显示在对应字段下方，并用 aria-describedby 关联
- `submit-feedback` - 提交后先加载态，再给成功/错误态
- `required-indicators` - 标出必填字段（如星号）
- `empty-states` - 无内容时给出有用的提示与行动
- `toast-dismiss` - toast 在 3-5 秒内自动消失
- `confirmation-dialogs` - 破坏性操作前先确认
- `input-helper-text` - 复杂输入框下方提供常驻辅助文本，而不是只靠 placeholder（Material Design）
- `disabled-states` - 禁用元素降低透明度（0.38–0.5）+ 更换光标 + 加语义属性（MD）
- `progressive-disclosure` - 复杂选项渐进展开；不要一上来就信息轰炸（Apple HIG）
- `inline-validation` - 失焦时校验（而非每次击键）；用户输完再显示错误（MD）
- `input-type-keyboard` - 用语义化 input 类型（email、tel、number）唤起正确的移动键盘（HIG、MD）
- `password-toggle` - 密码框提供显示/隐藏切换（MD）
- `autofill-support` - 用 autocomplete / textContentType 属性让系统能自动填充（HIG、MD）
- `undo-support` - 破坏性或批量操作支持撤销（如“撤销删除”toast）（Apple HIG）
- `success-feedback` - 完成的操作用简短视觉反馈确认（对勾、toast、色彩闪动）（MD）
- `error-recovery` - 错误信息必须给出清晰的恢复路径（重试、修改、帮助链接）（HIG、MD）
- `multi-step-progress` - 多步流程显示步骤指示器或进度条；允许返回上一步（MD）
- `form-autosave` - 长表单自动保存草稿，避免误关丢数据（Apple HIG）
- `sheet-dismiss-confirm` - 有未保存改动的面板/弹窗关闭前先确认（Apple HIG）
- `error-clarity` - 错误信息要说明原因 + 怎么改（不能只说“输入无效”）（HIG、MD）
- `field-grouping` - 相关字段按逻辑分组（fieldset/legend 或视觉分组）（MD）
- `read-only-distinction` - 只读状态在视觉与语义上都要区别于禁用（MD）
- `focus-management` - 多错误提交失败后聚焦错误摘要；没有摘要时聚焦第一个无效字段
- `error-summary` - 提交失败后在顶部放可聚焦的摘要，每条链接到对应无效字段，并保留字段级内联错误
- `touch-friendly-input` - 移动端输入框高度 ≥44px，满足触控目标要求（Apple HIG）
- `destructive-emphasis` - 破坏性操作用语义化危险色（红），并与主操作在视觉上分开（HIG、MD）
- `toast-accessibility` - toast 不得抢焦点；用 aria-live="polite" 供读屏播报（WCAG）
- `aria-live-errors` - 表单错误用 aria-live 区域或 role="alert" 通知读屏（WCAG）
- `contrast-feedback` - 错误与成功状态色对比度须达到 4.5:1（WCAG、MD）
- `timeout-feedback` - 请求超时要给出清晰反馈并提供重试（MD）

### 9. 导航模式（高）

- `bottom-nav-limit` - 底部导航最多 5 项；图标配文字标签（Material Design）
- `drawer-usage` - 抽屉/侧栏用于次级导航，而非主要操作（Material Design）
- `back-behavior` - 返回必须可预期且一致；保留滚动位置/状态（Apple HIG、MD）
- `deep-linking` - 所有关键页面都能通过 deep link / URL 到达，以便分享与通知落地（Apple HIG、MD）
- `tab-bar-ios` - iOS：顶层导航用底部 Tab Bar（Apple HIG）
- `top-app-bar-android` - Android：主体结构用带导航图标的 Top App Bar（Material Design）
- `nav-label-icon` - 导航项要图标 + 文字标签兼备；纯图标导航伤害可发现性（MD）
- `nav-state-active` - 当前位置在导航中要有视觉高亮（颜色、字重、指示条）（HIG、MD）
- `nav-hierarchy` - 主导航（tab/底栏）与次级导航（抽屉/设置）必须清晰分开（MD）
- `modal-escape` - 弹窗与底部面板要有明确的关闭/退出入口；移动端支持下滑关闭（Apple HIG）
- `search-accessible` - 搜索要触手可及（顶栏或 tab）；提供最近/推荐查询（MD）
- `breadcrumb-web` - Web：层级 3 级以上用面包屑帮助定位（MD）
- `state-preservation` - 返回时恢复之前的滚动位置、筛选状态与输入内容（HIG、MD）
- `gesture-nav-support` - 支持系统手势导航（iOS 侧滑返回、Android 预测性返回），互不冲突（HIG、MD）
- `tab-badge` - 导航项上的 badge 克制使用，只标未读/待处理；用户到访后清除（HIG、MD）
- `overflow-menu` - 操作放不下时用溢出/更多菜单，不要硬塞（MD）
- `bottom-nav-top-level` - 底部导航只放顶层页面；绝不在其中嵌套子导航（MD）
- `adaptive-navigation` - 大屏（≥1024px）优先侧栏；小屏用底部/顶部导航（Material Adaptive）
- `back-stack-integrity` - 绝不悄悄重置导航栈或意外跳回首页（HIG、MD）
- `navigation-consistency` - 导航位置在所有页面保持一致；不因页面类型而变
- `avoid-mixed-patterns` - 同一层级不要混用 Tab + 侧栏 + 底部导航
- `modal-vs-navigation` - 弹窗不用于主导航流程；它会打断用户的路径（HIG）
- `focus-on-route-change` - 页面切换后把焦点移到主内容区，方便读屏用户（WCAG）
- `persistent-nav` - 深层页面也要能到达核心导航；不要在子流程里完全藏起它（HIG、MD）
- `destructive-nav-separation` - 危险操作（注销账号、退出登录）要与普通导航项在视觉和位置上隔开（HIG、MD）
- `empty-nav-state` - 导航目的地不可用时说明原因，不要默默藏掉（MD）

### 10. 图表与数据（低）

- `chart-type` - 图表类型与数据类型匹配（趋势 → 折线，对比 → 柱状，占比 → 饼图/环形）
- `color-guidance` - 使用无障碍配色；避免只靠红/绿区分，照顾色觉障碍用户（WCAG、MD）
- `data-table` - 提供表格替代以保无障碍；只有图表对读屏不友好（WCAG）
- `pattern-texture` - 用图案、纹理或形状补充颜色，让数据不靠颜色也能区分（WCAG、MD）
- `legend-visible` - 始终显示图例；放在图表近旁，不要丢到首屏折叠线下（MD）
- `tooltip-on-interact` - hover（Web）或点按（移动端）时提供 tooltip/数据标签，显示精确值（HIG、MD）
- `axis-labels` - 坐标轴标注单位与可读刻度；移动端避免截断或旋转的标签
- `responsive-chart` - 图表在小屏要重排或简化（如横向柱状替代纵向、减少刻度）
- `empty-data-state` - 无数据时展示有意义的空状态（“暂无数据” + 引导），不要给一张空白图表（MD）
- `loading-chart` - 图表数据加载中用骨架屏/shimmer 占位；不要露出空坐标轴框架
- `animation-optional` - 图表入场动画必须尊重 prefers-reduced-motion；数据要立即可读（HIG）
- `large-dataset` - 1000+ 数据点时聚合或抽样；细节靠下钻查看，而不是全部渲染（MD）
- `number-formatting` - 坐标轴与标签上的数字、日期、货币按本地化格式（HIG、MD）
- `touch-target-chart` - 可交互图表元素（点、分段）要有 ≥44pt 点按区域，或触摸时放大（Apple HIG）
- `no-pie-overuse` - 超过 5 个类别不用饼图/环形图；改用柱状图更清晰
- `contrast-data` - 数据线条/柱形与背景对比 ≥3:1；数据文字标签 ≥4.5:1（WCAG）
- `legend-interactive` - 图例可点击切换系列显隐（MD）
- `direct-labeling` - 小数据集直接在图上标注数值，减少视线往返
- `tooltip-keyboard` - tooltip 内容键盘可达，不能只依赖 hover（WCAG）
- `sortable-table` - 数据表支持排序，用 aria-sort 标明当前排序状态（WCAG）
- `axis-readability` - 坐标轴刻度不拥挤；保持可读间距，小屏自动跳刻
- `data-density` - 单图信息密度有限度，避免认知过载；必要时拆成多图
- `trend-emphasis` - 强调数据趋势而非装饰；避免遮挡数据的重渐变/重阴影
- `gridline-subtle` - 网格线用低对比（如 gray-200），不与数据抢视线
- `focusable-elements` - 可交互图表元素（点、柱、扇区）必须支持键盘导航（WCAG）
- `screen-reader-summary` - 提供文字摘要或 aria-label，向读屏描述图表的关键结论（WCAG）
- `error-state-chart` - 数据加载失败要显示错误信息与重试操作，不能留下残破/空白图表
- `export-option` - 数据密集型产品提供图表数据的 CSV/图片导出
- `drill-down-consistency` - 下钻交互要保持清晰的返回路径与层级面包屑
- `time-scale-clarity` - 时间序列图要清楚标注时间粒度（日/周/月），并允许切换
