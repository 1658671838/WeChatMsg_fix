<template>
    <div class="card-container">
        <div class="card-background" id="capture">
            <div class="card">
                <div class="common" id="common">
                    <div class="avatar1">
                        <img id="common-my-avatar" :src="myavatar" alt="">
                    </div>
                    <div class="avatar2">
                        <img id="common-ta-avatar" :src="hisavatar" alt="">
                    </div>
                </div>

                <div class="title">
                    <div class="nickname">
                        <span id="my-nickname">{{ mynickname }}</span>
                        <span>&</span>
                        <span id="ta-nickname">{{ hisnickname }}</span>
                    </div>
                    <div class="reportname">{{ reportName }}</div>
                </div>
                <div class="times">
                    <div class="sentence">
                        <div class="tag-template">第一次聊天在</div>
                        <div>
                            <span class="tag-content" id="first-time">{{ CardData.firstChatDate }}</span>
                        </div>
                    </div>

                    <div class="sentence">
                        <div class="tag-template">已经相识</div>
                        <div>
                            <span class="tag-content" id="time-from-today">{{ daysSinceFirstChat }}</span>
                            <span class="tag-template">天</span>
                        </div>
                    </div>

                    <div class="sentence">
                        <div>
                            <span class="tag-content" id="year">{{ CardData.mostChatYear }}</span>
                            <span class="tag-template">年</span>
                            <span class="tag-content" id="month">{{ CardData.mostChatMonth }}</span>
                            <span class="tag-template">月</span>
                        </div>
                        <div>
                            <span class="tag-template">发送了</span>
                            <span class="tag-content" id="month-num">{{ CardData.mostChatCount }}</span>
                            <span class="tag-template">条消息</span>
                        </div>
                        <div>
                            <span class="tag-template">对你的话说不完</span>
                        </div>
                    </div>

                </div>
                <div class="sum-up">
                    {{ summaryText }}
                </div>
                <div class="tags">
                    <div class="left">
                        <div v-for="tag in CardData.leftTags" :key="tag.label">
                            <div class="tag-template">{{ tag.label }}</div>
                            <div>
                                <span class="tag-content">{{ tag.value }}</span>
                                <span class="tag-template">{{ tag.unit }}</span>
                            </div>
                        </div>
                    </div>
                    <div class="right">
                        <div v-for="tag in CardData.rightTags" :key="tag.label">
                            <div class="tag-template">{{ tag.label }}</div>
                            <div v-if="tag.image">
                                <img :src="tag.image" alt="Tag Image">
                            </div>
                            <div v-else>
                                <span class="tag-content">{{ tag.value }}</span>
                            </div>
                        </div>
                        <div class="qrcode">
                            <img src="../../public/url_qrcode.svg" alt="QrCode">
                        </div>
                    </div>
                </div>
                <div class="copyright">
                    <img src="../../public/favicon.ico" alt="">
                    <span>memotrace.cn</span>
                </div>

                <div class="bottom">
                    <div>{{ bottomText }}</div>
                </div>
            </div>
        </div>
        <div class="qr-container" id="qr-container" v-show="qrshow">
            <div class="common" id="common">
                <div class="avatar1">
                    <img id="common-my-avatar" :src="myavatar" alt="">
                </div>
                <div class="avatar2">
                    <img id="common-ta-avatar" :src="hisavatar" alt="">
                </div>
                <div class="qr-title">
                    <div>2024</div>
                    <div>微信年度报告</div>
                </div>
            </div>

            <div class="url-qr" id="url-qr">
            </div>
            <div class="footer">
                <div>微信扫一扫查看年度报告</div>
            </div>
        </div>

    </div>
    <div class="buttons">
        <button @click="captureImage" class="welcome-button">
            下载卡片
            <div class="hoverEffect">
                <div></div>
            </div>
        </button>
        <button @click="uploadReport" class="upload-button">
            分享报告
            <div class="hoverEffect">
                <div></div>
            </div>
        </button>
        <button @click="captureQRCode" class="QRCode-button" v-show="qrshow">
            二维码下载
            <div class="hoverEffect">
                <div></div>
            </div>
        </button>
    </div>
</template>

<script setup>
import {
    key,
    wxid,
    reportName,
    bottomText,
    CardData,
    daysSinceFirstChat,
    cardName,
    firstChatData,
    chatData,
    chatdescription,
    Calendardata,
    keyWordsData,
    quarterData,
    myavatar,
    hisavatar,
    mynickname,
    hisnickname,
    summaryText,
    UPLOAD_URL
} from "../js/getdata.js";
import { ref } from "vue";
import QRcodestyling from 'qr-code-styling'
import domtoimage from 'dom-to-image';

const uploda_data = {
    myavatar: myavatar.value,
    hisavatar: hisavatar.value,
    mynickname: mynickname.value,
    hisnickname: hisnickname.value,
    firstChatData: firstChatData.value,
    totalChatData: chatData.value,
    timePeriodData: chatdescription.value,
    CalendarData: Calendardata.value,
    keyWordData: keyWordsData.value,
    Quarter_SummaryData: quarterData.value,
    summaryText: summaryText.value,
};
const qrshow = ref(false);


function captureImage() {
    cardName.value = `${CardData.value.mynickname}&${CardData.value.hisnickname}的2024年度报告`;
    var element = document.getElementById('capture');
    var scale = 2;
    var width = element.offsetWidth;
    var height = element.offsetHeight;
    domtoimage.toBlob(element, {
        width: width * scale,
        height: height * scale,
        style: {
            transform: 'scale(' + scale + ')',
            transformOrigin: 'top left',
            width: width + 'px',
            height: height + 'px'
        }
    }).then(function (blob) {
        var link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = cardName.value;
        document.body.appendChild(link);
        element.classList.remove('dark-style');
        link.click();
        document.body.removeChild(link);
    })
        .catch(function (error) {
            console.error('oops, something went wrong!', error);
        });
    console.log('captureImage');
}

function captureQRCode() {
    var element = document.getElementById('qr-container');
    var scale = 2;
    var width = element.offsetWidth;
    var height = element.offsetHeight;
    domtoimage.toBlob(element, {
        width: width * scale,
        height: height * scale,
        style: {
            transform: 'scale(' + scale + ')',
            transformOrigin: 'top left',
            width: width + 'px',
            height: height + 'px'
        }
    }).then(function (blob) {
        var link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `${cardName.value}QRcode`;
        document.body.appendChild(link);
        element.classList.remove('dark-style');
        link.click();
        document.body.removeChild(link);
    })
        .catch(function (error) {
            console.error('oops, something went wrong!', error);
        });
    console.log('captureQrcode');
}

function uploadReport() {
    var userConfirmed = confirm("注意！！！\n本页面将会上传至云端，别人可通过链接查看该网页，该操作不会上传您的其他任何信息，页面将在下个版本更新之后删除，请注意链接生效时间。\n点击“确认”代表您同意上传，否则请点击“取消");
    if (userConfirmed) {
        // User clicked OK, perform the upload and display QR code
        uploadAndDisplayQRCode();
    } else {
        // User clicked Cancel or closed the dialog
        alert("Upload canceled.");
    }
}

function uploadAndDisplayQRCode() {
    // Simulate a GET request to the server endpoint
    displayQRCode("https://memotrace.cn/2024Report/");
}

function displayQRCode(url) {
    const qrCode = new QRcodestyling({
        width: 200,
        height: 200,
        type: "svg",
        data: url,
        cornersSquareOptions: {
            type: "extra-rounded", // 圆角方块，与主体一致
            gradient: {
                type: "linear",
                rotation: 90, // 同方向渐变
                colorStops: [
                    { offset: 0, color: "#d2cdff" }, // 起始色
                    { offset: 1, color: "#ffffd0" } // 结束色
                ]
            }
        },
        cornersDotOptions: {
            type: "dot", // 圆形，与主体圆角协调
            gradient: {
                type: "linear",
                rotation: 90, // 同方向渐变
                colorStops: [
                { offset: 0, color: "#d2cdff" }, // 起始色
                { offset: 1, color: "#ffffd0" } // 结束色
                ]
            }
        },
        dotsOptions: {
            type: "rounded", // 圆角
            gradient: {
                type: "linear",
                rotation: 90,
                colorStops: [
                { offset: 0, color: "#d2cdff" }, // 起始色
                { offset: 1, color: "#ffffd0" } // 结束色
                ]
            }
        },
        image: "data:image/png;base64,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",

        backgroundOptions: {
            color: "rgba(0,0,0,0)" // 设置背景颜色为透明
        },
    });
    qrCode.append(document.getElementById("url-qr"));
    qrshow.value = true;
}


</script>
<style scoped>
.card-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 90vh;
    /* background-image: linear-gradient(180deg,#5ee7df,#b490ca); */
    perspective: 1000px;
}

.card-background {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 800px;
    width: 450px;
    /* background-image: linear-gradient(200deg, #fbc2eb, #a6c1ee); */
    perspective: 1000px;
}

.card {
    position: relative;
    width: 360px;
    height: 580px;
    margin: 20px;
    /* background-image: linear-gradient(200deg, #a6c1ee, #fbc2eb, #fff); */
    background: radial-gradient(200% 100% at bottom center, #f7f7b6, #e96f92, #75517d);
    background: radial-gradient(220% 105% at top center, #75517d 40%, #e96f92 65%, #f7f7b6);
    border-radius: 20px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #fff;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
    flex-shrink: 0;
    animation: fadeIn 1s;
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

.card-background {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 800px;
    width: 450px;
    perspective: 1000px;
}

.card {
    position: relative;
    width: 360px;
    height: 580px;
    margin: 20px;
    border-radius: 20px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #fff;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
    flex-shrink: 0;
}

.card .common .avatar1,
.card .common .avatar2 {
    position: absolute;
    top: 30px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    box-shadow: 0 0 20px rgba(85, 59, 59, 0.8);
    overflow: hidden;
}

.card .love .avatar1,
.card .love .avatar2 {
    position: absolute;
    top: 35px;
    width: 65px;
    height: 65px;
    border-radius: 50%;
    box-shadow: 0 0 10px rgb(255, 112, 112, 0.5);
    overflow: hidden;
}

.avatar1 img,
.avatar2 img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar1::before,
.avatar1::before {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    /* background: linear-gradient(to bottom, transparent 50%, #af7777); */
}

.card .common .avatar1 {
    left: 30px;
}

.card .common .avatar2 {
    left: 80px;
}

.card .avatar {
    position: absolute;
    top: 30px;
    left: 30px;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    box-shadow: 0 0 20px rgba(180, 168, 168, 0.8);
    overflow: hidden;
}

.card .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.card .avatar::before {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, transparent 50%, #222);
}

.card .title {
    position: absolute;
    max-width: 160px;
    top: 20px;
    right: 30px;
    color: #333;
}

.card .title .nickname {
    font-size: 14px;
}

.card .title .reportname {
    font-size: 18px;
    font-weight: bold;
}

.card .times {
    position: absolute;
    top: 124px;
    left: 34px;
    display: block;
    color: #333;

}

.card .times .sentence {
    margin: 8px 0;
}

.card .sum-up {
    position: absolute;
    top: 80px;
    right: 30px;
    height: 245px;
    color: #333;
    font-size: 48px;
    font-family: 黑体;
    font-weight: bold;
    writing-mode: vertical-rl;
}

.card .tags {
    position: absolute;
    width: 100%;
    height: 200px;
    top: 340px;
    display: flex;
}

.card .tags .left,
.card .tags .right {
    width: 50%;
    color: #333;
}

.card .tags .left {
    padding-left: 34px;
}

.card .tags .right img {
    max-width: 50px;
}

.card .tags .right .qrcode {
    position: absolute;
    bottom: 0;
    right: 30px;
    bottom: -5px;
    z-index: 1;
}

.card .tags .right .qrcode img {
    width: 50px;
    height: 50px;
}

.tag-template {
    font-size: 14px;
    /* font-weight: bold; */
    margin: 5px 0px 2px 0px;
    font-family: 黑体;
}

.tag-content {
    font-size: 20px;
    font-weight: bold;

}

.card .copyright {
    position: absolute;
    height: 24px;
    bottom: 10px;
    left: 18px;
}

.card .copyright img {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    overflow: hidden;
    vertical-align: middle
}

.card .copyright span {
    font-size: 12px;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: bold;
    color: #333;
    vertical-align: middle
}

.card .url {
    position: absolute;
    top: 20px;
    right: 30px;
    font-size: 14px;
}

.card .url a {
    text-decoration: none;
    color: #5c5c5c;
    font-size: 10px;
}

.card .bottom {
    position: absolute;
    bottom: 12px;
    left: 165px;
    color: #8f8383;
    font-size: 11px;
    text-align: right;
}

.card .bottom a {
    text-decoration: none;
    color: #8f8383;
}

.upload-button,
.welcome-button,
.QRCode-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 15px 30px;
    border: 0;
    position: absolute;
    overflow: hidden;
    border-radius: 10rem;
    font-weight: bold;
    cursor: pointer;
    color: rgb(37, 37, 37);
    z-index: 1;
    box-shadow: 0 0px 7px -5px rgba(0, 0, 0, 0.5);
    bottom: 5%;
    left: 50%;
}

.upload-button {
    transform: translateX(calc(-100% + 160px));
}

.welcome-button {
    transform: translateX(-160px);
}

.QRCode-button {
    transform: translateX(calc(-100% + 310px));
}

.welcome-button:hover,
.upload-button:hover,
.QRCode-button:hover {
    background: rgb(193, 228, 248);
    color: rgb(33, 0, 85);
}

.hoverEffect {
    position: absolute;
    bottom: 0;
    top: 0;
    left: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1;
}

.hoverEffect div {
    background: rgb(222, 0, 75);
    background: linear-gradient(90deg,
            rgba(222, 0, 75, 1) 0%,
            rgba(191, 70, 255, 1) 49%,
            rgba(0, 212, 255, 1) 100%);
    border-radius: 40rem;
    width: 10rem;
    height: 10rem;
    transition: 0.4s;
    filter: blur(20px);
    animation: effect infinite 3s linear;
    opacity: 0.5;
}

.welcome-button:hover .hoverEffect div {
    width: 8rem;
    height: 8rem;
}

.upload-button:hover .hoverEffect div {
    width: 8rem;
    height: 8rem;
}

.QRCode-button:hover .hoverEffect div {
    width: 8rem;
    height: 8rem;
}

.qr-container {
    position: relative;
    width: 300px;
    height: 400px;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
    border-radius: 18px;
    background: radial-gradient(200% 100% at bottom center, #f7f7b6, #e96f92, #75517d);
    background: radial-gradient(220% 105% at top center, #75517d 40%, #e96f92 65%, #f7f7b6);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    /* align-content: center; */
}

.qr-container .common{
    margin-top: 50px;
    display: flex;
    align-items: center;
}

.qr-container .common .avatar1,
.qr-container .common .avatar2 {
    /* position: absolute;
    top: 34px; */
    width: 50px;
    height: 50px;
    border-radius: 50%;
    box-shadow: 0 0 20px rgba(85, 59, 59, 0.8);
    overflow: hidden;
}

.qr-container .common .qr-title {
    position: absolute;
    left: 150px;
    font-weight: 700;
    margin-left: 10px;
}

.qr-container .common .avatar1 {
    position: absolute;
    left: 50px;
}

.qr-container .common .avatar2 {
    position: absolute;
    left: 90px;
}

.qr-container .url-qr {
    /* position: absolute;
    top: 80px; */
    margin-top: 30px;
    /* margin-left: 50px; */
}
.footer{
    text-align: center;
    color: #8f8383;
    font-size: 11px;
    margin-bottom: 20px;
    /* position: absolute;
    bottom: 10px;
    left: 100px; */
}

@keyframes effect {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

@media screen and (max-width: 1080px) {
    .buttons {
        display: none;
    }
}

@media screen and (max-width: 400px) {
    .card {
        transform: scale(0.8);
    }

    .card .sum-up {
        font-size: 42px;
    }

    @keyframes fadeIn {
        0% {
            opacity: 0;
            transform: scale(0.5);
        }

        100% {
            opacity: 1;
            transform: scale(0.8);
        }
    }
}
</style>