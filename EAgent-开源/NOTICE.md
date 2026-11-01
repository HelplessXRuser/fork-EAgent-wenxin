# NOTICE / 版权与合规声明

## 上游

本仓库包含并衍生自 **EAgent**：

- 项目：https://github.com/YaoGaoChaoLe/EAgent
- 版权：Copyright (C) EAgent 原作者（YaoGaoChaoLe）
- 许可证：**GNU General Public License v3.0**（全文见根目录 `LICENSE`）

上游源码文件（`_EAgent.e`、`class/`、`config/`、`form/`、`resource/`、`Works/`、`*.e.txt`、`*.ec`、`project.etprj`、`icon.ico`、`index.html` 等）**均未修改**，版权归原作者所有。

## 本 fork 的修改

- 修改者：本仓库维护者
- 修改日期：2026-11-01
- 修改内容：见 `docs/MODIFICATIONS.md`（默认后端改为百度文心、界面文字、独立存档、DOM 选择器、回答读取过滤、图标）
- 本 fork 的整体（含修改）依据 GPL-3.0 授权分发。

## 关于「对应源码」

GPL-3.0 要求分发修改后的二进制时提供对应的完整源码。本 fork 通过**对发布版 EXE 做等长字节替换**实现，未改动易语言 `.e` 源码，因此：

1. 上游完整源码已随仓库提供（未修改）；
2. `tools/patch_eagent.py` 提供了本次修改的**完整、可复现配方**——对 `release/EAgent-DS.exe` 运行即可得到与本仓库 `dist/` 中功能一致的二进制（图标除外）；
3. 若需在源码层面维护该 fork，建议基于上游 `.e` 工程直接修改，或向上游提交 PR。

> 说明：本声明不是法律意见。正式发布前建议与原作者确认，或直接在上游源码上实现同样改动，以完全满足 GPL 的源码提供义务。

## 商标与免责

- “DeepSeek”“百度”“文心”“豆包”等名称与商标归各自权利人所有。
- 本项目与上述公司无任何关联，仅供学习研究。
- 请遵守目标网站的服务条款；因使用本项目产生的任何后果由使用者自行承担。
