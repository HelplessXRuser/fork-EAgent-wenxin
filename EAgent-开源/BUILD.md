# 构建 / 复现

## 1. 生成功能版（必须）

需要 Python 3。

```bash
python tools/patch_eagent.py upstream/EAgent-DS.exe dist/EAgent-文心.exe
```

- 输入必须是**未修改**的发布版 EXE；
- 脚本只做等长字节替换，输出大小与输入相同（2602368）；
- 校验：输出 sha256 应为 `3ec66f0f3526a50131f97c3803ef7e2169a89b15020d8f702df99eb795fc502e`。

## 2. 替换图标（可选）

需要 Node.js：

```bash
npm install resedit
node tools/set_icon.js dist/EAgent-文心.exe tools/icon/wenxin_girl.ico dist/EAgent-文心.exe
```

- 写入 3 个图标组、每个 7 个尺寸；
- 会使数字签名失效（Windows 可能提示“未知发布者”）；
- resedit 会重排图标资源，重新构建的产物大小可能与 `dist/EAgent-文心.exe`（3219456）不同，功能一致。

## 3. 从源码构建（完全合规的做法）

若要产出「源码 ⇒ 二进制」可完全对应的版本：

1. 安装**易语言 5.x**；
2. 打开 `project.etprj` / `_EAgent.e`；
3. 按 `docs/MODIFICATIONS.md` 在源码中做等价修改：
   - `1_启动调试浏览器.ps1` 的 `$Url`；
   - 界面文本 `DeepSeek` → `百度文心`；
   - `deepseek_debug_profile` → `wenxin___debug_profile`；
   - `$Selectors` 与 `$lastAssistJs`；
   - 页面匹配正则；
4. 编译输出 EXE。

> 源码路径/行号可能随上游版本变化，建议以 `tools/patch_eagent.py` 中的字符串定位逻辑为准。

## 目录说明

| 目录 | 内容 |
|------|------|
| `upstream/` | 上游原版 EXE（未修改，仅作复现基线） |
| `dist/` | 本 fork 产物 |
| `tools/` | 补丁脚本、图标替换脚本与图标资源 |
| `docs/` | 改动说明 |
