<template>
    <div class="chatdata-container">
        <div class="box">
            <div class="tag-title">
                <span class="tag-content">{{ chatData.mynickname }}</span> & <span class="tag-content">{{ chatData.hisnickname }}</span>的2024年
            </div>
            <div class="tag-title">
                一共发出<span class="tag-content">{{ chatData.totalmessages }}</span>条消息
            </div>
            <div class="tag-title">
                总计<span class="tag-content">{{ chatData.totalwords }}</span>字
            </div>
            <div class="tag-title">
                图片<span class="tag-content">{{ chatData.totalimages }}</span>张
            </div>
            <div class="tag-title">
                语音<span class="tag-content">{{ chatData.totalvoice }}</span>条
            </div>
            <div class="tag-title">
                表情包<span class="tag-content">{{ chatData.totalemojis }}</span>张
            </div>
            <div class="tag-title">
                我们最爱用的表情是
            </div>
            <div class="img-section">
                <img :src="chatData.emoji" alt="">
            </div>
        </div>
    </div>
</template>

<script setup>
import { chatData } from "../js/getdata.js";
console.log("chatData:", chatData)


</script>

<style scoped>
@font-face {
    font-family: "Pacifico-Regular";
    src: url("../../public/font/Pacifico-Regular.ttf") format("truetype");
    font-weight: normal;
    font-style: normal;
}

.chatdata-container {
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

.tag-title {
    font-size: 28px;
    color: #fff;
    margin: 5px 0px 0px 0px;
    font-family: 'Microsoft YaHei';
    /* font-weight: bold; */
}

.tag-content {
    font-size: 36px;
    background: linear-gradient(to right, #fffdd0, #d8efff); /* 渐变背景 */
    -webkit-background-clip: text; /* 仅在文字上显示背景 */
    -webkit-text-fill-color: transparent; /* 使文字填充颜色透明 */
    margin: 0px 5px;
    font-family: 'Pacifico-Regular';
    font-weight: bold;
}

.img-section{
    display: flex;
    justify-content: flex-end;
    flex-direction: column;
}

img {
    margin-left: 120px;
    margin-top: 30px;
    width: 100px;
    height: 100px;
}

@media screen and (max-width: 768px) {
    .box {
        width: 80%;
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
@media screen and (max-width: 390px) {
    .box{
        position: absolute;
        top: 15%;
    }
    .tag-content{
        font-size: 24px;
    }
}
</style>