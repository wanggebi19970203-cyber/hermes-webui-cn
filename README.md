# Hermes Web UI（中文版）

> **Hermes Web UI 的中文化 fork。** 界面默认中文，保留英文切换。
> 
> - 默认语言：中文（zh）
> - 切换英文：设置 → 语言 → English
> - 覆盖范围：登录页、所有面板、会话操作、错误提示、设置界面
> - 基于上游 [nesquena/hermes-webui](https://github.com/nesquena/hermes-webui) v0.42.2

<img alt="Hermes Web UI 三栏布局" width="1417" height="867" src="https://github.com/user-attachments/assets/51adff98-53ee-4800-8508-78b6c34dd3dc" />

<table>
  <tr>
    <td width="50%" align="center">
      <img alt="浅色模式 + 多 Profile 支持" src="https://github.com/user-attachments/assets/9b68142f-d974-4493-a8d1-fd73e622c7fd" />
      <br /><sub>浅色模式 + 多 Profile 支持</sub>
    </td>
    <td width="50%" align="center">
      <img alt="设置面板 + 密码配置" src="https://github.com/user-attachments/assets/941f3156-21e3-41fd-bcc8-f975d5000cb8" />
      <br /><sub>设置面板 + 密码配置</sub>
    </td>
  </tr>
</table>

---

## 什么是 Hermes

[Hermes Agent](https://hermes-agent.nousresearch.com/) 是一个驻留在服务器上的自主 Agent，可通过终端或消息应用访问。

大多数 AI 工具每次会话都从零开始——不认识你、不知道你在做什么、不了解你的项目。Hermes 不一样：它有持久记忆，运行越久越懂你。

核心特性：
- **持久记忆** — 跨会话记忆，自动学习你的环境和偏好
- **定时任务** — 离线时自动执行 cron 任务，结果推送到 Telegram、Discord、Slack 等
- **多平台访问** — 同一个 Agent 在终端可用，在手机上也能聊
- **自进化 Skills** — Hermes 自动从经验中保存可复用技能，不需要安装插件
- **多模型支持** — OpenAI、Anthropic、Google、DeepSeek 等任意切换
- **编排子 Agent** — 可以调用 Claude Code 或 Codex 处理复杂编码任务
- **完全自托管** — 你的对话、你的记忆、你的服务器

---

## 快速开始

### 前置条件

需要先安装 [Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)：

* [ ] 运行 `curl` 命令安装 Hermes
* [ ] 用 `hermes model` 配置 [LLM 提供商](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart#2-set-up-a-provider)
* [ ] 用 `hermes gateway setup` 配置 [消息网关](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/)
* [ ] 确保 `hermes` 命令行可以正常对话
* [ ] 可选：[配置扩展记忆](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers)
* [ ] 可选：[配置工具](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools)

### 安装 Web UI

```bash
git clone git@github.com:wanggebi19970203-cyber/hermes-webui-cn.git hermes-webui
cd hermes-webui
./start.sh
```

脚本会自动完成：
1. 定位你的 Hermes agent 目录
2. 找到（或创建）Python 环境
3. 启动 Web 服务
4. 打印访问地址（远程机器会同时打印 SSH 隧道命令）

---

## Docker 部署

```bash
docker compose up -d
```

或手动运行：

```bash
docker build -t hermes-webui .
docker run -d -p 8787:8787 -v ~/.hermes:/root/.hermes hermes-webui
```

开启密码认证：

```bash
docker run -d -p 8787:8787 -e HERMES_WEBUI_PASSWORD=*** -v ~/.hermes:/root/.hermes hermes-webui
```

> **注意：** Docker Compose 默认绑定 `127.0.0.1`（仅本地访问）。
> 如需网络访问，修改 `docker-compose.yml` 端口为 `"8787:8787"` 并设置 `HERMES_WEBUI_PASSWORD`。

---

## 远程访问

服务器默认绑定 `127.0.0.1`（仅本地），远程服务器需要 SSH 隧道：

```bash
# 在本地机器执行
ssh -N -L 8787:127.0.0.1:8787 user@你的服务器地址
```

然后浏览器打开 http://localhost:8787

---

## 手机访问（Tailscale）

[Tailscale](https://tailscale.com) 是基于 WireGuard 的零配置 VPN。手机和服务器加入同一网络即可直接访问。

1. 在服务器和手机安装 [Tailscale](https://tailscale.com/download)
2. 启动 WebUI 并开启密码：

```bash
HERMES_WEBUI_HOST=0.0.0.0 HERMES_WEBUI_PASSWORD=*** ./start.sh
```

3. 手机浏览器打开 `http://<服务器Tailscale IP>:8787`

---

## 手动启动

```bash
cd /path/to/hermes-agent
HERMES_WEBUI_PORT=8787 venv/bin/python /path/to/hermes-webui/server.py
```

> 需要使用 agent venv 中的 Python，系统 Python 会缺少 `openai`、`httpx` 等依赖。

---

## 功能一览

### 对话和 Agent
- SSE 流式响应（逐 token 实时显示）
- 多模型动态切换（配置了哪个 provider 就能用哪个）
- 消息队列：忙碌时自动排队
- 编辑历史消息、重新生成回复
- 工具调用卡片（参数、结果一目了然）
- Mermaid 图表渲染（流程图、时序图、甘特图）
- 思考过程展示（Claude extended thinking / o3 reasoning）
- 危险命令审批（允许一次/本次/始终/拒绝）
- SSE 自动重连（SSH 隧道断开恢复）
- 文件附件、消息时间戳、代码块复制
- 上下文窗口用量指示器（token 数、费用、填充进度条）

### 会话管理
- 创建、重命名、复制、删除、按标题和内容搜索
- 置顶、归档、项目分组、标签筛选
- 今天/昨天/更早 分组（可折叠）
- 导出 Markdown / JSON，从 JSON 导入
- CLI 会话桥接（hermes-agent 的会话自动出现在列表中）

### 文件浏览器
- 目录树（展开/折叠）、面包屑导航
- 预览：文本、代码、Markdown（渲染后）、图片
- 在线编辑、创建、删除、重命名
- Git 检测（分支名、未提交文件数）
- 右侧面板可拖拽调整宽度

### 语音输入
- 麦克风按钮（Web Speech API）
- 点击录音，再点或发送停止
- 实时显示识别结果

### 多 Profile
- 顶栏切换器、侧边栏管理面板
- 创建、切换、删除 Profile
- 切换时自动重新加载配置、Skills、Memory、Cron

### 认证与安全
- 可选密码认证（默认关闭，本地零摩擦）
- HMAC 签名 Cookie（24h 有效期）
- 安全头（X-Content-Type-Options、X-Frame-Options）
- 20MB 请求体限制

### 主题
- 7 个内置主题：深色（默认）、浅色、岩板、Solarized 暗色、Monokai、Nord、OLED
- 设置面板实时预览，或 `/theme` 命令切换

### 斜杠命令
- `/help` `/clear` `/model` `/workspace` `/new` `/usage` `/theme` `/compact`

### 面板
- **对话** — 会话列表、搜索、置顶、归档、项目
- **任务** — 创建/编辑/运行/暂停/删除 cron 任务
- **Skills** — 按分类浏览、搜索、创建/编辑/删除
- **记忆** — 编辑 MEMORY.md 和 USER.md
- **Profiles** — 管理 Agent Profile
- **待办** — 当前会话任务列表
- **工作区** — 添加/删除/切换工作区

### 移动端适配
- 汉堡菜单侧栏、底部 5 标签导航栏
- 文件从右侧滑入
- 触控目标最小 44px

---

## 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `HERMES_WEBUI_AGENT_DIR` | 自动发现 | hermes-agent 路径 |
| `HERMES_WEBUI_PYTHON` | 自动发现 | Python 可执行文件 |
| `HERMES_WEBUI_HOST` | `127.0.0.1` | 绑定地址 |
| `HERMES_WEBUI_PORT` | `8787` | 端口 |
| `HERMES_WEBUI_STATE_DIR` | `~/.hermes/webui-mvp` | 会话和状态存储目录 |
| `HERMES_WEBUI_DEFAULT_WORKSPACE` | `~/workspace` | 默认工作区 |
| `HERMES_WEBUI_DEFAULT_MODEL` | `openai/gpt-5.4-mini` | 默认模型 |
| `HERMES_WEBUI_PASSWORD` | *(未设置)* | 设置密码以启用认证 |
| `HERMES_HOME` | `~/.hermes` | Hermes 状态目录 |
| `HERMES_CONFIG_PATH` | `~/.hermes/config.yaml` | Hermes 配置文件路径 |

---

## 中文本地化说明

本 fork 基于原版 [nesquena/hermes-webui](https://github.com/nesquena/hermes-webui) 开发，目标是让中文用户开箱即用。

### 做了什么
- 所有用户可见文案走 `static/i18n.js` 中的 `t(key)` 函数
- `zh` locale 与 `en` 完全对齐（各 389 个 key，零缺口）
- 登录页根据 `settings.language` 自动渲染对应语言
- `settings.language` 默认值为 `zh`
- 保留完整的英文切换能力，切换后无中英残留

### 如何添加新文案
1. 在 `static/i18n.js` 的 `en` 和 `zh` 两个 locale 中同时添加 key
2. HTML 中使用 `data-i18n`（文本）、`data-i18n-title`（title）、`data-i18n-placeholder`（placeholder）
3. JS 中使用 `t('key')` — 包括 `showToast()`、`setStatus()`、`confirm()`、`prompt()`
4. `option` 元素由 JS 在运行时填充（`applyLocaleToDOM()` 不处理 option）

详细约束见 [ARCHITECTURE.md](ARCHITECTURE.md#i18n-约束)。

---

## 项目结构

```
hermes-webui-cn/
├── server.py              HTTP 路由入口 + 认证中间件
├── api/
│   ├── auth.py            密码认证、签名 Cookie
│   ├── config.py          发现、全局状态、配置管理
│   ├── routes.py          所有 GET/POST 路由处理
│   ├── streaming.py       SSE 引擎、Agent 执行
│   ├── models.py          会话模型 CRUD
│   ├── profiles.py        Profile 状态管理
│   ├── workspace.py       文件操作、Git 检测
│   └── upload.py          文件上传处理
├── static/
│   ├── index.html         HTML 模板（126 个 i18n 属性）
│   ├── style.css          全部 CSS（含移动端响应式）
│   ├── i18n.js            中英文语言包（389 key × 2 locale）
│   ├── ui.js              DOM 渲染、Markdown、工具卡片
│   ├── messages.js        消息发送、SSE 处理
│   ├── sessions.js        会话 CRUD、列表渲染
│   ├── panels.js          任务/Skills/Memory/Profile/设置面板
│   ├── workspace.js       文件预览、文件操作
│   ├── commands.js        斜杠命令
│   └── boot.js            启动初始化、移动端导航
├── tests/                 pytest 测试（独立端口 8788）
├── Dockerfile
├── docker-compose.yml
└── 文档：HERMES.md / ROADMAP.md / ARCHITECTURE.md / TESTING.md / CHANGELOG.md
```

---

## 相关文档

- `HERMES.md` — Hermes 的设计理念、与其他工具的详细对比
- `ROADMAP.md` — 功能路线图和 Sprint 历史
- `ARCHITECTURE.md` — 系统设计、所有 API 端点、i18n 约束
- `TESTING.md` — 手动浏览器测试计划（含中文本地化回归检查）
- `CHANGELOG.md` — 每个版本的发布说明
- `THEMES.md` — 主题系统文档

---

## 仓库

```
上游仓库：https://github.com/nesquena/hermes-webui
中文 Fork：git@github.com:wanggebi19970203-cyber/hermes-webui-cn.git
```
