<template>
    <div class="stat-container">
        <div v-if="currentStage !== null" class="transition-box" :key="currentStage">
            <p class="transition-text">{{ transitionText }}</p>
        </div>
        <div v-else class="box">
            <div v-for="(stage, index) in stages" :key="index" class="center-text">
                <p class="tag-title">{{ stage.title }}</p>
                <span class="tag-content">{{ stage.content }}</span>
                <span class="tag-unit">{{ stage.unit }}</span>
            </div>
        </div>
        <ul class="bg-bubbles">
			<li></li>
			<li></li>
			<li></li>
			<li></li>
			<li></li>
			<li></li>
			<li></li> 
			<li></li>
			<li></li>
			<li></li>
		</ul>
    </div>
</template>

<script setup name="ChatData">
import { ref, onMounted } from 'vue';
import { statsData } from "../js/getdata.js";

let stages = [
                {
                    text: `今年你在微信度过了${statsData.daysInWeChat}天`,
                    title: '今年你在微信度过了',
                    content: String(statsData.daysInWeChat),
                    unit: '天'
                },
                {
                    text: `陪伴你的好友一共有${statsData.numOfFriends}人`,
                    title: '陪伴你的好友一共有',
                    content: String(statsData.numOfFriends),
                    unit: '人'
                },
                {
                    text: `你给他们发送了${statsData.messagesSent}条消息`,
                    title: '你给他们发送了',
                    content: String(statsData.messagesSent),
                    unit: '条消息'
                },
                {
                    text: `收到了他们的${statsData.messagesReceived}条消息`,
                    title: '收到了他们的',
                    content: String(statsData.messagesReceived),
                    unit: '条消息'
                },
                {
                    text: `总计${statsData.totalWords}个字`,
                    title: '总计',
                    content: String(statsData.totalWords),
                    unit: '个字'
                }
            ];


const currentStage = ref(0);

const transitionText = ref(stages[0].text);

const advanceStage = () => {
    if (currentStage.value < stages.length - 1) {
        setTimeout(() => {
            stages = [
                {
                    text: `今年你在微信度过了${statsData.daysInWeChat}天`,
                    title: '今年你在微信度过了',
                    content: String(statsData.daysInWeChat),
                    unit: '天'
                },
                {
                    text: `陪伴你的好友一共有${statsData.numOfFriends}人`,
                    title: '陪伴你的好友一共有',
                    content: String(statsData.numOfFriends),
                    unit: '人'
                },
                {
                    text: `你给他们发送了${statsData.messagesSent}条消息`,
                    title: '你给他们发送了',
                    content: String(statsData.messagesSent),
                    unit: '条消息'
                },
                {
                    text: `收到了他们的${statsData.messagesReceived}条消息`,
                    title: '收到了他们的',
                    content: String(statsData.messagesReceived),
                    unit: '条消息'
                },
                {
                    text: `总计${statsData.totalWords}个字`,
                    title: '总计',
                    content: String(statsData.totalWords),
                    unit: '个字'
                }
            ];
            currentStage.value++;
            transitionText.value = stages[currentStage.value].text;
            // console.log(currentStage.value);
            // console.log(transitionText.value);
            advanceStage(); // 继续下一阶段
        }, 2000); // 每个阶段的停留时间
    } else {
        setTimeout(() => {
            currentStage.value = null; // 显示最终布局
        }, 2000);
    }
};

onMounted(() => {
    advanceStage();
});
</script>

<style scoped>
@font-face {
    font-family: "Pacifico-Regular";
    src: url("../../public/font/Pacifico-Regular.ttf") format("truetype");
    font-weight: normal;
    font-style: normal;
}

.stat-container {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    /* -webkit-animation: square 30s infinite;
    animation: square 30s infinite; */
}

.box {
    border-radius: 10px;
    /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); */
    width: 30%;
    height: 64%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    animation: fadeIn 1s;
}



.center-text {
    margin: 0.45rem 1rem;
    text-align: center;
}

.tag-title {
    font-size: 28px;
    color: white;
    margin: 5px 0px -10px 0px;
    font-family: 'Microsoft YaHei';
    /* font-weight: bold; */
}

.tag-content {
    font-size: 36px;
    background: linear-gradient(to right, #fffdd0, #d8efff); /* 渐变背景 */
    -webkit-background-clip: text; /* 仅在文字上显示背景 */
    -webkit-text-fill-color: transparent; /* 使文字填充颜色透明 */
    margin: 0px 0px -10px 0px;
    font-family: 'Pacifico-Regular';
    font-weight: bold;
}

.tag-unit {
    font-size: 20px;
    font-family: 'Microsoft YaHei';
    color: white;
    /* font-weight: bold; */
}

.transition-box {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    animation: fadeInOut 3s cubic-bezier(.32, .46, .48, .4) forwards;
}

.transition-text {
    font-size: 48px;
    background: linear-gradient(to right, #fffdd0, #d8efff); /* 渐变背景 */
    -webkit-background-clip: text; /* 仅在文字上显示背景 */
    -webkit-text-fill-color: transparent; /* 使文字填充颜色透明 */
    text-align: center;
    font-family: 'Microsoft YaHei';
    font-weight: bold;
}

@keyframes fadeInOut {
    0% {
        opacity: 0;
        transform: scale(0.8);
    }

    50% {
        opacity: 1;
        transform: scale(1);
    }

    100% {
        opacity: 0;
        transform: scale(0.8);
    }
}


@keyframes fadeIn {
    0% {
        opacity: 0;
        transform: scale(0.8);
    }

    100% {
        opacity: 1;
        transform: scale(1);
    }
}

.bg-bubbles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 3;
}
.bg-bubbles li {
  position: absolute;
  list-style: none;
  display: block;
  width: 40px;
  height: 40px;
  background-color: rgba(255, 255, 255, 0.15);
  bottom: -160px;
  -webkit-animation: square 30s infinite;
  animation: square 30s infinite;
  -webkit-transition-timing-function: linear;
  transition-timing-function: linear;
}
.bg-bubbles li:nth-child(1) {
  left: 10%;
}
.bg-bubbles li:nth-child(2) {
  left: 20%;
  width: 80px;
  height: 80px;
  -webkit-animation-delay: 2s;
          animation-delay: 2s;
  -webkit-animation-duration: 17s;
          animation-duration: 17s;
}
.bg-bubbles li:nth-child(3) {
  left: 25%;
  -webkit-animation-delay: 4s;
          animation-delay: 4s;
}
.bg-bubbles li:nth-child(4) {
  left: 40%;
  width: 60px;
  height: 60px;
  -webkit-animation-duration: 22s;
          animation-duration: 22s;
  background-color: rgba(255, 255, 255, 0.25);
}
.bg-bubbles li:nth-child(5) {
  left: 70%;
}
.bg-bubbles li:nth-child(6) {
  left: 80%;
  width: 120px;
  height: 120px;
  -webkit-animation-delay: 3s;
          animation-delay: 3s;
  background-color: rgba(255, 255, 255, 0.2);
}
.bg-bubbles li:nth-child(7) {
  left: 32%;
  width: 160px;
  height: 160px;
  -webkit-animation-delay: 7s;
          animation-delay: 7s;
}
.bg-bubbles li:nth-child(8) {
  left: 55%;
  width: 20px;
  height: 20px;
  -webkit-animation-delay: 15s;
          animation-delay: 15s;
  -webkit-animation-duration: 40s;
          animation-duration: 40s;
}
.bg-bubbles li:nth-child(9) {
  left: 25%;
  width: 10px;
  height: 10px;
  -webkit-animation-delay: 2s;
          animation-delay: 2s;
  -webkit-animation-duration: 40s;
          animation-duration: 40s;
  background-color: rgba(255, 255, 255, 0.3);
}
.bg-bubbles li:nth-child(10) {
  left: 90%;
  width: 160px;
  height: 160px;
  -webkit-animation-delay: 11s;
          animation-delay: 11s;
}
@-webkit-keyframes square {
  0% {
    -webkit-transform: translateY(0);
            transform: translateY(0);
  }
  100% {
    -webkit-transform: translateY(-900px) rotate(600deg);
            transform: translateY(-900px) rotate(600deg);
  }
}
@keyframes square {
  0% {
    -webkit-transform: translateY(0);
            transform: translateY(0);
  }
  100% {
    -webkit-transform: translateY(-900px) rotate(600deg);
            transform: translateY(-900px) rotate(600deg);
  }
}
@media screen and (max-width: 768px) {
  .box {
    width: 80%;
  }
}
@media (max-width: 480px) {
    .box {
    width: 80%;
    
  }
}

@media (max-width: 390px) {
    .box {
    width: 80%;
  }
  .center-text{
    margin: 0;
  }
  .tag-title{
    font-size: 20px;
  }
}
</style>