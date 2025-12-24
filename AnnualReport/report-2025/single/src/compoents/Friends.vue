<template>
    <div class="box-container">
        <div class="box1">
            <h1>看一看</h1>
            <h1>哪些是你的年度聊天好友</h1>
        </div>
        <div class="box2">
            <div v-for="(friend, index) in chatFriends0.chatFriends" :class="index % 2 === 0 ? 'leftbox' : 'rightbox'">
                <div v-if="(index + 1) % 2 === 0" class="tag">
                    <div class="name">{{friend.name}}</div>
                    <div class="content">{{friend.messageCount}}</div>
                    <div class="content">{{friend.wordCount}}</div>
                </div>
                <div class="avatar-container">
                    <div class="circle-breath"></div>
                    <img :src="friend.avatarSrc" alt="lazy">
                </div>
                <div v-if="index % 2 === 0" class="tag">
                    <div class="name">{{friend.name}}</div>
                    <div class="content">{{friend.messageCount}}</div>
                    <div class="content">{{friend.wordCount}}</div>
                </div>
            </div>
        </div> 
    </div>
</template>

<script setup>
import { onMounted,ref, onBeforeUnmount } from 'vue';
import { chatFriendsData } from '../js/getdata.js';
const chatFriends0= ref(
	chatFriendsData
);
</script>

<style scoped>
.box-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
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

.box1 {
    /* height: 18vh; */
    width: 60vw;
    max-width: 800px;
    color: white;
    animation: fadeIn 1s;
}

.title {
    font-size: 24px;
    color: #333;
    font-weight: bold;
}

.box2 {
    height: 70vh;
    width: 60vw;
    max-width: 800px;
    animation: fadeIn 1s;
}

.leftbox,
.rightbox {
    display: flex;
    width: 100%;
}

.leftbox {
    justify-content: flex-start;
}

.rightbox {
    justify-content: flex-end;
}

.tag {
    color: #333;
    font-weight: bold;
    text-align: left;
    margin: 0 20px;
    vertical-align: middle;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
}

.tag .name {
    font-size: 20px;
    color: #fff;
    font-weight: bold;
}

.tag .content {
    font-size: 16px;
    color: #fff;
}

.avatar-container {
    position: relative;
    width: 80px;
    height: 80px;
    display: inline-block;
    vertical-align: middle
}

.circle-breath {
    background: rgba(255, 192, 203, 0.1);
    box-shadow: 0 0 0 0 rgb(204, 73, 152);
    height: 80px;
    width: 80px;
    border-radius: 50%;
    animation: donghua 1s ease-in-out infinite;
    position: absolute;
}

img {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    position: absolute;
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

@media screen and (max-width: 768px) {
    .box1 {
        height: 18vh;
        width: 70vw;
    }
    .box1 h1 {
        padding: 0;
        margin: 0;
    }
    .box2 {
        height: 70vh;
        width: 90vw;
    }
}
</style>