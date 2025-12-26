# 此项目fork自 [WeChatMsg](https://github.com/LC044/WeChatMsg)，使用gemini新增了2025年度报告，目前暂无gui界面。

微信各版本下载（这里可以下载对应的微信任何版本）：https://github.com/cscnk52/wechat-windows-versions

> [!WARNING]
> **版本注意事项**：
> * 微信版本过低可能导致无法登录。
> * 微信版本过高可能导致无法获取密钥。
> * 目前支持的最高版本为 **4.0.3.22**，建议下载此版本进行操作。

## 现已支持微信4.0，[点击查看详细设计文档](https://blog.lc044.love/post/13)

<h1 align="center">我的数据我做主</h1>
<div align="center">
    <a href="https://github.com/1658671838/WeChatMsg_fix/stargazers">
        <img src="https://img.shields.io/github/stars/1658671838/WeChatMsg_fix.svg" />
    </a>
    <a href="https://github.com/1658671838/WeChatMsg_fix/network/members" target="_blank">
        <img alt="GitHub forks" src="https://img.shields.io/github/forks/1658671838/WeChatMsg_fix?color=eb6ea5">
    </a>
</div>

<blockquote>
<div style="background-color: #eaf7ea; border-radius: 10px; padding: 20px; position: relative;">
  <div style="position: relative;">
    <div style="position: absolute;top: 0;bottom: 0;left: 0;width: 2px;background-color: #000000;"></div>
    <h2>前言</h2>
    <div style="text-indent: 2em;">
        <a align="center" href="https://memotrace.cn/"><img src="./doc/images/logo3.0.png"/></a>
        <p style="text-indent:2em;">我深信有意义的不是微信，而是隐藏在对话框背后的一个个<strong>深刻故事</strong>。未来，每个人都能拥有AI的陪伴，而你的数据能够赋予它有关于你过去的珍贵记忆。我希望每个人都有将自己的生活痕迹👨‍👩‍👦👚🥗🏠️🚴🧋⛹️🛌🛀留存的权利，而不是遗忘💀。</p>
        <p style="text-indent:2em;">AI的发展不仅仅是技术的提升，更是情感💞的延续。每一个对话、每一个互动都是生活中独一无二的片段，是真实而动人的情感交流。因此，我希望AI工作者们能够<strong>善用这些自己的数据</strong>，用于培训独特的、属于个体的人工智能。让<strong>个人AI成为生活中的朋友</strong>，能够理解、记录并分享我们的欢笑、泪水和成长。</p>
        <p style="text-indent:2em;">那天，AI不再是高不可攀的存在，而是融入寻常百姓家的一部分。因为<strong>每个人能拥有自己的AI</strong>，将科技的力量融入生活的方方面面。这是一场关于真情实感的革命，一场让技术变得更加人性化的探索，让我们共同见证未来的美好。</p>
        <p align="center"><strong>所以《留痕》</strong></p>
    </div>
  </div>
</div>
</blockquote>

## 3.0 全面来袭

### 全面适配微信4.0 [点击查看详细设计文档](https://blog.lc044.love/post/13)

![数据库架构设计图](./doc/images/数据库架构设计图.png)

  * 全新框架、重构底层逻辑
  * 更低的内存占用
  * 更快的导出速度



## 🍉功能

- 🔒️🔑🔓️Windows本地微信数据库（支持微信4.0）
- 还原微信聊天界面
    - 🗨文本✅
    - 🏝图片✅
    - 拍一拍等系统消息✅ 
- 导出数据
  - 批量导出数据✅ 
  - 导出联系人✅ 
  - sqlite数据库✅ 
  - HTML✅ 
    - 文本、图片、视频、表情包、语音、文件、分享链接、系统消息、引用消息、合并转发的聊天记录、转账、音视频通话、位置分享、名片、小程序、视频号
    - 支持时间轴跳转
    - 引用消息可定位到原文
    - 分享链接、小程序支持超链接跳转
    - 合并转发的聊天记录支持展开
  - CSV文档✅ 
  - TXT文档✅ 
  - Word文档✅
- 分析聊天数据，做成[可视化年报]

## 2025年度报告

### 预览

[个人年度报告在线预览](https://memotrace.cn/2024/single/)


### 源码地址

[https://github.com/LC044/AnnualReport](https://github.com/LC044/AnnualReport)

# ⌛使用


## 源码运行

### 1. 环境准备
1. 下载并安装 [Python 3.10+](https://www.python.org/downloads/)，安装时请勾选 `Add Python to PATH`。
2. 下载并安装 **微信 4.0.3.22** 版本。
3. 下载并安装 [Node.js](https://nodejs.org/) (用于预览网页版报告)。

### 2. 安装依赖
在项目根目录下打开终端，运行以下命令安装 Python 依赖：
```bash
pip install -r requirements.txt
```

### 3. 生成年度报告数据
1. 使用文本编辑器打开 `generate_report_data.py` 文件。
2. 修改 `db_dir` 变量，将其改为您电脑上微信数据库的实际路径（通常位于 `WeChat Files\wxid_xxxx\db_storage`）。
3. 运行脚本生成数据：
```bash
python generate_report_data.py
```

### 4. 启动报告预览
1. 进入报告前端目录：
```bash
cd AnnualReport/report-2025/single
```
2. 安装前端依赖并启动服务：
```bash
npm install
npm run dev
```
3. 脚本运行成功后会显示一个本地链接（如 `http://localhost:5173`），复制到浏览器打开即可查看您的2025年度报告。

## PC端使用过程中部分问题解决（可参考）

#### 🤔如果您在pc端使用的时候出现问题，可以先参考以下方面，如果仍未解决，可以在群里交流~

* 不支持Win7
* 不支持Mac(未来或许会实现)
* 遇到问题四大法宝
  * 首先要删除app/Database/Msg文件夹
  * 重启微信
  * 重启exe程序
  * 重启电脑
  * 换电脑
如果您在运行可执行程序的时候出现闪退的现象，请右击软件使用管理员权限运行。

# 🏆致谢

<details>

* PC微信工具:[https://github.com/xaoyaoo/PyWxDump](https://github.com/xaoyaoo/PyWxDump)
* PyQt组件库:[https://github.com/PyQt5/CustomWidgets](https://github.com/PyQt5/CustomWidgets)
* 得力小助手:[ChatGPT](https://chat.openai.com/) [Gemini](https://gemini.google.com/)

</details>

---
> \[!IMPORTANT]
> 
> 声明：该项目有且仅有一个目的：“留痕”——我的数据我做主，前提是“我的数据”其次才是“我做主”，禁止任何人以任何形式将其用于任何非法用途，对于使用该程序所造成的任何后果，所有创作者不承担任何责任🙄<br>
> 该软件不能找回删除的聊天记录，任何企图篡改微信聊天数据的想法都是无稽之谈。<br>
> 本项目所有功能均建立在”前言“的基础之上，基于该项目的所有开发者均不能接受任何有悖于”前言“的功能需求，违者后果自负。<br>
> 如果该项目侵犯了您或您产品的任何权益，请联系我删除<br>
> 软件贩子勿扰，违规违法勿扰，二次开发请务必遵守开源协议

# 🤝贡献者

<a href="https://github.com/lc044/wechatmsg/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=lc044/wechatmsg" />
</a>
<a href="https://github.com/1658671838/WeChatMsg_fix/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=1658671838/WeChatMsg_fix" />
</a>

# 🎄温馨提示

如果您在使用该软件的过程中

* 发现新的bug
* 有新的功能诉求
* 操作比较繁琐
* 觉得UI不够美观
* 等其他给您造成困扰的地方

请提起[issue](https://github.com/1658671838/WeChatMsg_fix/issues)，我将尽快为您解决问题

如果您是一名开发者，有新的想法或建议，欢迎[fork](https://github.com/1658671838/WeChatMsg_fix/forks)
该项目并发起[PR](https://github.com/1658671838/WeChatMsg_fix/pulls)，我将把您的名字写入贡献者名单中

# License

WeChatMsg is licensed under [MIT](./LICENSE).

Copyright © 2022-2024 by SiYuan.
Copyright © 2025 by xuncha.
