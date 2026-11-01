# EAgent-文心 Fork 说明

本仓库是 [EAgent](https://github.com/YaoGaoChaoLe/EAgent) 的衍生版本（fork），把原本面向 DeepSeek 网页的默认后端改为**百度文心（wenxin.baidu.com）**，并做了一些体验修正。

- 上游仓库：https://github.com/YaoGaoChaoLe/EAgent
- 上游提交（本次基于）：`1b44514`
- 上游许可证：**GNU GPL v3.0**（见根目录 `LICENSE`，版权归原作者所有）
- 本 fork 同样以 **GPL-3.0** 发布

## 目录结构

```
.
├── LICENSE                 上游 GPL-3.0 全文（未修改）
├── README.md               上游 README（未修改）
├── NOTICE.md               本 fork 的版权/合规声明
├── BUILD.md                如何从原版 EXE 复现本 fork
├── docs/MODIFICATIONS.md   逐项改动说明（含字节长度）
├── upstream/
│   └── EAgent-DS.exe       上游原版 EXE（未修改，GPL 复现基线）
├── dist/
│   └── EAgent-文心.exe     本 fork 构建产物（功能等价 + 换图标）
├── tools/
│   ├── patch_eagent.py     从原版 EXE 生成 fork 的补丁脚本
│   ├── set_icon.js         可选：替换 exe 图标（需 npm i resedit）
│   └── icon/wenxin_girl.ico
│
└── （以下为上游易语言工程源码，未修改）
    _EAgent.e  class/  config/  form/  resource/  Works/
    const.e.txt  struct.e.txt  global.e.txt  dll.e.txt
    project.etprj  icon.ico  index.html  auto_update.txt
    华侨精绘皮肤模块4.8.ec  精易模块[v11.1.5].ec  .github/
```

## 重要：为什么用「补丁脚本」

原作者用**易语言**开发。本 fork 没有改动 `.e` 源码，而是对发布版 EXE 做**等长字节替换**（不改变文件大小、不破坏 PE 结构），因此：

- 上游源码（`.e` / `.ec`）保持原样，已在仓库中；
- `tools/patch_eagent.py` 是这次修改的**完整、可复现的配方**：拿原版 EXE 跑一遍即可得到同样的 fork 二进制；
- `dist/EAgent-文心.exe` = `patch_eagent.py` 的输出 + 替换图标。

## 免责声明

- 本项目仅供学习研究，请遵守百度文心及各服务的使用条款。
- 修改后的 EXE 数字签名失效，Windows SmartScreen 可能提示“未知发布者”。
- 本项目与字节跳动、百度、DeepSeek 均无关联。
