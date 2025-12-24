<template>
    <div class="ripple-container">
        <div class="title">
            <div class="des">
                2024
            </div>
            <div class="des">
                你们说的最多的词是
            </div>
            <br>
            <div class="keywords">
                <div>
                    <span class="keyword">
                        {{ takeyWord.keyWord }}
                    </span>

                    <span class="keyword_num">{{ takeyWord.keyWordCount }}次</span>
                </div>
                <span class="separator">×</span>
                <div>
                    <span class="keyword">
                        {{ mykeyWord.keyWord }}
                    </span>
                    <span class="keyword_num">{{ mykeyWord.keyWordCount }}次</span>
                </div>
            </div>
        </div>
        <div class="message-box">
            <div v-for="(message, index) in keyWordsData.messages" :key="message.id"
                :class="['item', message.side === 'left' ? 'item-left' : 'item-right']">
                <div v-if="message.side === 'left'" class="avatar">
                    <img :src="hisavatar" loading="lazy">
                </div>
                <div
                    :class="message.side === 'left' ? 'content-wrapper content-wrapper-left' : 'content-wrapper content-wrapper-right'">

                    <div class="bubble" :class="message.side === 'left' ? 'bubble-left' : 'bubble-right'">
                        <!-- {{message.content }} -->
                        <span v-if="parts[index].before">{{ parts[index].before }}</span>
                        <span v-if="parts[index].keyword" class="message-keyword">{{ parts[index].keyword }}</span>
                        <span v-if="parts[index].after">{{ parts[index].after }}</span>
                    </div>
                </div>
                <div v-if="message.side === 'right'" class="avatar">
                    <img :src="myavatar" loading="lazy">
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import {  keyWordsData, mykeyWord, takeyWord, myavatar, hisavatar  } from '../js/getdata.js';
console.log("keyWordsData:", keyWordsData)
const parts = computed(() => {
  return keyWordsData.value.messages.map(message => {
    let keyword = '';
    if (message.side === 'left'){
        keyword = takeyWord.value.keyWord;
    } else{
       keyword = mykeyWord.value.keyWord;
    }
    const index = message.content.indexOf(keyword);
    if (index !== -1) {
      return {
        before: message.content.slice(0, index), // 关键字之前的部分
        keyword: keyword, // 关键字
        after: message.content.slice(index + keyword.length) // 关键字之后的部分
      };
    }
    return {
      before: message.content, // 如果没有找到关键字
      keyword: '',
      after: ''
    };
  });
});
</script>

<style scoped>
@font-face {
    font-family: "Pacifico-Regular";
    src: url("../../public/font/Pacifico-Regular.ttf") format("truetype");
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

.ripple-container {
    position: fixed;
    right: 0;
    top: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    animation: fadeIn 1s;
}

.title {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 80vw;
    height: 40vh;
}

.title .des {
    font-size: 24px;
    /* font-weight: bold; */
    font-family: Pacifico-Regular;
    color: white;
}

.keyword {
    font-size: 86px;
    font-family: 黑体;
    font-weight: bold;
    margin-right: 10px;
}

.title .keywords {
    display: flex;
    justify-content: space-between;
    background: linear-gradient(to right, #fffdd0, #d8efff); /* 渐变背景 */
    -webkit-background-clip: text; /* 仅在文字上显示背景 */
    -webkit-text-fill-color: transparent; /* 使文字填充颜色透明 */
}

.message-keyword{
    background: linear-gradient(to right, #fffdd0, #d8efff); /* 渐变背景 */
    -webkit-background-clip: text; /* 仅在文字上显示背景 */
    -webkit-text-fill-color: transparent; /* 使文字填充颜色透明 */
}

.keyword_num {
    font-size: 30px;
    font-weight: bold;
    font-family: Pacifico-Regular;
    display: flex;
    justify-content: center;
    background: linear-gradient(to right, #d8ddff, #feb47b, #ddffc2); /* 渐变背景 */
    -webkit-background-clip: text; /* 仅在文字上显示背景 */
    -webkit-text-fill-color: transparent; /* 使文字填充颜色透明 */
}

.separator {
    font-size: 48px;
    margin: 20px 10px;
    color: #888;
}

@media screen and (max-width: 768px) {
    .keyword {
        font-size: 40px;
    }

    .keyword_num {
        font-size: 18px;
    }

    .separator {
        margin: 0px 10px;
    }

    .message-box {
        width: 80vw;
        height: 60vh;
    }

}


.message-box {
    display: flex;
    align-items: center;
    flex-direction: column;
    width: 40vw;
    height: 60vh;
}


.bubble {
    white-space: pre-wrap;
    padding: 10px 11px;
    border-radius: 5px;
    color: #1f1f1f;
    font-size: 14px;
    max-width: 400px;
    position: relative;
    word-wrap: break-word;
    word-break: normal;
}

.item-left .bubble {
    margin-left: 15px;
    background-color: rgba(255, 255, 255, 0.1);
}

.item-left .bubble:before,
.item-right .bubble:before {
    content: "";
    position: absolute;
    width: 0;
    height: 0;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent
}

.item-left .bubble:before {
    left: -20px;
    border-left: 10px solid transparent;
    border-right: 10px solid #fff;
    opacity: 0.1;
}

.item-right .bubble {
    margin-right: 15px;
    background-color: rgba(169, 250, 115, 0.4);
}

.item-right .bubble:before {
    border-left: 10px solid #a9fa73;
    border-right: 10px solid transparent;
    right: -20px;
    opacity: 0.4;
}

@media screen and (max-width: 768px) {
    .message-box {
        width: 80vw;
        height: 60vh;
    }

    .bubble {
        max-width: 280px;
    }

    .item-right .bubble {
        margin-right: 8px;
    }

    .item-left .bubble {
        margin-left: 8px;
    }

    .item-left .bubble:before {
        content: "";
        position: absolute;
        width: 0;
        height: 0;
        border-left: 8px solid transparent;
        border-top: 8px solid transparent;
        border-right: 8px solid #fff;
        border-bottom: 8px solid transparent;
        left: -16px;
    }

    .item-right .bubble:before {
        content: "";
        position: absolute;
        width: 0;
        height: 0;
        border-left: 8px solid #9eea6a;
        border-top: 8px solid transparent;
        border-right: 8px solid transparent;
        border-bottom: 8px solid transparent;
        right: -16px;
    }
}

.item {
    margin-top: 15px;
    display: flex;
    width: 100%;
}

.item-refer {
    margin-top: 4px;
}

.item.item-right {
    justify-content: flex-end;
}

.item.item-center {
    justify-content: center;
}

.item.item-center span {
    font-size: 12px;
    padding: 2px 4px;
    color: #fff;
    background-color: #dadada;
    border-radius: 3px;
    -moz-user-select: none;
    /*火狐*/
    -webkit-user-select: none;
    /*webkit浏览器*/
    -ms-user-select: none;
    /*IE10*/
    -khtml-user-select: none;
    /*早期浏览器*/
    user-select: none;
}

.content-wrapper {
    display: flex;
    flex-direction: column;
    max-width: 80%;
}

.content-wrapper-left {
    align-items: baseline;
}

.content-wrapper-right {
    align-items: flex-end;
}

.displayname {
    margin-left: 13px;
    margin-left: 13px;
    font-size: 13px;
    margin-bottom: 5px;
    color: darkgray;
}

.chat-image img,
.chat-file img {
    margin-right: 18px;
    margin-left: 18px;
    max-width: 300px;
    /*max-height: auto;*/
}

.avatar img {
    width: 42px;
    height: 42px;
    border-radius: 3px;
    user-select: none;
}
</style>