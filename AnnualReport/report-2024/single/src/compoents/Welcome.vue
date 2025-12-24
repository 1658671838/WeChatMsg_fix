<template>
    <div class="message-container">
        <div class="message">
            <div class="logo">
                <img class="logo-img" :src="Welcome_data.avatarSrc" alt="logo" />
                <div :class="{ name: true, 'text-hidden': true, long: Welcome_data.nickname.length >= 6 }">
                    <span class="bg">{{ Welcome_data.nickname }}</span>
                </div>
            </div>
            <div class="description cards" @click="changeBox">
                <div class="content">
                    <Icon size="24">
                        <QuoteLeft />
                    </Icon>
                    <div class="text">
                        <p v-for="(line, index) in visibleText" :key="index">{{ line }}</p>
                    </div>
                    <!-- <div class="text">
                        <p>{{ descriptionText.hello }}</p>
                        <p>{{ descriptionText.text1 }}</p>
                        <p>{{ descriptionText.text2 }}</p>
                    </div> -->
                    <Icon size="24">
                        <QuoteRight />
                    </Icon>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
import { Icon } from "@vicons/utils";
import { QuoteLeft, QuoteRight } from "@vicons/fa";
import { reactive, ref } from "vue";
import { Welcome_data } from "../js/getdata.js";
import http from '../js/http';

// const siteLogo = ref(Welcome_data.siteLogo);
// const nickname = ref(Welcome_data.nickname);

// console.log('siteLogo', siteLogo.value)
// console.log('nickname', nickname.value)

// const descriptionText = reactive(Welcome_data.descriptionText);
export default {
  name: 'ChildComponent',
  isReady:false,
  data() {
    return {
      Welcome_data,
      visibleText: [], // 用于显示当前已呈现的段落
      allText: [], // 所有段落内容的数组
      currentIndex: 0 // 当前显示的段落索引
    };
  },
  methods: {
    async fetchData() {
    },
    async startTyping() {
      this.visibleText = [];
      this.currentIndex = 0;
      for (let i = 0; i < this.allText.length; i++) {
        await this.typeParagraph(this.allText[i]);
        this.currentIndex++;
      }
      this.isReady = true;
      this.$emit('load-complete');
    },
    typeParagraph(paragraph) {
      return new Promise((resolve) => {
        let typedText = "";
        const chars = paragraph.split("");
        let charIndex = 0;

        const interval = setInterval(() => {
          if (charIndex < chars.length) {
            typedText += chars[charIndex];
            if (!this.visibleText[this.currentIndex]) {
              // 如果当前段落还未初始化，则初始化它
              this.visibleText.push(typedText);
            } else {
              // 更新当前段落内容
              this.visibleText[this.currentIndex] = typedText;
            }
            charIndex++;
          } else {
            clearInterval(interval);
            resolve(); // 当前段落完成后，resolve Promise
          }
        }, 50); // 设置每个字符出现的时间间隔
      });
    },
    changeBox() {
      this.startTyping(); // 点击触发重新开始打字机效果
    }
  },
  mounted() {
    console.log('开始加载');
    // 页面加载时自动调用 fetchData
    this.allText = Object.values(this.Welcome_data.descriptionText);
    this.changeBox();

    console.log('加载完成');
  }
};
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

p{
    margin: 10px 0 10px 0;
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
    max-width: 460px;
}

.message .logo .logo-img {
    border-radius: 50%;
    width: 120px;
}

.message .logo .name {
    width: 100%;
    padding-left: 22px;
    /* transform: translateY(-8px); */
    font-family: "Pacifico-Regular";
}

.message .logo .name .bg {
    font-size: 5rem;
    font-weight: 900;
}




.message .description {
    padding: 1rem;
    /* margin-top: 3.5rem; */
    max-width: 560px;
    animation: fade 0.5s;
}

.message .description .content {
    display: flex;
    justify-content: space-between;
}

.message .description .content .text {
    font-size: 24px;
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
}



.message .description {
    margin-top: 0rem;
}



@media (max-width: 720px) {
    .message .logo {
        max-width: 100%;
    }
}



@media (max-width: 1400px) {
    .message .logo .logo-img {
        border-radius: 50%;
        width: 100px;
    }
    .message .logo .name .bg {
        font-size: 2rem;
        font-weight: 900;
    }
    .message .description .content .text {
        /* background-color: aqua; */
        font-size: 16px;
        margin: 0.75rem 1rem;
        line-height: 2rem;
        margin-right: auto;
    }
    p{
        margin: 0px;
    }
}

@media (max-width: 480px) {
    .message .logo .logo-img {
        border-radius: 50%;
        width: 100px;
    }

    .message .logo .name .bg {
        font-size: 2rem;
        font-weight: 900;
    }

    .message .description .content .text {
        font-size: 16px;
        margin: 0.75rem 1rem;
        line-height: 2rem;
        margin-right: auto;
    }
}

@media (max-width: 360px) {
    .message .logo .logo-img {
        border-radius: 50%;
        width: 100px;
    }
    .message .logo .name .bg {
        font-size: 2rem;
        font-weight: 900;
    }
    .message .description .content .text {
        /* background-color: aqua; */
        font-size: 14px;
        margin: 0.75rem 1rem;
        line-height: 2rem;
        margin-right: auto;
    }
    p{
        margin: 0px;
    }
}
</style>