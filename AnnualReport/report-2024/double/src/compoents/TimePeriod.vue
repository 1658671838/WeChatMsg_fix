<template>
    <div class="chart-container">
        <div id="chart-1" class="chart"></div>
        <div class="desc">
            <div class="sum-up">
                {{ chatdescription.summary }}
            </div>
            <div class="left">
                <div>{{ chatdescription.timedes }} <span class="time-period">{{
                    chatdescription.timePeriod }}</span></div>
                <div>是你们全年最爱的聊天时段</div>
                <div v-if="chatdescription.favoriteChatDate.is_exist === 1">
                    <span class="time-period">{{ chatdescription.favoriteChatDate.year }}</span>年
                    <span class="time-period">{{ chatdescription.favoriteChatDate.month }}</span>月
                    <span class="time-period">{{ chatdescription.favoriteChatDate.day }}</span>日
                </div>
                <div v-else>
                    <br>
                </div>

                <div>{{ chatdescription.remarks[0] }}</div>
                <div>{{ chatdescription.remarks[1] }}</div>
            </div>
            <div class="right">
                <div>{{ chatdescription.quote[0] }}</div>
                <div>{{ chatdescription.quote[1] }}</div>
            </div>
        </div>
    </div>
</template>

<script setup name="TimePeriod">
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import { chatdescription } from '../js/getdata.js';

console.log("chatdescription:", chatdescription.value);

const timePeriodData = ref([]);
const chartIds = ['chart-1'];
const chartInstances = [];

const drawChart = (chartId, index, timePeriodData) => {
    console.log("timePeriodData:", timePeriodData);
    const chartDom = document.getElementById(chartId);
    const myChart = echarts.init(chartDom);

    // Example data
    const xAxisData = ['00', '01, 02', '03', '04', '05', '06', '07', '08, 09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'];
    // Define colors for seasons: Spring, Summer, Autumn, Winter
    const seasonColors = ['#1E90FF']; // Green, Red, Yellow, Blue

    const option = {
        title: {
            text: `2024聊天时段分布图`, // Chart title
            bottom: '0%', // Align title to the bottom
            left: 'center', // Horizontally center the title
            textStyle: {
                fontSize: 14,
                fontWeight: 'bold',
                align: 'center',
                verticalAlign: 'middle',
                lineHeight: 14,
                color: '#ddd',
            },
        },
        xAxis: {
            position: 'top',
            data: xAxisData,
            axisLine: { show: false },
            axisTick: { show: false },
            axisLabel: { show: index === 0 },
            splitLine: { show: false },
        },
        yAxis: {
            show: false,
        },
        series: [
            {
                name: `Series ${index + 1}`,
                type: 'line',
                data: timePeriodData,
                smooth: true,
                lineStyle: {
                    width: 2,
                    color: seasonColors[0], // Apply seasonal colors
                },
                symbol: 'none',
                symbolSize: 6,
            },
        ],
        grid: {
            left: '10%',
            right: '10%',
            top: `15%`, // Create staggered layout with vertical offset
            bottom: '10%',
        },
        animation: true,
        animationDuration: 4000, // Animation duration (in milliseconds)
        animationEasing: 'cubicOut', // Easing effect for the animation
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
    color: #fff;
}

.right {
    text-align: right;
    width: 100%;
    font-size: 20px;
    font-family: 'Microsoft YaHei';
    color: #000;
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
        height: 200px;
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
