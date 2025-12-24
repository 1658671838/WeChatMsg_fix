<template>
    <div class="chart-container">
        <div v-for="(chart, index) in chartIds" :key="index" :id="chart" class="chart"></div>
        <div class="desc">
            <div class="sum-up">
                每日聊天痕迹
            </div>
            <div class="left">
                <div>2024年，你们有 <span class="time-period">{{ Calendardata.daysChatted }}</span> 天在聊天</div>
                <div>
                    <span class="time-period">{{ Calendardata.mostActiveYear }}</span>年
                    <span class="time-period">{{ Calendardata.mostActiveMonth }}</span>月，
                    你们聊天最多，
                </div>
                <div>平均每天聊天 <span class="time-period">{{ Calendardata.averageChats }}</span> 次</div>
                <div style="margin-top: 8px;">有你陪伴的日子都很有意义</div>
            </div>
            <div class="right">
                <div>
                    <span class="time-period">{{ Calendardata.peakChatYear }}</span>年
                    <span class="time-period">{{ Calendardata.peakChatMonth }}</span>月
                    <span class="time-period">{{ Calendardata.peakChatDay }}</span>日
                </div>
                <div style="margin-top: 8px;">
                    聊天高达 <span class="time-period">{{ Calendardata.peakChats }}</span> 次
                </div>
                <div style="margin-top: 8px;">
                    {{ poeticMessages[10] }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup name="Calendar">
import { onMounted, onUnmounted, ref } from 'vue';
import * as echarts from 'echarts';
// import { Calendardata, ChatCalendarData } from '../js/getdata.js';
import { Calendardata } from '../js/getdata.js';
console.log("Calendardata:",Calendardata.value)
const poeticMessages = ref({
    1: "这一天，指尖跃动如琴弦，每一句话都弹奏出心灵深处的共鸣",
    2: "这一天，消息如潮涌，彼此的心声在文字间交织成一曲悠扬的和鸣",
    3: "这一天，文字飞舞成诗，屏幕两端仿佛缩短了时空的距离",
    4: "这一天，言语如繁星闪烁，点亮了平凡日子里独特的夜空",
    5: "这一天，聊天框成了时光的画布，书写下不可复制的暖意和陪伴",
    6: "这一天，消息如雨落，滋润了彼此心田中未曾言说的渴望",
    7: "这一天，屏幕闪烁间，连绵的对话汇成了生命中细腻的诗行",
    8: "这一天，字句穿梭如风，将两颗心牵引到更近的距离",
    9: "这一天，每一次的回复都像是一次心灵的击掌，节奏刚好合拍",
    10: "这一天，微信不只是沟通的工具，而是我们情感共鸣的舞台"
});



const chartIds = ['calendar-map'];
let chartInstances = []; // Save chart instances

function generatePieces(max_num, numSegments, colors) {
    const step = (max_num + 100) / numSegments;
    const pieces = [];
    for (let i = 0; i < numSegments; i++) {
        pieces.push({
            gte: i * step,
            lte: (i + 1) * step,
            color: colors[i % colors.length]
        });
    }
    return pieces;
}

function interpolateColors(colors, n) {
    const result = [];

    // Helper function to interpolate between two colors
    const interpolate = (color1, color2, factor) => {
        const c1 = parseInt(color1.slice(1), 16);
        const c2 = parseInt(color2.slice(1), 16);

        const r1 = (c1 >> 16) & 255;
        const g1 = (c1 >> 8) & 255;
        const b1 = c1 & 255;

        const r2 = (c2 >> 16) & 255;
        const g2 = (c2 >> 8) & 255;
        const b2 = c2 & 255;

        const r = Math.round(r1 + (r2 - r1) * factor);
        const g = Math.round(g1 + (g2 - g1) * factor);
        const b = Math.round(b1 + (b2 - b1) * factor);

        return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
    };

    // Distribute the gradient points evenly
    const segments = colors.length - 1;
    const segmentSteps = Math.floor(n / segments);
    const extraSteps = n % segments;

    for (let i = 0; i < segments; i++) {
        const startColor = colors[i];
        const endColor = colors[i + 1];
        const steps = segmentSteps + (i < extraSteps ? 1 : 0); // Distribute extra steps evenly

        for (let j = 0; j < steps; j++) {
            const factor = j / steps;
            result.push(interpolate(startColor, endColor, factor));
        }
    }

    // Ensure the final color is included
    result.push(colors[colors.length - 1]);

    return result;
}

// const colors = ['rgb(8,48,107)', '#82b0cb', '#ffffff', '#e98184', 'rgb(103,0,13)'];
const colors1 = ['#ffffff', '#e98184', '#e04c50', '#bb0000'];
// const colors1 = ['#3680ae', '#82b0cb', '#ffffff', '#e98184', '#e04c50'];
const colors = interpolateColors(colors1, 100);

const drawChart = (chartId, ChatCalendarData, max_day_count, min_day_count) => {
    const chartDom = document.getElementById(chartId);
    const myChart = echarts.init(chartDom);
    const screenWidth = window.innerWidth;
    let cellSize;
    if (screenWidth < 768) { // 手机屏幕
        cellSize = 6;
    } else { // 电脑屏幕
        cellSize = 16;
    }
    const option = {
        title: {
            top: 30,
            left: 'center',
            text: '2024聊天数日历图',
            textStyle: {
                fontSize: 16,
                fontWeight: 'bold',
                align: 'center',
                verticalAlign: 'middle',
                lineHeight: 16,
                color: '#ddd',
            },
        },
        tooltip: {},
        visualMap: {
            min: min_day_count,
            max: max_day_count,
            show: false,
            type: 'piecewise',
            orient: 'horizontal',
            left: 'center',
            textStyle: {
                color: '#ff0000' // 设置字体颜色为红色
            },
            top: 65,
            outOfRange: {
                color: '#000' // 0 或不在范围内的数据颜色
            },
            pieces: generatePieces(max_day_count, 200, interpolateColors(colors1, 100)),
        },
        calendar: {
            top: 120,
            left: 30,
            right: 30,
            cellSize: ['auto', cellSize],
            range: '2024',
            itemStyle: {
                borderWidth: 0.5,
            },
            yearLabel: { show: false },
            dayLabel: {
                show: false
            },
            monthLabel: {
                color: 'white',
            },
        },
        series: {
            type: 'heatmap',
            coordinateSystem: 'calendar',
            data: ChatCalendarData
        }
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
    const [data, max, min] = [Calendardata.value.data, Calendardata.value.max_day_count, Calendardata.value.min_day_count]
    var chartInstance = drawChart(chartIds[0], data, max, min);
    window.addEventListener('resize', () => {
        chartInstance.resize();
    });

})



onUnmounted(() => {
    window.removeEventListener('resize', handleResize);

});
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
    padding: 20px 0 0 0;
    box-sizing: border-box;
    animation: fadeIn 1s;
}

.chart {
    width: 45%;
    height: 250px;
    margin-bottom: -5px;
}

.desc {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    font-size: 14px;
    color: #333;
    width: 40%;
}

.sum-up {
    font-size: 40px;
    /* font-weight: bold; */
    color: white;
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
    margin: 0 5px;
}

.right {
    text-align: right;
    width: 100%;
    font-size: 20px;
    font-family: 'Microsoft YaHei';
    color: #000;
    margin-top: -10px;
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

@media (max-width: 480px) {

    .chart {
        width: 100%;
        padding: 0;
    }

    .desc {
        width: 80%;
    }
}

@media (max-width: 390px) {
    .chart {
        width: 90%;
        height: 200px;
    }

    .desc {
        width: 80%;
    }

    .left {
        text-align: left;
        width: 100%;
        font-size: 16px;
        font-family: 'Microsoft YaHei';
        color: #000;
    }

    .time-period {
        font-family: Pacifico-Regular;
        font-size: 22px;
        color: #fff;
    }

    .right {
        text-align: right;
        width: 100%;
        font-size: 16px;
        font-family: 'Microsoft YaHei';
        color: #000;
        margin-top: 0px;
    }
}
</style>