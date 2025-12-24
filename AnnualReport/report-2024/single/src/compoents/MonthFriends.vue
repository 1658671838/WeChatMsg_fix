<template>
  <div class="container">
    <div class="title">根据12个月的聊天习惯</div>
    <div class="year">2024年月度好友</div>
    <div class="circle-container">
      <div class="icon-container">
        <img :src="welcome_data.avatarSrc" alt="icon" class="icon">
      </div>
      <div
        v-for="(item, index) in months.month_data"
        :key="index"
        class="user"
        :style="getStyle(index, item.num)"
        @mouseover="hoverIndex = index"
        @mouseleave="hoverIndex = null"
      >
        <span>{{ item.month }}</span>
        <img
          class="avatar"
          :style="{ width: getWidth(item.num) + 'px', height: getWidth(item.num) + 'px' }"
          :src="item.avatar"
        />
        <span>{{ item.nickname }}</span>
        <span v-if="hoverIndex === index" class="num-display">{{ item.num }}</span>
      </div>
    </div>
    <div class="footer">无论什么时候<br>都有人陪你聊天</div>
  </div>
</template>

<script setup>
import { ref, computed,onMounted,onBeforeUnmount } from 'vue';
import {monthFriendsData,Welcome_data} from '../js/getdata.js';

const angles = [300, 330, 0, 30, 60, 90, 120, 150, 180, 210, 240, 270];
const months = ref(monthFriendsData);
const welcome_data = ref(Welcome_data);
const hoverIndex = ref(null);

const radius = ref(170);
const minWidth = ref(35);
const maxWidth = ref(55);

const updateDimensions = () => {
  const screenWidth = window.innerWidth;
  console.log(screenWidth);
  if(screenWidth>1920){
    radius.value = 250;
    minWidth.value = 50;
    maxWidth.value = 90;
  } else if(screenWidth<720){
    radius.value = 150;
    minWidth.value = 25;
    maxWidth.value = 55;
  }else{
    radius.value = 170;
    minWidth.value = 25;
    maxWidth.value = 45;
  }
};

onMounted(() => {
  updateDimensions(); // 初始化时设置尺寸
  window.addEventListener('resize', updateDimensions); // 监听窗口大小变化
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateDimensions); // 清理事件监听器
});



const getWidth = (num) => {
  const minNum = computed(() => Math.min(...months.value.month_data.map(month => month.num)));
  const maxNum = computed(() => Math.max(...months.value.month_data.map(month => month.num)));
  // const minNum = 0;
  // const maxNum = 1000;
  let width = minWidth.value + ((num - minNum.value) * (maxWidth.value - minWidth.value)) / (maxNum.value - minNum.value);
  return Math.max(minWidth.value, Math.min(maxWidth.value, width));
};

const getStyle = (index, num) => {
  const angle = angles[index];
  const x = radius.value * Math.cos((angle - 0) / 360 * (2 * Math.PI)) - 55; // 计算x坐标
  const y = radius.value * Math.sin((angle - 0) / 360 * (2 * Math.PI)) - 20; // 计算y坐标
  return {
    transform: `rotate(${angle}deg) translate(${radius}px) rotate(-${angle}deg)`,
    left: `calc(50% + ${x}px)`,
    top: `calc(50% + ${y}px)`,
  };
};
</script>

<style scoped>
.container{
    margin: 0;
    padding: 0;
    display: flex;
    /* justify-content: center; */
    align-items: center;
    flex-direction: column;
    height: 100vh;
    width: 100vw;
    box-sizing: border-box;
    
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
.title {
  margin-top: 40px;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  color: #ffffffcb;
}
.year {
  font-size: 34px;
  font-weight: bold;
  margin: 20px 0;
  color: #ffffffe0;
  animation: fadeIn 1s;
}
.status-circle {
  /* position: relative; */
  width: 600px;
  height: 600px;
  border-radius: 50%;
  margin: 20px auto;
  /* border: 2px solid #333; */
}
.status {
  position: absolute;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100px;
  height: 30px;
  transform-origin: 150px 150px; /* 圆的中心点 */
  font-size: 12px;
  font-weight: bold;
}
.relax {
  background-color: #d8c9f7;
  color: #fff;
  border-radius: 15px;
  padding: 5px;
}
.passion {
  background-color: #00c57b;
  color: #fff;
  border-radius: 15px;
  padding: 5px;
}
.happy {
  background-color: #ff4b7d;
  color: #fff;
  border-radius: 15px;
  padding: 5px;
}
.icon-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  /* animation: fadeIn 1s; */
}
.icon {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
.footer {
  position: absolute;
  bottom: 15%;
  margin-top: 20px;
  font-size: 20px;
  text-align: right;
  font-weight: bold;
  width: 800px;
  /* width: 100%; */
}
.user{
    position: absolute;
    justify-content: center;
    align-items: center;
    text-align: center;
    display: flex;
    flex-direction: column;
    max-width: 100px;
    width: 100px;
    /* height: 30px; */
    transform-origin: 150px 150px; /* 圆的中心点 */
    animation: fadeIn 1s;
}
.num-display {
  position: absolute; /* Position the number absolutely */
  top: 100%; /* Position below the user element */
  left: 50%; /* Center horizontally */
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7); /* Background for visibility */
  color: white; /* Text color */
  padding: 5px; /* Padding around the number */
  border-radius: 5px; /* Rounded corners */
  display: none; /* Initially hidden */
}

.user:hover .num-display {
  display: block; /* Show on hover */
}
.avatar{
    border-radius: 50%;
    width: 40px;
    height: 40px;
}
.user span{
    font-size: 14px;
    color: #fff;
    max-width: 100px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

@media screen and (max-width: 540px) {
  .icon-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100px;
    height: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
    .user span{
      font-size: 12px;
      color: #fff;
      max-width: 80px;
  }
}
@media screen and (min-width: 2560px) {
  .title {
    margin-top: 40px;
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #ffffffcb;
  }
  .year {
    font-size: 34px;
    font-weight: bold;
    margin: 10px 0;
    color: #ffffffe0;
  }
  .footer {
    position: absolute;
    bottom: 10%;
    margin-top: 20px;
    font-size: 20px;
    text-align: center;
    font-weight: bold;
  }
  .icon-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 180px;
    height: 180px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
    .user span{
      font-size: 12px;
      color: #fff;
      max-width: 80px;
  }

}

@media screen and (max-width: 1440px) {
    .title {
    margin-top: 50px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    color: #ffffffcb;
  }
  .year {
    font-size: 34px;
    font-weight: bold;
    margin: 10px 0;
    color: #ffffffe0;
  }
  .footer {
    position: absolute;
    bottom: 15%;
    /* margin-top: 20px; */
    font-size: 20px;
    text-align: center;
    font-weight: bold;
  }
  .icon-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100px;
    height: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
    .user span{
      font-size: 12px;
      color: #fff;
      max-width: 80px;
  }
}
@media screen and (max-width: 390px) {
    .title {
    margin-top: 40px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    color: #ffffffcb;
  }
  .year {
    font-size: 34px;
    font-weight: bold;
    margin: 10px 0;
    color: #ffffffe0;
  }
  .footer {
    position: absolute;
    bottom: 10%;
    /* margin-top: 20px; */
    font-size: 20px;
    text-align: center;
    font-weight: bold;
  }
}
</style>