# SSTV Decoder · 跨平台通用慢扫描电视解码插件

[English](README.md) | [简体中文](README.zh-CN.md) | [在线展示页（`sstv-decoder.netlify.app`）](https://sstv-decoder.netlify.app)（源码见 [`docs/`](docs/index.html)）

面向国际空间站（ISS / ARISS）过境监听与业余无线电爱好者的**通用开源 Robot 36 SSTV 音频解码插件**。

基于 **MCP（Model Context Protocol）** 与 **Agent Skills（`SKILL.md`）** 双开放标准构建，一次开源即可直接运行在 **Cursor、Claude Desktop、Claude Code、OpenAI Codex、Antigravity、Windsurf、ChatGPT** 以及纯命令行环境中，无需绑定信用卡上架封闭商店。

> **项目展示网页**：仓库 [`docs/`](docs/index.html) 目录内置中英双语航天风格宣传页与作者介绍页，可在 GitHub 仓库开启 GitHub Pages（选择分支 `/docs` 目录）或直接托管到 Vercel 免费上线。

---

## 核心特性

- **全自动寻帧**：自动扫描整段过境录音中的 Robot 36 VIS 识别头（`VIS 8`），无需人工估算或填写时间戳。
- **行同步校准与双声道择优**：逐帧拟合 150 ms 扫描时钟以抵抗采样率漂移和多普勒频移；双声道录音自动为每一帧选择信噪比更优的声道。
- **弱信号频谱恢复**：当行同步较弱或信号中断时，自动切换至噪声协方差频谱参考估计，并将结果清晰标记为 `partial`（部分恢复）。
- **多音频格式支持**：通过 FFmpeg 支持 **WAV、M4A/MP4、MP3、FLAC、OGG/Opus、AAC、AIFF、WebM、WMA** 等常见格式（单次上限 15 分钟 / 128 MiB）。
- **三种通用接入方式**：
  - **本地 `stdio` MCP（主力推荐）**：零服务器部署、零费用、本地隐私保护，直接读取本机录音保存 PNG 并向多模态 Agent 返回图片预览。
  - **远程 Streamable HTTP MCP**：兼容公网 HTTPS 音频链接与 ChatGPT 附件上传（`openai/fileParams`），内置 MCP App 结果卡片。
  - **通用 Agent Skill（`skills/sstv-decoder/SKILL.md`）**：不配 MCP 也能让支持 `agentskills.io` 规范的 AI 自动学会检查与解码录音。

---

## 环境要求

1. **Python 3.11+**（推荐安装 [`uv`](https://docs.astral.sh/uv/)，支持 `uvx` 零配置即开即用）
2. 系统 `PATH` 中已安装 **FFmpeg 与 ffprobe**：
   - macOS：`brew install ffmpeg`
   - Ubuntu / Debian：`sudo apt update && sudo apt install -y ffmpeg`
   - Windows：`winget install Gyan.FFmpeg`

---

## 介入边界与一句话通用安装

> **边界说明**：本插件从你**已经录得无线电音频文件之后**才开始介入。国际空间站过境时刻预报、轨道追踪与手台/八木天线收音由爱好者自行完成；把录好的音频交给 AI 后，识别头定位、行同步校准与图像解码全部由本插件自动完成。

遵循开放 Agent Skills 规范，**一条指令**即可安装到本机支持的多个主流 AI Agent（覆盖 **Claude Code、Cursor、OpenAI Codex、Antigravity、Windsurf、GitHub Copilot、Gemini CLI** 等 75+ 工具）：

```sh
npx skills add BruceStyle/sstv-decoder
```

---

## 进阶接入：本地 / 远程 MCP 服务

如果需要在仅支持 MCP 的客户端（如 Claude Desktop）中使用本插件，可使用下方的标准 MCP 配置（在正式发布至 PyPI 前，请将 `"uvx", "sstv-decoder-mcp"` 替换为 `"uvx", "--from", "git+https://github.com/BruceStyle/sstv-decoder", "sstv-decoder-mcp"`）：

### 1. Cursor
在项目 `.cursor/mcp.json` 或全局 `~/.cursor/mcp.json` 中添加：
```json
{
  "mcpServers": {
    "sstv-decoder": {
      "command": "uvx",
      "args": ["sstv-decoder-mcp"]
    }
  }
}
```

### 2. Claude Desktop
添加到 `claude_desktop_config.json`（macOS 位于 `~/Library/Application Support/Claude/claude_desktop_config.json`）：
```json
{
  "mcpServers": {
    "sstv-decoder": {
      "command": "uvx",
      "args": ["sstv-decoder-mcp"]
    }
  }
}
```

### 3. Claude Code
```sh
claude mcp add sstv-decoder -- uvx sstv-decoder-mcp
```

### 4. OpenAI Codex
添加到 `~/.codex/config.toml`：
```toml
[mcp_servers.sstv-decoder]
command = "uvx"
args = ["sstv-decoder-mcp"]
```

### 5. Antigravity / Windsurf / VS Code
在 MCP 配置 JSON 中加入：
```json
{
  "mcpServers": {
    "sstv-decoder": {
      "command": "uvx",
      "args": ["sstv-decoder-mcp"]
    }
  }
}
```

### 6. ChatGPT 与网页端远程 Agent（Streamable HTTP MCP）
通过 Docker 或命令启动 HTTP 服务并暴露 HTTPS 域名，在客户端添加自定义远程 MCP 地址 `https://<your-domain>/mcp`：
```sh
uvx sstv-decoder mcp --transport http --host 0.0.0.0 --port 8000
```

---

## 命令行（CLI）用法

```sh
# 仅预检音频参数与 VIS 识别头（不进行整帧解调）
uvx sstv-decoder inspect /path/to/iss_pass.m4a

# 解码 Robot 36 图像到指定目录（省略 -o 时默认输出到 <文件名>_sstv/）
uvx sstv-decoder decode /path/to/iss_pass.m4a -o ./output_frames

# 启动标准本地 stdio MCP 服务
uvx sstv-decoder mcp

# 启动远程 Streamable HTTP MCP 服务
uvx sstv-decoder mcp --transport http --host 127.0.0.1 --port 8000
```

---

## MCP 工具一览

### 本地 `stdio` 服务（`sstv-decoder-mcp`）
- `decode_sstv_audio(audio_path, output_dir?, include_images?, overwrite?)`：解码本地音频中的 Robot 36 帧，保存 `frame-01.png` 等图片及 `report.json`，并返回内联 PNG 图片预览与结构化报告。
- `inspect_sstv_audio(audio_path)`：读取音频流信息并扫描所有 SSTV VIS 识别头（可识别 Robot 36、PD120、Martin、Scottie 等常见模式的 VIS 码）。
- `list_supported_modes()`：返回支持解码的模式、音频格式、文件限制与 VIS 码表。

### 远程 HTTP 服务（`/mcp`）
- `decode_robot36_audio(audio?, audio_url?)`：同时兼容 ChatGPT 附件参数（`openai/fileParams`）和标准 HTTPS 音频链接 `audio_url`，配合 MCP App 结果卡片预览并下载 PNG。

---

## Docker 自托管与环境变量

```sh
docker build -t sstv-decoder .
docker run -p 8000:8000 \
  -e SSTV_PUBLIC_ORIGIN=https://sstv.example.org \
  -e SSTV_ALLOW_PUBLIC_URLS=1 \
  sstv-decoder
```

| 环境变量 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `SSTV_PUBLIC_ORIGIN` | 对外可访问的 HTTPS Origin，用于生成图片链接与 CSP | `http://127.0.0.1:8000` |
| `SSTV_AUDIO_HOSTS` | 允许下载远程音频的主机白名单（逗号分隔） | 附件模式默认 `*.oaiusercontent.com` |
| `SSTV_ALLOW_PUBLIC_URLS` | 设为 `1` 时允许下载任意公网 HTTPS `audio_url`（内置私网/回环 IP SSRF 防护） | `0` |
| `SSTV_ALLOWED_ORIGINS` | 额外允许的 Origin 列表（逗号分隔） | `origin, chatgpt.com, claude.ai` |
| `SSTV_RESULT_CACHE` | 部署在 Vercel 时设为 `vercel` 以启用 `AsyncRuntimeCache` | 单进程内存缓存（30 分钟过期） |
| `SSTV_DOMAIN_CHALLENGE_TOKEN` | 可选，用于 `/.well-known/openai-apps-challenge` 域名验证 | 未设置 |

---

## 本地开发与发布到 PyPI

PyPI 账号注册与开源发布**完全免费且不需要绑定信用卡**。

```sh
# 同步本地开发环境
uv sync

# 运行全部单元测试
uv run python -m unittest discover -s tests -v

# 构建发布包（wheel 与 sdist）
uv build

# 发布到 PyPI（使用 PyPI API Token）
uv publish
```

## 开源协议

[MIT](LICENSE)
