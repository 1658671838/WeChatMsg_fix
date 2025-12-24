<template>
    <div class="annual-friends">
      <h1 class="title">历年年度好友</h1>
      <div class="friend-list">
        <div class="friend-item" v-for="(friend,index) in yearFriendsData.year_data" :key="index">
          <div class="year">{{ friend.year }}</div>
            <div class="avatar-container">
                <div class="circle-breath"></div>
                <img class="avatar" :src="friend.avatar" alt="Avatar" />
            </div>
          <div class="nickname">{{ friend.nickname }}</div>
        </div>
      </div>
      <h2 class="title2">当年那个陪你聊到很晚的人<br><span style="color: brown;">还在吗？</span></h2>
    </div>
  </template>
  

  <script setup>
  import { ref, computed,onMounted,onBeforeUnmount } from 'vue';
  import {yearFriendsData,Welcome_data} from '../js/getdata.js';
  
  </script>
  
  <style scoped>

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
.annual-friends {
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    /* height: 100vh; */
    width: 100vw;
    box-sizing: border-box;
}

.title {
  font-size: 32px;
  margin-top: 10vh;
  margin-bottom: 20px;
  animation: fadeIn 1s;
  max-width: 400px;
  text-align: center;
}
.title2 {
  font-size: 24px;
  margin-bottom: 20px;
  animation: fadeIn 4s;
  text-align: center;
}

.friend-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 400px;
  /* height: 50vh; */
  margin: 0 auto;
  animation: fadeIn 1s;
}

.friend-item {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 10px 0;
  width: 100%;
  max-width: 800px;
  /* background-color: #2a318d; */
  padding: 10px;
  border-radius: 8px;
}

.year {
  font-size: 24px;
  margin-right: 15px;
  color: #ffffff;
}

.avatar-container {
    position: relative;
    width: 50px;
    height: 50px;
    display: inline-block;
    vertical-align: middle
}

.circle-breath {
    background: rgba(255, 192, 203, 0.1);
    box-shadow: 0 0 0 0 rgb(204, 73, 152);
    height: 50px;
    width: 50px;
    border-radius: 50%;
    animation: donghua 1s ease-in-out infinite;
    position: absolute;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.nickname {
    margin-left: 15px;
    text-align: left;
    flex-grow: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #ffffff;
}

@keyframes donghua {
    0% {
        transform: scale(1);
        box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.6);
    }

    100% {
        transform: scale(1);
        box-shadow: 0 0 0 24px rgba(204, 73, 152, 0%);
    }

}
@media screen and (max-width: 390px) {
    .friend-item {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 10px 0;
        width: 100%;
        max-width: 800px;
        /* background-color: #2a318d; */
        padding: 0px;
        border-radius: 8px;
    }
}
  </style>
  