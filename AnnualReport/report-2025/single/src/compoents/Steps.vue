<template>
    <div class="chart-container">
        <div v-for="(chart, index) in chartIds" :key="index" :id="chart" class="chart"></div>
        <div class="desc">
            <div class="sum-up">
                {{ stepdescription.sumUp }}
            </div>
            <div class="left">
                <div>{{ stepdescription.left.totalStepsPrefix }} <span class="time-period">{{ stepdescription.left.totalSteps }}</span></div>
                <div>{{ stepdescription.left.distancePrefix }} <span class="time-period">{{ stepdescription.left.distance }}</span>{{ stepdescription.left.distanceSuffix }}</div>
                <div>{{ stepdescription.left.earthPrefix }} <span class="time-period">{{ stepdescription.left.earthRounds }}</span>{{ stepdescription.left.earthSuffix }}</div>
            </div>
            <div class="right">
                <div>
                    <span class="time-period">{{ stepdescription.right.year }}</span>年
                    <span class="time-period">{{ stepdescription.right.month }}</span>月
                    <span class="time-period">{{ stepdescription.right.day }}</span>日
                </div>
                <div>
                    {{ stepdescription.right.stepsPrefix }}<span class="time-period">{{ stepdescription.right.steps }}</span>{{ stepdescription.right.stepsSuffix }}
                </div>
                <div>
                    {{ stepdescription.right.message }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, onUnmounted, reactive } from 'vue';
import * as echarts from 'echarts';
import {stepdescription, stepData} from '../js/getdata.js';

const chartIds = ['calendar-map'];
let chartInstances = []; // Save chart instances

function generatePieces(numSegments, colors) {
  const step = (stepdescription.right.steps+100) / numSegments;
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
const colors = interpolateColors(colors1,100);

const drawChart = (chartId, index) => {
    const chartDom = document.getElementById(chartId);
    const myChart = echarts.init(chartDom);
    const screenWidth = window.innerWidth;
    let cellSize;
    if (screenWidth < 768) { // 手机屏幕
        cellSize= 6;
    } else { // 电脑屏幕
        cellSize= 16;
    }
    const option = {
        title: {
            top: 0,
            // bottom:0,
            left: 'center',
            text: '2025运动步数日历图',
            // show:false,
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
            min: 0,
            max: 10000,
            type: 'piecewise',
            orient: 'horizontal',
            left: 'center',
            top: 65,
            show:false,
            pieces: generatePieces(200, interpolateColors(colors1,100)),
        },
        calendar: {
            top: 50,
            left: 30,
            right: 30,
            cellSize:['auto',cellSize],
            range: '2025',
            itemStyle: {
                borderWidth: 0.5,
            },
            yearLabel: { show: false },
            dayLabel: {
                show: false
            },
            monthLabel: {
                color:'white',
            },
        },
        
        series: {
            type: 'heatmap',
            coordinateSystem: 'calendar',
            data: stepData
        }
    };
    myChart.setOption(option);
    return myChart;
};

function getVirtualData(year) {
    const date = +echarts.time.parse(year + '-01-01');
    const end = +echarts.time.parse(+year + 1 + '-01-01');
    const dayTime = 3600 * 24 * 1000;
    const data = [];
    for (let time = date; time < end; time += dayTime) {
        data.push([
            echarts.time.format(time, '{yyyy}-{MM}-{dd}', false),
            Math.floor(Math.random() * 10000)
        ]);
    }
    return data;
}

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
    width: 40%;
}

.sum-up {
    font-size: 48px;
    /* font-weight: bold; */
    text-align: left;
    width: 100%;
    color: white;
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
    margin-top: -50px;
}


@media (max-width: 480px) {

    .chart {
        width: 100%;
        height: 100px;
        padding: 0;
    }

    .desc {
        width: 80%;
    }
}

@media (max-width: 390px) {
    .chart {
        width: 90%;
        /* height: 150px; */
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
        margin-top: -50px;
    }
    .left{
        font-size: 16px;
    }
    .sum-up{
        font-size: 30px;
    }
}
</style>
