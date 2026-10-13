# DSH 插件同步清单（本机 → 其他机器）

> 用途：把本机 DeepSeek Harness（下称 DSH）已安装的第三方插件，原样搬到另一台机器。
> 全部来自公开来源（npm / GitHub），无私有包。唯一例外：`dsh-codearts-auth` 的原始 GitHub 仓库已 404，需改用 npm 同名包（见 2.2 节）。
> 需要手工重建的只有本机配置（API Key、隧道 Token），本文件不含任何密钥。
> 生成时间：2026-10-13 ｜ 来源机器：Windows，DSH Desktop `0.2.0-rc.2`

---

## 0. TL;DR

在新机器上，插件本体分两步落地：

1. **装包**：在 profile 目录执行 `pnpm add <spec>`（或直接用 DSH 侧边栏「插件」页面逐个安装）。
2. **启用**：把包名写进 profile `package.json` 的 `dsh.profile.bundles` 数组。

只做第 1 步 = 装上了但不加载；只做第 2 步 = 找不到包直接报错。

侧边栏「插件」页面会**同时**完成这两步，所以单机零散安装优先用它；批量迁移用第 3.3 节的手工路线最可复现。

---

## 1. 环境基线

| 项目 | 本机值 | 说明 |
| --- | --- | --- |
| DSH | Desktop `0.2.0-rc.2` | 部分插件 `engines.dsh` 要求 `>=0.2.0-rc.2`，低于此版本会拒绝加载 |
| 系统 | Windows x64 | `dsh-ops` 依赖 Windows；`dsh-voice-alert` 无平台限制 |
| Node | `v22.19.0` | |
| pnpm | `11.21.0` | DSH 用 profile 自带的 pnpm 调用；手工装包请用 11.x |
| npm registry | `https://registry.npmmirror.com` | 本机 `~/.npmrc` 设为国内镜像，非必须 |
| Profile 目录 | `%USERPROFILE%\.dsh\profiles\desktop` | **桌面版用的就是这一个**，插件的 package.json / cordis.yml 都在这 |
| 次要 Profile | `%USERPROFILE%\.dsh\profiles\web` | 开发用，见第 9 节 |

Profile 目录关键文件：

```
%USERPROFILE%\.dsh\profiles\desktop\
├── package.json          # dependencies（装了哪些）+ dsh.profile.bundles（启用哪些）
├── pnpm-lock.yaml        # 锁定版本
├── pnpm-workspace.yaml   # nodeLinker / allowBuilds / minimumReleaseAgeExclude
├── cordis.yml            # 自动生成：所有 bundle 层合并后的完整加载清单（勿手改）
├── cordis.patch.yml      # 手写：本 profile 的配置覆盖层（要手改的是这个）
└── node_modules\
```

---

## 2. 插件总表

**状态说明**：`已启用` = 在 `dsh.profile.bundles` 里，当前会被加载；`已安装未启用` = 在 `dependencies` 里但不在 `bundles` 里，包在磁盘上但进程不加载它。

### 2.1 已启用的插件（7 个第三方插件；另加 2 个 DSH 基础层）

| 插件 | 版本 | 来源 spec | 许可证 | 作用 |
| --- | --- | --- | --- | --- |
| `dshmarket` | 1.66.8 | npm `^1.66.8` | MIT | DSH 可视化插件市场：浏览 / 搜索 / 一键安装社区插件 |
| `dsh-voice-alert` | 1.0.0 | GitHub `BUGLAN/dsh-voice-alert` | MIT | 任务完成或等待回复时播放提示音 + 发系统通知，带设置页（本机自研，已开源） |
| `@linxin666/dsh-usage` | 0.4.5 | npm `^0.4.5` | Apache-2.0 | 用量统计：各 provider 余额与套餐额度探测、Token 实时账本、侧边栏价格卡片 |
| `@linxin666/dsh-remote-web-ui` | 0.4.5 | npm `^0.4.5` | Apache-2.0 | 扫码配对远程访问：手机/其他电脑接入同一 Web GUI，支持 LAN 绑定与 Cloudflare 隧道 |
| `@linxin666/dsh-client-ui-web-ui-settings` | 0.4.5 | npm `^0.4.5` | Apache-2.0 | dsh-web 系插件的统一设置分区（开关 + 配置表单的宿主页） |
| `dsh-ops` | 0.2.6 | GitHub `T-Auto/dsh-ops` | MIT AND Apache-2.0 | Windows 下提供 bash / PowerShell 7 与一套 Rust 高性能工具，提升 token 效率（注册 `shell` / `file` / `background` 三行） |
| `@eddyskywalker/dsh-chatgpt-subscription` | 0.17.0 | npm `^0.17.0` | MIT | 用 ChatGPT 订阅额度接入 Codex 模型，作为 DSH 的 provider |

### 2.2 已安装但未启用的插件（6 个）

包已经在 `node_modules` 里、也已锁进 `pnpm-lock.yaml`，但没写进 `dsh.profile.bundles`，所以当前进程不加载。想用的话按第 3.4 节把它们加进 bundles 即可。

| 插件 | 版本 | 来源 spec | 许可证 | 作用 |
| --- | --- | --- | --- | --- |
| `@nanmicoder/dsh-agent-teams` | 0.1.22 | npm `0.1.22` | MIT | AgentTeams 多智能体协作：队长 / 成员 / 带依赖的任务 / 消息，自然语言驱动，Web GUI 有树状监视器 |
| `@linxin666/dsh-client-ui-task-board` | 0.4.5 | npm `^0.4.5` | Apache-2.0 | Host 权威任务看板：真实会话执行 + Host cron 定时 + 可选跨平台防休眠 |
| `dsh-synapse` | 0.4.2 | npm `^0.4.2` | MIT | 可视化、非线性的对话工作区 |
| `dsh-our-free-model` | 1.3.1 | GitHub `zouyuxuan122/dsh-our-free-model` | MIT | 免费模型聚合：免登录免 API Key 使用 Muse Spark 1.3 / MiMo V2.6 等模型，含可用性探测、Token 热力图、OpenAI 格式本地转发端口 |
| `dsh-plugin-control-your-development` | 0.4.2 | GitHub `HaoyanZhang123/dsh-plugin-control-your-development` | MIT | 把「掌控开发进度」产品仪表盘嵌进 DSH 右侧边栏（附带配套 skill） |
| `dsh-codearts-auth` | 0.4.1 | ⚠️ 原 GitHub 来源 `zhengwuji/Jet-Hub` **已失效**，改用 npm `dsh-codearts-auth@0.3.1004` | MIT | 华为云 CodeArts 浏览器登录，把临时凭证存进 `ctx.credentials`（**注意仓库名与包名不同**） |

> ⚠️ **`dsh-codearts-auth` 需要特别注意**
> 本机装的 0.4.1 来自 GitHub `zhengwuji/Jet-Hub`，该仓库**现在已 404（已删除或转私有）**，`codeload` 与 GitHub API 均返回 404。插件管理器安装前会先 `git ls-remote` 检查仓库可达性，所以在别的机器上**这条来源一定会安装失败**。
> 可用替代（npm 上同名包，同一作者线）：
> - `dsh-codearts-auth@0.3.1004` —— 描述与本机 0.4.1 完全一致（CodeArts 浏览器登录），最接近；
> - `dsh-codearts-auth@1.0.261007`（latest）—— 功能扩展为「多 AI 编程服务商账号登录 + 多账号池 + 凭证静默刷新」，版本线不同，按需选。
>
> 另外该包名与仓库名不一致（仓库叫 `Jet-Hub`），直接搜仓库名搜不到。

---

## 3. 安装方式

### 3.1 方式 A：DSH 侧边栏「插件」页面（推荐，单机零散装）

打开 Web GUI → 侧边栏 **插件** 页 → 安装 bundle → 粘贴 spec（如 `@linxin666/dsh-usage@^0.4.5`）。

插件页面会同时完成「pnpm 装包」和「写进 `dsh.profile.bundles`」两件事，并且装完默认启用。GitHub 来源在真正下载前会先做一次 `git ls-remote` 连通性检查（默认 5s 超时）。

### 3.2 方式 B：让 agent 装（`plugin_manager` 工具）

在带 `plugin_manager` 工具的会话（Creator 模式 / 支持该工具的 preset）里，直接让 agent 装：

```
帮我装这些 DSH 插件：@linxin666/dsh-usage@^0.4.5、dsh-ops@github:T-Auto/dsh-ops
```

该工具要求当前调用处于 `danger-full-access` 或通过审批。与方式 A 等价。

### 3.3 方式 C：手工迁移 profile（批量、最可复现）

适合「一次性把整机插件搬到新机器」。全程在 profile 目录里操作。

```powershell
# 0) 关掉 DSH（避免文件被占用），然后进入 profile 目录
cd $env:USERPROFILE\.dsh\profiles\desktop
```

**第 1 步：先补 `pnpm-workspace.yaml`**（否则 git 来源的包会因为构建脚本未授权直接失败，见第 8 节）

```yaml
packages:
  - .

nodeLinker: hoisted
autoInstallPeers: false
allowBuilds:
  cloudflared: true
  # 本机历史值（对应的 Jet-Hub 仓库已 404，新机器可删掉这一行）：
  # dsh-codearts-auth@https://codeload.github.com/zhengwuji/Jet-Hub/tar.gz/17f41dc3a89a4afb0d0c7253c482daa115c064ca: true
minimumReleaseAgeExclude:
  - '@linxin666/dsh-usage@0.4.5'
```

> 遇到 `ERR_PNPM_GIT_DEP_PREPARE_NOT_ALLOWED` 时，把报错里给出的**那一整串**包标识原样粘到 `allowBuilds` 下并设为 `true`（键里带 `@https://codeload.github.com/...` 的写法照抄即可）。

**第 2 步：装包**（第 4 节有完整命令）

**第 3 步：写进 bundles**

```powershell
# 把插件名追加进 dsh.profile.bundles（去重，保持已有顺序）
node -e "const fs=require('fs');const f='package.json';const p=JSON.parse(fs.readFileSync(f,'utf8'));const add=process.argv.slice(1);const b=p.dsh.profile.bundles;for(const n of add){if(!b.includes(n))b.push(n)};fs.writeFileSync(f,JSON.stringify(p,null,2)+'\n');console.log(b.join('\n'))" -- dsh-voice-alert dshmarket @linxin666/dsh-usage @linxin666/dsh-remote-web-ui @linxin666/dsh-client-ui-web-ui-settings dsh-ops @eddyskywalker/dsh-chatgpt-subscription
```

**第 4 步：重启 DSH**，然后按第 7 节验证。

> `bundles` 是**有序**的，后面的层会覆盖前面的配置。建议把基础层 `@deepseek-ai/dsh-base`、`@deepseek-ai/dsh-web-app` 留在最前，第三方插件跟在后面。

### 3.4 启用第 2.2 节那 6 个「已安装未启用」的插件

包已经在磁盘上，只要加进 bundles 再重启即可：

```powershell
cd $env:USERPROFILE\.dsh\profiles\desktop
node -e "const fs=require('fs');const f='package.json';const p=JSON.parse(fs.readFileSync(f,'utf8'));const add=process.argv.slice(1);const b=p.dsh.profile.bundles;for(const n of add){if(!b.includes(n))b.push(n)};fs.writeFileSync(f,JSON.stringify(p,null,2)+'\n');console.log(b.join('\n'))" -- @nanmicoder/dsh-agent-teams @linxin666/dsh-client-ui-task-board dsh-synapse dsh-our-free-model dsh-plugin-control-your-development dsh-codearts-auth
```

若在**新机器**上（包还没装），则用 `pnpm add` + 上面的命令一起做。

---

## 4. 完整安装命令（复制即用）

```powershell
# 进入 profile 目录
cd $env:USERPROFILE\.dsh\profiles\desktop

# 4.1 本机已启用的 7 个第三方插件
pnpm add `
  "@eddyskywalker/dsh-chatgpt-subscription@^0.17.0" `
  "@linxin666/dsh-client-ui-web-ui-settings@^0.4.5" `
  "@linxin666/dsh-remote-web-ui@^0.4.5" `
  "@linxin666/dsh-usage@^0.4.5" `
  "dsh-ops@github:T-Auto/dsh-ops" `
  "dshmarket@^1.66.8" `
  "dsh-voice-alert@github:BUGLAN/dsh-voice-alert"

# 4.2 本机已装未启用的 6 个（按需）
pnpm add `
  "@nanmicoder/dsh-agent-teams@0.1.22" `
  "@linxin666/dsh-client-ui-task-board@^0.4.5" `
  "dsh-synapse@^0.4.2" `
  "dsh-our-free-model@github:zouyuxuan122/dsh-our-free-model" `
  "dsh-plugin-control-your-development@github:HaoyanZhang123/dsh-plugin-control-your-development" `
  "dsh-codearts-auth@0.3.1004"   # 原 GitHub 来源已 404，改用 npm
```

> `dsh-codearts-auth` 请**不要**写 `github:zhengwuji/Jet-Hub`，仓库已不存在；见 2.2 节说明。

一行版（bash / Git Bash 也能跑）：

```bash
cd "$USERPROFILE/.dsh/profiles/desktop"
pnpm add "@eddyskywalker/dsh-chatgpt-subscription@^0.17.0" "@linxin666/dsh-client-ui-web-ui-settings@^0.4.5" "@linxin666/dsh-remote-web-ui@^0.4.5" "@linxin666/dsh-usage@^0.4.5" "dsh-ops@github:T-Auto/dsh-ops" "dshmarket@^1.66.8" "dsh-voice-alert@github:BUGLAN/dsh-voice-alert"
```

> `pnpm add` 只写 `dependencies`，**不会**写 `dsh.profile.bundles`。装完必须执行第 3.3 节第 3 步。

---

## 5. profile 配置模板

### 5.1 `package.json`（本机现状，仅供对照）

```json
{
  "name": "dsh-profile-desktop",
  "private": true,
  "dependencies": {
    "@eddyskywalker/dsh-chatgpt-subscription": "^0.17.0",
    "@linxin666/dsh-client-ui-task-board": "^0.4.5",
    "@linxin666/dsh-client-ui-web-ui-settings": "^0.4.5",
    "@linxin666/dsh-remote-web-ui": "^0.4.5",
    "@linxin666/dsh-usage": "^0.4.5",
    "@nanmicoder/dsh-agent-teams": "0.1.22",
    "dsh-codearts-auth": "github:zhengwuji/Jet-Hub",
    "dsh-ops": "github:T-Auto/dsh-ops",
    "dsh-our-free-model": "github:zouyuxuan122/dsh-our-free-model",
    "dsh-plugin-control-your-development": "github:HaoyanZhang123/dsh-plugin-control-your-development",
    "dsh-synapse": "^0.4.2",
    "dsh-voice-alert": "github:BUGLAN/dsh-voice-alert",
    "dshmarket": "^1.66.8"
  },
  "dsh": {
    "profile": {
      "bundles": [
        "@deepseek-ai/dsh-base",
        "@deepseek-ai/dsh-web-app",
        "dsh-voice-alert",
        "dshmarket",
        "@linxin666/dsh-usage",
        "@linxin666/dsh-remote-web-ui",
        "@linxin666/dsh-client-ui-web-ui-settings",
        "dsh-ops",
        "@eddyskywalker/dsh-chatgpt-subscription"
      ]
    }
  }
}
```

⚠️ **不要整份覆盖新机器的 `package.json`**：`@deepseek-ai/dsh-base` / `dsh-web-app` 的具体版本随 DSH 版本变化，新机器上可能不同。请只合并 `dependencies` 条目和 `bundles` 条目。

> 本机原始值是 `"dsh-voice-alert": "link:E:/repo/deepseek-harness/plugins/dsh-voice-alert"`（本地软链开发态）。搬到别的机器请用 `github:BUGLAN/dsh-voice-alert`。
>
> `dsh-codearts-auth` 那一行是**本机历史值**，仓库已 404；新机器请改成 `"dsh-codearts-auth": "^0.3.1004"`（见 2.2 节）。

### 5.2 `pnpm-workspace.yaml`

见第 3.3 节第 1 步。要点：

- `nodeLinker: hoisted`：DSH 插件生态普遍按 hoisted 布局解析依赖，别改成默认的 isolated。
- `autoInstallPeers: false`：插件 peer 依赖靠 DSH 宿主提供，自动装会引入重复的 `@deepseek-ai/*`。
- `allowBuilds`：git 来源的包若带构建脚本，必须在这里显式放行（`cloudflared` 也是必需的）。
- `minimumReleaseAgeExclude`：pnpm 11 的供应链最小发布年龄策略会挡掉刚发布的版本，需要时加白名单。

---

## 6. 需要手工重建的本机配置（`cordis.patch.yml`）

`cordis.patch.yml` 是**本机配置**，不是插件本体，无法照抄。以下条目在新机器上要按自己的情况重填。文件位置：`%USERPROFILE%\.dsh\profiles\desktop\cordis.patch.yml`。

| 配置项 | 本机情况 | 迁移时怎么做 |
| --- | --- | --- |
| `llm-pi-ai` 的 providers | 配了 7 个自建/中转 provider（`commandcode` / `opencode-go` / `ark` / `zai-coding-cn` / `togenashitogeari` / `newapi` / `z1rry`），各自用 `apiKeyEnv` 读环境变量 | **只搬结构，Key 自己填**。环境变量名：`COMMANDCODE_API_KEY`、`OPENCODE_GO_API_KEY`、`ARK_API_KEY`、`ZAI_CODING_CN_API_KEY`、`TOGENASHITOGEARI_API_KEY`、`NEWAPI_API_KEY`、`Z1RRY_API_KEY` |
| `remote-web-ui` | `publicBaseUrl: https://dsh.buglan.com` + 一段 Cloudflare `tunnelToken` | **Token 是本机专属凭证，本文件不包含**。新机器必须在设置页重新生成/绑定自己的隧道 |
| `webserver` | `127.0.0.1:19387` | 端口按需改；本机 GUI 地址由它决定 |
| `permission` | `defaultPreset: danger-full-access` | 按自己的安全偏好设 |
| `ui-theme` / `ui-chat` / `ui-settings-*` | 主题、字号、转录视图等个人偏好 | 可照抄，纯偏好 |
| `preset-pj-mode` | 本机自定义的 agent preset（`@deepseek-ai/dsh-agent-preset`），一段很长的 persona 正文 | **不是插件**，属于个人 prompt 定制。需要就自行搬 `cordis.patch.yml` 里对应整段 |
| `voice-alert` | `disabled: false` | 装了 `dsh-voice-alert` 后保持启用 |

凭证相关：

- `%USERPROFILE%\.dsh\.credentials.yaml` 存登录态/密钥。**不要**把它当插件清单一起外发；确实要迁移登录态再单独处理。
- 本文件（以及第 2、4 节的命令）**不含任何密钥**，可以安全分享。

---

## 7. 验证

```powershell
# 1) 包是否装上
cd $env:USERPROFILE\.dsh\profiles\desktop
pnpm list --depth 0

# 2) 插件行是否进了合并后的加载清单（cordis.yml 末尾就是插件层）
Select-String -Path cordis.yml -Pattern "voice-alert|dshmarket|dsh-usage|remote-web-ui|dsh-ops|chatgpt-subscription|ui-web-ui-settings"
```

期望：`cordis.yml` 尾部能看到对应的 `- id:` / `name:` 行（该文件由 DSH 在启动时按 `bundles` 顺序重新生成）。

运行期检查：

- 侧边栏出现 **插件市场**、**用量统计** 等入口；
- 设置页出现 **dsh-web** 相关分区；
- 任务结束时 `dsh-voice-alert` 会响铃 / 发系统通知。

改完配置后：开着 HMR 时配置变更即时生效；否则**重启 DSH**。

---

## 8. 排障

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `ERR_PNPM_GIT_DEP_PREPARE_NOT_ALLOWED`：`needs to execute build scripts but is not in the "allowBuilds" allowlist` | git 来源的包带构建脚本，pnpm 默认拒绝执行 | 按报错提示把该包加进 `pnpm-workspace.yaml` 的 `allowBuilds`。本机踩过：`dsh-synapse`、`dsh-codearts-auth`、`cloudflared` |
| 装完插件但侧边栏/设置页没变化 | 只进了 `dependencies`，没进 `dsh.profile.bundles` | 执行第 3.3 节第 3 步，然后重启 |
| `listBundles` 里显示某 bundle `error` | 包在磁盘上但加载失败（版本不兼容、依赖缺失） | 看报错；`engines.dsh` 不满足时降级/升级 DSH 或换插件版本 |
| GitHub 来源安装卡住 / 失败 | 插件管理器先做 `git ls-remote` 连通性检查（默认 5s） | 检查代理与 Git 配置；只影响来源可达性检查，不影响后续 pnpm 下载 |
| `remote: Repository not found` / 404 | 上游仓库被删除或转私有 | 换 npm 上的同名包，或从别处拿 tarball/本地路径。本机已踩：`dsh-codearts-auth` 的 `zhengwuji/Jet-Hub`（见 2.2 节） |
| 提示最小发布年龄策略拦下新版本 | pnpm 11 供应链策略 | 把该版本加进 `minimumReleaseAgeExclude` |
| `dsh-ops` 在非 Windows 上不可用 | 它面向 Windows 提供 bash / PowerShell 7 与 Rust 工具链 | Linux/macOS 不要装 |
| 装了两个提供同名能力的插件 | bundles 后者覆盖前者，顺序即优先级 | 调整 `dsh.profile.bundles` 顺序 |

---

## 9. 附录

### 9.1 次要 profile：`web`（开发用，可不搬）

`%USERPROFILE%\.dsh\profiles\web\package.json`：

```json
{
  "name": "dsh-profile-web",
  "private": true,
  "dependencies": {
    "@deepseek-ai/dsh-panel": "link:E:/repo/deepseek-harness/packages/panel/panel",
    "@deepseek-ai/dsh-tool-panel": "link:E:/repo/deepseek-harness/packages/panel/tool-panel",
    "@linxin666/dsh-client-ui-task-board": "^0.4.5",
    "@linxin666/dsh-remote-web-ui": "^0.4.5"
  },
  "dsh": {
    "profile": {
      "bundles": [
        "@deepseek-ai/dsh-base",
        "@deepseek-ai/dsh-web-app",
        "@linxin666/dsh-client-ui-task-board",
        "@linxin666/dsh-remote-web-ui"
      ],
      "patchReload": "live"
    }
  }
}
```

其中两个 `link:` 指向本机 DSH 源码检出 `E:/repo/deepseek-harness/packages/panel/`，属于开发态挂载，**不要搬到别的机器**。

### 9.2 来源速查

| 插件 | 仓库 / 主页 |
| --- | --- |
| `dshmarket` | https://github.com/dsh-market/dsh-market ｜ https://dshmarket.com |
| `dsh-voice-alert` | https://github.com/BUGLAN/dsh-voice-alert |
| `dsh-ops` | https://github.com/T-Auto/dsh-ops |
| `@linxin666/*`（usage / remote-web-ui / web-ui-settings / task-board） | https://github.com/zhu1090093659/dsh-web |
| `@eddyskywalker/dsh-chatgpt-subscription` | https://github.com/Aa728848/dsh-chatgpt-subscription |
| `@nanmicoder/dsh-agent-teams` | https://github.com/NanmiCoder/dsh-agent-teams |
| `dsh-plugin-control-your-development` | https://github.com/HaoyanZhang123/dsh-plugin-control-your-development |
| `dsh-our-free-model` | https://github.com/zouyuxuan122/dsh-our-free-model |
| `dsh-codearts-auth` | ⚠️ https://github.com/zhengwuji/Jet-Hub —— **已 404，不可用**；改用 npm `dsh-codearts-auth` |
| `dsh-synapse` | https://github.com/liangmianya/dsh-synapse |

> 上表 GitHub 地址已于 2026-10-13 用 `git ls-remote` 逐个验证：除 `zhengwuji/Jet-Hub` 外全部可达。

### 9.3 版本速查（本机锁定值）

```
@eddyskywalker/dsh-chatgpt-subscription  0.17.0
@linxin666/dsh-client-ui-task-board      0.4.5
@linxin666/dsh-client-ui-web-ui-settings 0.4.5
@linxin666/dsh-remote-web-ui             0.4.5
@linxin666/dsh-usage                     0.4.5
@nanmicoder/dsh-agent-teams              0.1.22
dsh-codearts-auth                        0.4.1   (github zhengwuji/Jet-Hub @17f41dc ← 该仓库已 404)
                                         0.3.1004  ← npm 上最接近的替代（描述与本机 0.4.1 一致）
                                         1.0.261007 ← npm latest，功能已扩展为多服务商账号池
dsh-ops                                  0.2.6   (github T-Auto/dsh-ops @5338d51)
dsh-our-free-model                       1.3.1   (github zouyuxuan122/dsh-our-free-model @98842df)
dsh-plugin-control-your-development      0.4.2   (github HaoyanZhang123/... @309b2ec)
dsh-synapse                              0.4.2
dsh-voice-alert                          1.0.0
dshmarket                                1.66.8
```
