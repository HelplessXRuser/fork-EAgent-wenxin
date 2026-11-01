# EAgent-文心

> 0 tokens、0 门槛、轻量级 —— 基于**百度文心网页版**的 Agent，让文心“操控”你的电脑。

![license](https://img.shields.io/badge/license-GPL--3.0-blue)

本仓库是 [EAgent](https://github.com/YaoGaoChaoLe/EAgent) 的衍生版本（fork），把默认后端从 DeepSeek 换成了**百度文心（wenxin.baidu.com）**，其余保留上游的 CDP 自动化思路。

- 上游仓库：<https://github.com/YaoGaoChaoLe/EAgent>
- 上游许可证：GPL-3.0（版权归原作者）
- 本 fork 同样以 **GPL-3.0** 发布

---

## 和上游有什么不同

| 项目 | 上游（DeepSeek 版） | 本 fork（文心版） |
|------|--------------------|------------------|
| 默认网页 | `chat.deepseek.com` | `wenxin.baidu.com` |
| 界面文字 | DeepSeek | 百度文心 |
| 浏览器存档 | `deepseek_debug_profile` | `wenxin___debug_profile`（独立，不与 DeepSeek 版互串） |
| 页面选择器 | DeepSeek DOM | 文心 DOM：`#chat-textarea` / `#ci-submit-button-ai` / `.answer-box` |
| 回答读取 | 原逻辑 | 过滤「正在思考 / 正在搜索」占位文字，避免永远停在“思考中” |
| 图标 | 上游图标 | 文心娘图标（可替换） |

逐项说明见 [docs/MODIFICATIONS.md](docs/MODIFICATIONS.md)。

## 环境要求

- **必须**：Edge 浏览器（Windows 自带）
- **系统**：Windows 10 / 11
- **权限**：必须以**管理员身份**运行（需要启动浏览器调试端口并执行 PowerShell）

## 快速使用

1. 下载 [dist/EAgent-文心.exe](dist/EAgent-文心.exe)
2. 右键 → **以管理员身份运行**（不要直接双击）
3. 点击 `选择工作目录`，选择一个目录
4. 程序会自动打开 Edge 并进入文心页面；**免登录即可基础对话**，需要完整功能时再登录百度账号
5. 点击 `开始新对话`，等待 AI 分析提示词
6. 用 EAgent 发消息，**不要在网页里发** —— 网页只负责展示

## 实现原理

- **不是反代**、没有第三方中转、不逆向文心接口。
- 核心：通过 CDP 自动化模拟真实用户操作。这类操作**可能违反 [《文心用户协议》](https://yiyanapp.baidu.com/app/userprivacy)**，请自行评估风险。

```text
用 PowerShell 连接 Chrome/Edge 调试端口，
通过 CDP WebSocket 在文心页面里执行 JavaScript，
模拟输入、上传文件、点击发送，并轮询判断助手回复是否完成、返回助手回复信息。
```

## 目录结构

```text
├── dist/EAgent-文心.exe      ← 本 fork 产物（下载这个）
├── upstream/EAgent-DS.exe    ← 上游原版 EXE（未修改，GPL 复现基线）
├── tools/
│   ├── patch_eagent.py       ← 从原版 EXE 复现本 fork 的补丁脚本
│   ├── set_icon.js           ← 可选：替换图标（需 npm i resedit）
│   └── icon/wenxin_girl.ico
├── docs/MODIFICATIONS.md     ← 逐项改动说明
├── BUILD.md                  ← 构建 / 复现步骤
├── FORK.md                   ← fork 说明与目录
├── NOTICE.md                 ← 版权与 GPL 合规声明
├── index.html                ← 项目介绍页
└── （上游易语言工程源码，未修改）
    _EAgent.e  class/  config/  form/  resource/  Works/
    const.e.txt  struct.e.txt  global.e.txt  dll.e.txt
    project.etprj  icon.ico  auto_update.txt  *.ec
```

## 构建 / 复现

```bash
python tools/patch_eagent.py upstream/EAgent-DS.exe dist/EAgent-文心.exe
```

详见 [BUILD.md](BUILD.md)。

> 注意：本 fork 通过**等长字节修改**原版 EXE 实现，未改动易语言源码。GPL 合规方式见 [NOTICE.md](NOTICE.md)。

## 声明

- 仅单个 .exe，**仅供学习交流**，不适用于生产环境。
- **无安全沙箱**：文心可能生成恶意代码并经 EAgent 在你的电脑执行，请审查 AI 要执行的命令。
- 有基础防风控措施，但**极端高频**使用仍可能被文心限制；作者不承担责任。
- 上游由**易语言**编写，编译器缺陷常导致杀毒软件误报；本 fork 由原版等长修改而来。
- 本项目与百度、DeepSeek 均无关联，请遵守目标网站服务条款。

## 致谢

- 上游作者：[YaoGaoChaoLe/EAgent](https://github.com/YaoGaoChaoLe/EAgent)（GPL-3.0）
- 本 fork 仅更换后端页面与适配，核心思路与绝大部分代码归上游所有。
