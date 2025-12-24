<template>
    <div class="chart-container">
        <div class="title">
            <div class="des">
                <span class="nickname">“{{chatData.hisnickname}}”</span>在你电脑中的分量
            </div>
            <div class="des">
                大概有这么重
            </div>
            <div class="keyword">
                {{chatData.total_message_size}}MB
            </div>
        </div>
        <div class="desc">
            <div class="sum-up">
                2024年
            </div>
            <div class="left">
                <div>你们一共产生了<br><span class="time-period">{{chatData.total_message_size}}MB</span>
                    的聊天数据</div>
                <div>相当于<span class="time-period">{{ messageSizeData.imageNum }}</span>张图片</div>
                <div>或<span class="time-period">{{ messageSizeData.musicNum }}</span>首音乐</div>
                <div>或<span class="time-period">{{ messageSizeData.videoNum }}</span>部高清视频</div>
            </div>
            <div class="right">
                <div>内存杀手？</div>
                <div>不删是我对你最大的尊敬</div>
            </div>
        </div>
    </div>
</template>

<script setup name="TimePeriod">
import { ref, onMounted,computed } from 'vue';
import * as echarts from 'echarts';
import { chatdescription,chatData } from '../js/getdata.js';


const messageSizeData = computed(() => ({
    imageNum: chatData.value.total_message_size / 5,
    videoNum: chatData.value.total_message_size / 250,
    musicNum: chatData.value.total_message_size / 4,
}));


onMounted(() => {
})



</script>

<style scoped>
@font-face {
    font-family: "Pacifico-Regular";
    src: url("../../public/font/Pacifico-Regular.ttf") format("truetype");
    font-weight: normal;
    font-style: normal;
}

.chart-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    height: 100vh;
    width: 100vw;
    padding: 60px 0 0 0;
    box-sizing: border-box;
    animation: fadeIn 1s;
}

.chart {
    width: 45%;
    height: 250px;
    margin: 18px 0;
}
.title {
    color: white;
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 300px;
    /* height: 40vh; */
}


.title .keyword {
    font-size: 86px;
    font-family: 黑体;
    font-weight: bold;
    background: linear-gradient(to right, #d8ddff, #feb47b, #ddffc2); /* 渐变背景 */
    -webkit-background-clip: text; /* 仅在文字上显示背景 */
    -webkit-text-fill-color: transparent; /* 使文字填充颜色透明 */

}

.title .footer {
    width: 300px;
}

.keyword_num {
    font-size: 30px;
    font-weight: bold;
    font-family: Pacifico-Regular;
    display: flex;
    justify-content: flex-start;
    background: linear-gradient(to right, #fffdd0, #d8efff); /* 渐变背景 */
    -webkit-background-clip: text; /* 仅在文字上显示背景 */
    -webkit-text-fill-color: transparent; /* 使文字填充颜色透明 */
}
.desc {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    font-size: 14px;
    color: #333;
    width: 35%;
}
.nickname{
    background: linear-gradient(to right, #fffdd0, #d8efff); /* 渐变背景 */
    -webkit-background-clip: text; /* 仅在文字上显示背景 */
    -webkit-text-fill-color: transparent; /* 使文字填充颜色透明 */
}
.sum-up {
    font-size: 40px;
    /* font-weight: bold; */
    text-align: left;
    color: white;
    width: 100%;
}

.left {
    text-align: left;
    width: 100%;
    font-size: 20px;
    font-family: 'Microsoft YaHei';
    color: #000;
}

.time-period {
    font-size: 24px;
    background: linear-gradient(to right, #d8ddff, #feb47b, #ddffc2); /* 渐变背景 */
    -webkit-background-clip: text; /* 仅在文字上显示背景 */
    -webkit-text-fill-color: transparent; /* 使文字填充颜色透明 */
}

.right {
    text-align: right;
    width: 100%;
    font-size: 20px;
    font-family: 'Microsoft YaHei';
    color: #000;
    animation: fadeIn 5s;
}

@media screen and (max-width: 768px) {
    .chart {
        width: 90%;
    }

    .desc {
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
@media screen and (max-width: 768px) {
    .chart {
        width: 90%;
        height: 250px;
        margin: 30px 0;
    }

   .desc {
        width: 80%;
        height: 10vh;
    }
    .left{
        font-size: 16px;
    }
    .sum-up{
        font-size: 30px;
    }
}
</style>
