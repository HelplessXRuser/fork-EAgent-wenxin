# 改动清单（MODIFICATIONS）

基线与产物：

| 项 | 值 |
|----|----|
| 上游仓库 | https://github.com/YaoGaoChaoLe/EAgent |
| 上游提交 | `1b44514` |
| 原版 EXE | `upstream/EAgent-DS.exe`，2602368 字节，sha256 `06863b789e20a8872397548a38693aed345c4edd2d708a9b1b8f7001ce36e26c` |
| 纯补丁产物 | 2602368 字节，sha256 `3ec66f0f3526a50131f97c3803ef7e2169a89b15020d8f702df99eb795fc502e` |
| 最终产物（含图标） | `dist/EAgent-文心.exe`，3219456 字节，sha256 `6c643ee26149d5681fce48e941fd7a65ae2c5a21abc9a56f828b83bc9fae6838` |

所有改动均为**等长字节替换**，文件大小与 PE 布局不变。

> 注：`upstream/EAgent-DS.exe` 为上游新版原始 EXE（旧版 `不是游戏-EAgent.exe` 已不在本机，如需可从上上游 Releases 补充）。
> 重新执行 `patch + set_icon` 时，图标资源布局可能略有差异，故最终产物大小不一定等于 `dist/` 中的 3219456，功能一致。

## 1. 默认网页地址

| 位置 | 原值 | 新值 | 长度 |
|------|------|------|------|
| `1_启动调试浏览器.ps1` 的 `$Url` 默认值 | `https://chat.deepseek.com` | `https://wenxin.baidu.com/` | 25 → 25 |

## 2. 界面文字

| 原值 | 新值 | 次数 | 说明 |
|------|------|------|------|
| `DeepSeek` | `百度文心`（GBK，8 字节） | 8 | 标题、帮助、错误提示、以及用于查找浏览器窗口的标题匹配串 |
| `向deepseek发送文本` | `向百度文心发送文本` | 4 | 工具/命令标题 |
| `永远不要把deepseek窗口关掉` | `永远不要把百度文心窗口关掉` | 1 | 提示语 |

## 3. 独立浏览器存档

| 原值 | 新值 | 次数 |
|------|------|------|
| `deepseek_debug_profile` | `wenxin___debug_profile` | 3 |

使文心版与 DeepSeek 版各自使用独立浏览器配置，登录/会话互不串。

## 4. CDP 页面匹配正则

| 原值 | 新值 | 长度 |
|------|------|------|
| `chat\.deepseek\.com` | `wenxin\.baidu\.com.` | 19 → 19 |

## 5. 文心页面的 DOM 选择器（`$Selectors`）

```powershell
$Selectors = @{
    assistant = @('.answer-box')
    user      = @('[class*="answer-ask"]')
    input     = @('#chat-textarea','textarea')
    sendBtn   = @('#ci-submit-button-ai','.ci-submit-button-ai-active')
}
```

- `#chat-textarea`：文心输入框
- `#ci-submit-button-ai`：发送按钮
- `.answer-box`：AI 回答容器
- `[class*="answer-ask"]`：用户消息容器

## 6. 读取回答时过滤占位文字（`$lastAssistJs`）

文心在生成期会先往回答框写入「**正在思考**」「正在搜索…」等占位文字，且会稳定超过 1 秒。原逻辑「文本稳定 10 次即完成」会把它当成回答，导致界面一直显示“正在思考”。

改为：

```js
(function(){
  var a=pick('assistant'), e=a.pop(), t=(e&&e.innerText)||'';
  return (t.length>5 && !/^正在/.test(t)) ? t : '';
})()
```

即：改用 `innerText`，长度 ≤5 或以「正在」开头时视为空，只有真正的回答正文才参与“稳定判定”。

## 7. 图标（可选）

`tools/icon/wenxin_girl.ico`（7 个尺寸：16–256），通过 `tools/set_icon.js` 写入 PE 图标资源。
此步骤会**使原数字签名失效**。

## 8. 项目介绍页与 README

- `index.html` 全量改写为文心版：
  - 标题/导航/首屏/页脚：`EAgent` → `EAgent-文心`；
  - 「起源」「快速使用」「实现原理」「声明」等文案中的 DeepSeek → 百度文心；
  - 下载链接改为 `./dist/EAgent-文心.exe`；
  - 新增 fork 说明：上游归属、GPL-3.0、改动清单入口。
- `README.md` 重写为文心版：差异对照表、环境要求、快速使用、原理、目录结构、构建、声明、致谢。

## 9. 用户协议替换

| 项 | 值 |
|----|----|
| 原引用 | `https://cdn.deepseek.com/policies/zh-CN/deepseek-terms-of-use.html`（DeepSeek 用户协议） |
| 新引用 | `https://yiyanapp.baidu.com/app/userprivacy`（《文心用户协议》，官方页面） |

> 仅替换引用链接，未复制协议正文（避免版权问题），协议内容以百度官方页面为准。

## 未改动项（有意保留）

| 项 | 原因 |
|----|------|
| 控件名 `编辑框_向deepseek发信息` | 内部引用名，改了会破坏代码引用 |
| `https://status.deepseek.com` 链接 | 状态页链接，无百度等价物 |
| 调试串 `no deepseek page` | 仅控制台输出，不影响功能 |
| 端口 `9222` | 与主程序内部常量一致，改动会导致重复拉起浏览器 |
| 发送方式（回车提交） | 该版本验证可用，保持原逻辑 |
