<template>
    <div class="stat-container">
        <div v-if="currentStage !== null" class="transition-box" :key="currentStage">
            <p class="transition-text">{{ transitionText }}</p>
        </div>
        <div v-else class="box">
            <div class="center-text">
                <p class="tag-title">我们第一次聊天在</p>
                <span class="tag-content">{{ firstChatData.firstChatDate.year }}</span>
                <span class="tag-unit">年</span>
                <span class="tag-content">{{ firstChatData.firstChatDate.month }}</span>
                <span class="tag-unit">月</span>
                <span class="tag-content">{{ firstChatData.firstChatDate.day }}</span>
                <span class="tag-unit">日</span>
            </div>
            <div class="center-text">
                <p class="tag-title">距今已有</p>
                <span class="tag-content">{{ daysSinceFirstChat }}</span>
                <span class="tag-unit">天</span>
            </div>
            <div class="center-text">
                <p class="tag-title">2024年的第一段对话</p>
                <p class="tag-title">是由<span class="tag-content">{{ firstChatData.initiator }}</span>发起的</p>
            </div>

            <div class="message-box">
                <div v-for="(message, index) in firstChatData.conversation" :key="message.id"
                    :class="['item', message.side === 'left' ? 'item-left' : 'item-right']">
                    <div v-if="message.side === 'left'" class="avatar">
                        <img :src="hisavatar" loading="lazy">
                    </div>
                    <div
                        :class="message.side === 'left' ? 'content-wrapper content-wrapper-left' : 'content-wrapper content-wrapper-right'">

                        <div class="bubble" :class="message.side === 'left' ? 'bubble-left' : 'bubble-right'">{{
            message.content }}
                        </div>

                    </div>
                    <div v-if="message.side === 'right'" class="avatar">
                        <img :src="myavatar" loading="lazy">
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup name="FirstData">
import { ref, onMounted } from 'vue'
import { firstChatData, myavatar, hisavatar, FirstData_isReady } from '../js/getdata.js'

const emit = defineEmits();

console.log("firstChatData", firstChatData.value)
const daysSinceFirstChat = ref(0)
const stages = ref([{ text: '我们第一次聊天在' }])
const currentStage = ref(0);
const transitionText = ref('');

const advanceStage = () => {
    if (currentStage.value < stages.value.length - 1) {
        setTimeout(() => {
            currentStage.value++;
            transitionText.value = stages.value[currentStage.value].text;
            advanceStage();
        }, 2000);
    } else {
        FirstData_isReady.value = true;
        emit('load-complete');
        setTimeout(() => {
            currentStage.value = null;
        }, 2000);
    }
};

onMounted(() => {
    FirstData_isReady.value = false;
    emit('loading');
    const date = new Date(firstChatData.value.firstChatDate.year, firstChatData.value.firstChatDate.month - 1, firstChatData.value.firstChatDate.day);
    daysSinceFirstChat.value = Math.floor((new Date() - date) / (1000 * 60 * 60 * 24));

    stages.value.push(
        { text: `${firstChatData.value.firstChatDate.year}年${firstChatData.value.firstChatDate.month}月${firstChatData.value.firstChatDate.day}日` },
        { text: `距今已有${daysSinceFirstChat.value}天` },
        { text: '2024年的第一段对话' },
        { text: `是由${firstChatData.value.initiator}发起的` }
    );
    transitionText.value = stages.value[currentStage.value].text;
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
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.box {
    border-radius: 10px;
    width: 30%;
    height: 64%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    animation: fadeIn 1s;
}

@media screen and (max-width: 768px) {
    .box {
        width: 80%;
    }
}

.center-text {
    margin: 0.45rem 1rem;
    text-align: center;
}

.tag-title {
    font-size: 28px;
    color: #fff;
    margin: 5px 0px -10px 0px;
    font-family: 'Microsoft YaHei';
    /* font-weight: bold; */
}

.tag-content {
    font-size: 36px;
    background: linear-gradient(to right, #fffdd0, #d8efff);
    /* 渐变背景 */
    -webkit-background-clip: text;
    /* 仅在文字上显示背景 */
    -webkit-text-fill-color: transparent;
    /* 使文字填充颜色透明 */
    margin: 0px 0px -10px 0px;
    font-family: 'Pacifico-Regular';
    font-weight: bold;
}

.tag-unit {
    font-size: 20px;
    font-family: 'Microsoft YaHei';
    color: #fff;
    font-weight: bold;
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
    background: linear-gradient(to right, #fffdd0, #d8efff);
    /* 渐变背景 */
    -webkit-background-clip: text;
    /* 仅在文字上显示背景 */
    -webkit-text-fill-color: transparent;
    /* 使文字填充颜色透明 */
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


.message-box {
    display: flex;
    align-items: center;
    flex-direction: column;
    margin-top: 20px;
    width: 30vw;
    height: 60vh;
}


.bubble {
    white-space: pre-wrap;
    padding: 10px 11px;
    border-radius: 5px;
    color: #1f1f1f;
    font-size: 14px;
    max-width: 400px;
    position: relative;
    word-wrap: break-word;
    word-break: normal;
}

.item-left .bubble {
    margin-left: 15px;
    background-color: rgba(255, 255, 255, 0.1);
}

.item-left .bubble:before,
.item-right .bubble:before {
    content: "";
    position: absolute;
    width: 0;
    height: 0;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent
}

.item-left .bubble:before {
    left: -20px;
    border-left: 10px solid transparent;
    border-right: 10px solid #fff;
    opacity: 0.1;
}

.item-right .bubble {
    margin-right: 15px;
    background-color: rgba(169, 250, 115, 0.4);
}

.item-right .bubble:before {
    border-left: 10px solid #a9fa73;
    border-right: 10px solid transparent;
    right: -20px;
    opacity: 0.4;
}

@media screen and (max-width: 768px) {
    .message-box {
        width: 80vw;
        height: 60vh;
    }

    .bubble {
        max-width: 280px;
    }

    .item-right .bubble {
        margin-right: 8px;
    }

    .item-left .bubble {
        margin-left: 8px;
    }

    .item-left .bubble:before {
        content: "";
        position: absolute;
        width: 0;
        height: 0;
        border-left: 8px solid transparent;
        border-top: 8px solid transparent;
        border-right: 8px solid #fff;
        border-bottom: 8px solid transparent;
        left: -16px;
    }

    .item-right .bubble:before {
        content: "";
        position: absolute;
        width: 0;
        height: 0;
        border-left: 8px solid #9eea6a;
        border-top: 8px solid transparent;
        border-right: 8px solid transparent;
        border-bottom: 8px solid transparent;
        right: -16px;
    }
}

.item {
    margin-top: 15px;
    display: flex;
    width: 100%;
}

.item-refer {
    margin-top: 4px;
}

.item.item-right {
    justify-content: flex-end;
}

.item.item-center {
    justify-content: center;
}

.item.item-center span {
    font-size: 12px;
    padding: 2px 4px;
    color: #fff;
    background-color: #dadada;
    border-radius: 3px;
    -moz-user-select: none;
    /*火狐*/
    -webkit-user-select: none;
    /*webkit浏览器*/
    -ms-user-select: none;
    /*IE10*/
    -khtml-user-select: none;
    /*早期浏览器*/
    user-select: none;
}

.content-wrapper {
    display: flex;
    flex-direction: column;
    max-width: 80%;
}

.content-wrapper-left {
    align-items: baseline;
}

.content-wrapper-right {
    align-items: flex-end;
}

.displayname {
    margin-left: 13px;
    margin-left: 13px;
    font-size: 13px;
    margin-bottom: 5px;
    color: darkgray;
}

.chat-image img,
.chat-file img {
    margin-right: 18px;
    margin-left: 18px;
    max-width: 300px;
    /*max-height: auto;*/
}

.avatar img {
    width: 42px;
    height: 42px;
    border-radius: 3px;
    user-select: none;
}

@media screen and (max-width: 390px) {
    .box {
        position: absolute;
        top: 15%;
    }

    .message-box {
        width: 80vw;
        height: 60vh;
    }

    .center-text {
        font-size: 24px;
        margin: 0.45rem 0rem;
        text-align: center;
    }

    .transition-text {
        font-size: 40px;
        text-align: center;
        font-family: 'Microsoft YaHei';
        font-weight: bold;
    }
}
</style>