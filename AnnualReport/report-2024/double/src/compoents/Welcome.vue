<template>
    <div class="message-container">
        <div class="message">
            <div>
                <div class="logo" style="justify-content: flex-start;">
                    <img class="logo-img" :src="myavatar" alt="logo" />
                    <div :class="{ name: true, 'text-hidden': true, long: mynickname.length >= 6 }">
                        <span class="bg">{{ mynickname }}</span>
                    </div>
                </div>
                <div class="logo">
                    <div :class="{ name: true, 'text-hidden': true, long: hisnickname.length >= 6 }">
                        <span class="bg">{{ hisnickname }}</span>
                    </div>
                    <img class="logo-img" :src="hisavatar" alt="logo" />
                </div>
            </div>

            <div class="description cards" @click="changeBox">
                <div class="content">
                    <Icon size="24" class="dynamic-icon">
                        <QuoteLeft />
                    </Icon>
                    <div class="text">
                        <p v-for="(line, index) in visibleText" :key="index">{{ line }}</p>
                    </div>
                    <Icon size="24" class="dynamic-icon">
                        <QuoteRight />
                    </Icon>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import { Icon } from "@vicons/utils";
import { QuoteLeft, QuoteRight } from "@vicons/fa";
import { onMounted, ref, defineEmits } from "vue";
import {
    myavatar,
    hisavatar,
    mynickname,
    hisnickname,
    isReady,
    visibleText,
    currentIndex,
    allText
} from "../js/getdata.js";
// import { Welcome_data } from "../js/getdata.js";

const emit = defineEmits();

const startTyping = async () => {
    visibleText.value = [];
    currentIndex.value = 0;

    for (let i = 0; i < allText.value.length; i++) {
        await typeParagraph(allText.value[i]);
        currentIndex.value++;
    }
    isReady.value = true;
    emit('load-complete');
};
const typeParagraph = (paragraph) => {
    return new Promise((resolve) => {
        let typedText = '';
        const chars = paragraph.split('');
        let charIndex = 0;

        const interval = setInterval(() => {
            if (charIndex < chars.length) {
                typedText += chars[charIndex];
                if (!visibleText.value[currentIndex.value]) {
                    // 如果当前段落还未初始化，则初始化它
                    visibleText.value.push(typedText);
                } else {
                    // 更新当前段落内容
                    visibleText.value[currentIndex.value] = typedText;
                }
                charIndex++;
            } else {
                clearInterval(interval);
                resolve(); // 当前段落完成后，resolve Promise
            }
        }, 50); // 设置每个字符出现的时间间隔
    });
};

const changeBox = () => {
    startTyping(); // 点击触发重新开始打字机效果
};

onMounted(() => {
    console.log('开始加载');
    changeBox();
    console.log('加载完成');
});
</script>

<style scoped>
@font-face {
    font-family: "Pacifico-Regular";
    /* 自定义字体名称 */
    src: url("../../public/font/Pacifico-Regular.ttf") format("truetype");
    /* 字体文件路径 */
    font-weight: normal;
    /* 字体粗细 */
    font-style: normal;
    /* 字体样式 */
}

.message-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
    padding: 16px;
    box-sizing: border-box;
}

.message {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
}

.message .logo {
    display: flex;
    flex-direction: row;
    align-items: center;
    animation: fade 0.5s;
    max-width: 660px;
    overflow: hidden;
}

.message .logo .logo-img {
    border-radius: 50%;
    width: 100px;
}

.message .logo .name {
    width: 100%;
    padding: 0 22px;
    transform: translateY(-8px);
    font-family: "Pacifico-Regular";
    word-break: break-word;
    overflow-wrap: break-word;
    white-space: normal;
    line-height: 1;
}

.message .logo .name .bg {
    font-size: 3.5em;
    font-weight: 900;
}


@media (max-width: 768px) {
    .message .logo {
        display: flex;
        flex-direction: row;
        align-items: center;
        animation: fade 0.5s;
        max-width: 660px;
        overflow: hidden;
    }

    .message .logo .logo-img {
        border-radius: 50%;
        width: 100px;
    }

    .message .logo .name {
        width: 100%;
        padding: 0 22px;
        transform: translateY(-8px);
        font-family: "Pacifico-Regular";
        word-break: break-word;
        overflow-wrap: break-word;
        white-space: normal;
        line-height: 1;
    }

    .message .logo .name .bg {
        font-size: 2.5em;
        font-weight: 900;
    }
}

.message .description {
    padding: 1rem;
    /* margin-top: 3.5rem; */
    max-width: 520px;
    animation: fade 0.5s;
}

.message .description .content {
    display: flex;
    justify-content: space-between;
}

.message .description .content .text {
    font-size: 20px;
    margin: 0.75rem 1rem;
    line-height: 2rem;
    margin-right: auto;
}

.message .description .content .text p:nth-of-type(1) {
    font-family: "Pacifico-Regular";
}

.message .description .content .xicon:nth-of-type(2) {
    align-self: flex-end;
}

@media (max-width: 720px) {
    .message .description {
        max-width: 100%;
        pointer-events: none;
    }

    .message .description .content .text {
        font-size: 16px;
        margin: 0rem 0rem;
        line-height: 1.5rem;
        margin-right: auto;
    }

    .dynamic-icon {
        width: 16px;
        /* 小屏幕时图标大小 */
        height: 16px;
        /* 小屏幕时图标大小 */
    }
}

@media (max-width: 390px) {
    .message .logo .logo-img {
        border-radius: 50%;
        width: 50px;
    }

    .message .logo .name {
        margin-left: 0;
        height: auto;
        transform: none;
        text-align: center;
    }

    .message .logo .name .bg {
        font-size: 1.5rem;
    }

    .message .logo .name .sm {
        font-size: 1.4rem;
    }

    .message .description .content .text {
        font-size: 14px;
        margin: 0rem 0rem;
        line-height: 1.5rem;
        margin-right: auto;
    }

    .dynamic-icon {
        width: 16px;
        /* 小屏幕时图标大小 */
        height: 16px;
        /* 小屏幕时图标大小 */
    }
}
</style>