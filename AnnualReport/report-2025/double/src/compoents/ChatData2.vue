<template>
    <div class="chart-container">
        <div id="chart-1" class="chart"></div>
        <div class="desc">
            <div class="sum-up">
                2024年
            </div>
            <div class="left">
                <div><span class="nickname">{{chatData.mynickname}}</span>发送了<span class="time-period">{{
                    chatData.send_msg_num }}</span>条消息</div>
                <div><span class="nickname">{{chatData.hisnickname}}</span>发送了<span class="time-period">{{
                    chatData.receive_msg_num }}</span>条消息</div>
            </div>
            <div class="right">
                <div>谁是话痨呢？</div>
                <!-- <div>{{ chatdescription.quote[1] }}</div> -->
            </div>
        </div>
    </div>
</template>

<script setup name="TimePeriod">
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import { chatdescription,chatData } from '../js/getdata.js';

console.log("chatdescription:", chatdescription.value);

const timePeriodData = ref([]);
const chartIds = ['chart-1'];
const chartInstances = [];

const drawChart = (chartId, index, timePeriodData) => {
    console.log("timePeriodData:", timePeriodData);
    const chartDom = document.getElementById(chartId);
    const myChart = echarts.init(chartDom);
    const indicator = ['文本','图片','视频','表情包','视频','文件'];
    // 将 my_type_count 和 ta_type_count 转换为对象
    const myCountMap = Object.fromEntries(chatData.value.my_type_count);
    const taCountMap = Object.fromEntries(chatData.value.ta_type_count);
    // 创建数值数组
    const myValues = indicator.map(key => myCountMap[key] || 0);
    const taValues = indicator.map(key => taCountMap[key] || 0);
    // 计算每个关键字的最大值
    const result = {};

    indicator.forEach(key => {
        const myCount = myCountMap[key] || 0; // 如果不存在则为 0
        const taCount = taCountMap[key] || 0; // 如果不存在则为 0
        result[key] = Math.floor(Math.max(myCount, taCount)*1.2); // 取最大值
    });
    const screenWidth = window.innerWidth;
    let cellSize;
    if (screenWidth < 768) { // 手机屏幕
        cellSize = 6;
    } else { // 电脑屏幕
        cellSize = 16;
    }
    const option = {
        color: ['#67F9D8', '#FFE434', '#56A3F1', '#FF917C'],
        title: {
            text: '双方发送消息类型',
            show:false,
        },
        legend: {
            data: [chatData.value.mynickname, chatData.value.hisnickname],
            top:'0px',
            left:0,
            textStyle: {
                color: '#ffffff', // 设置文字颜色
                fontSize: 12       // 设置文字大小为
            },
        },
        radar: {
            // shape: 'circle',
            indicator: [
                { text: indicator[0], max: result[indicator[0]] },
                { text: indicator[1], max: result[indicator[1]] },
                { text: indicator[2], max: result[indicator[2]] },
                { text: indicator[3], max: result[indicator[3]] },
                { text: indicator[4], max: result[indicator[4]] },
                { text: indicator[5], max: result[indicator[5]] },
            ],
            axisName: {
                color: '#fff',
                // backgroundColor: '#333',
                borderRadius: 3,
                padding: [3, 5]
            }
        },
        series: [
        {
            type: 'radar',
            radarIndex: 0,
            data: [
                {
                    value: myValues ,
                    name: chatData.value.mynickname,
                    symbol: 'rect',
                    symbolSize: 10,
                    lineStyle: {
                        type: 'dashed'
                    },
                    label: {
                        show: true,
                        textStyle: {
                            color: '#ffffff', // 设置文字颜色为红色
                            fontSize: 8       // 设置文字大小为 14px
                        },
                        formatter: function (params) {
                            return params.value;
                        }
                    }
                },
                {
                    value: taValues,
                    name: chatData.value.hisnickname,
                    label: {
                        show: true,
                        textStyle: {
                            color: '#ffffff', // 设置文字颜色为红色
                            fontSize: 8       // 设置文字大小为 14px
                        },
                        formatter: function (params) {
                            return params.value;
                        }
                    },
                    areaStyle: {
                        color: new echarts.graphic.RadialGradient(0.1, 0.6, 1, [
                        {
                            color: 'rgba(255, 145, 124, 0.1)',
                            offset: 0
                        },
                        {
                            color: 'rgba(255, 145, 124, 0.9)',
                            offset: 1
                        }
                        ])
                    }
                }
            ]
            }
        ]
    };

    myChart.setOption(option);
    return myChart;
};

onMounted(() => {
    const chartInstance = drawChart(chartIds[0], 0, chatdescription.value.data);
    chartInstances.push(chartInstance);
    window.addEventListener('resize', () => {
        chartInstance.resize();
    });
    // timePeriodPromise.then((data) => {
    //     if (data &&  data.timePeriodData) {
    //         console.log(data);
    //         chatdescription.value = data.timePeriodData;

    //         const chartInstance = drawChart(chartIds[0], 0, chatdescription.value.data);
    //         chartInstances.push(chartInstance);
    //         window.addEventListener('resize', () => {
    //             chartInstance.resize();
    //         });
    //     }
    //     else{
    //         const chartInstance = drawChart(chartIds[0], 0, chatdescription.value.data);
    //     }
    // })
    //     .catch((err) => {
    //         console.log(err);
    //     });
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
    font-family: Pacifico-Regular;
    font-size: 24px;
    background: linear-gradient(to right, #fffdd0, #d8efff); /* 渐变背景 */
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
