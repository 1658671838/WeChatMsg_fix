<template>
    <div class="chart-container">
        <div v-for="(chart, index) in chartIds" :key="index" :id="chart" class="chart"></div>
        <div class="desc">
            <div class="sum-up">
                {{ chatdescription0.sumUp }}
            </div>
            <div class="left">
                <div>{{ chatdescription0.left.prefix }} <span class="time-period">{{ chatdescription0.left.timePeriod }}</span></div>
                <div>{{ chatdescription0.left.suffix }}</div>
            </div>
            <div class="right">
                <span v-for="(line, idx) in chatdescription0.right" :key="idx">
                    {{ line }}<br v-if="idx !== chatdescription0.right.length - 1" />
                </span>
            </div>
        </div>
    </div>
</template>

<script setup name="TimePeriod">
import { onMounted, onUnmounted, ref} from 'vue';
import * as echarts from 'echarts';
import {
    xAxisData,
    yAxisData,
    generateData,
    seasonColors,
    chartTitle,
    chatdescription
} from '../js/getdata.js'; 

const chatdescription0 = ref(
	chatdescription
);

const chartIds = ['chart-1']; // Define chart IDs
let chartInstances = []; // Save chart instances



const drawChart = (chartId, index) => {
    const chartDom = document.getElementById(chartId);
    const myChart = echarts.init(chartDom);

    // 获取示例数据
    const data = yAxisData;

    const option = {
        title: {
            text: chartTitle, // 使用从data.js中获取的图表标题
            bottom: '0%',
            left: 'center',
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
                data: data,
                smooth: true,
                lineStyle: {
                    width: 2,
                    color: seasonColors[index % seasonColors.length],
                },
                symbol: 'none',
                symbolSize: 6,
            },
        ],
        grid: {
            left: '10%',
            right: '10%',
            top: `15%`,
            bottom: '10%',
        },
        animation: true,
        animationDuration: 4000,
        animationEasing: 'cubicOut',
    };

    myChart.setOption(option);
    return myChart;
};

const handleResize = () => {
    chartInstances.forEach((chart) => {
        if (chart) chart.resize();
    });
};

onMounted(() => {
    chartInstances = chartIds.map((chartId, index) => drawChart(chartId, index));
    window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
    window.removeEventListener('resize', handleResize);
    chartInstances.forEach((chart) => {
        if (chart) chart.dispose();
    });
});
</script>

<style scoped>
@font-face {
    font-family: "Pacifico-Regular";
    src: url("/font/Pacifico-Regular.ttf") format("truetype");
    font-weight: normal;
    font-style: normal;
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
    margin: 30px 0;
}

.desc {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    margin-top: 20px;
    font-size: 14px;
    color: #333;
    width: 35%;
}

.sum-up {
    font-size: 48px;
    color: white;
    /* font-weight: bold; */
    text-align: left;
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