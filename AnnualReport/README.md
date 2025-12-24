# 年度报告模板

## 运行示例

[个人年度报告在线预览](https://memotrace.cn/2024/single/)

手机可以扫码观看

<img src="./doc/image/qrcode2.png" height="300px"/>

![](/doc/demo1.gif)

[双人年度报告在线预览](https://memotrace.cn/2024Report/)

手机可以扫码观看

<img src="./doc/image/qrcode1.png" height="300px"/>

## 使用

需要安装 node.js 版本 20

### 克隆代码

```bash
git clone https://github.com/LC044/AnnualReport

cd AnnualReport

cd report-2024

cd single
```

### 安装依赖

```bash
npm install
```

### 运行

```bash
npm run dev
```

### 打包

```bash
npm run build
```

### 修改数据

为了方便修改、自定义，所有数据均定义在getData.js里，你可以只修改这里面的数据来定制专属于你自己的年度报告。

```javascript
/**********第一页************/
// Welcome.vue
// 欢迎页数据
export const Welcome_data = reactive({
    avatarSrc: './header/header7.webp',
    nickname: "初霜",
    descriptionText: {
        hello: "Hello World!",
        text1: "时光荏苒，转眼间我们又走过了一年。",
        text2: "在过去的365天里，从深夜的长谈到清晨的祝福，从好友间的调侃到工作中的忙碌……",
        text4: "这些聊天记录，是属于你的独家记忆。",
        text7: "打开报告，开启你的专属年度记忆吧！"
    }
});



/**********第二页************/
// ChatData.vue
// 全年消息统计数据
export var statsData = {
    // 一年中的天数
    daysInWeChat: 365, 
    // 聊天人数
    numOfFriends: 113,
    // 发出的消息数
    messagesSent: 14404,
    // 收到的消息数
    messagesReceived: 18708,
    // 总字数
    totalWords: 493092
};
```