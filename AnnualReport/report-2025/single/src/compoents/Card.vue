<template>
    <div class="card-container">
        <div class="tool" id="tool">
            <div class="login-wrapper">
                <div class="header">修改资料</div>
                <div class="form-wrapper">
                    <input type="text" class="input-item" name="username" placeholder="修改昵称" id="set-nickname" @input="handleInput">
                    <!-- <input type="password" class="input-item" name="password" placeholder="password"> -->
                    <div data-animation="ripple" class="btn" id="privacy" @click="privacy">隐藏好友</div>
                    <!-- <a data-animation="ripple" id="random">保存图片</a> -->
                    <div data-animation="ripple" class="btn" id="captureButton" @click="download">保存图片</div>
                </div>
                <div class="msg">
                    <a>下载</a>海报图片 
                </div>
            </div>
        </div>
        <div class="card-background" id="capture">
            <div class="card">
                <div class="avatar">
                    <img :src="wechatReportData.avatarSrc" alt="Avatar">
                </div>
                <div class="title">
                    <div class="nickname">@{{ wechatReportData.nickname }}</div>
                    <div class="reportname">{{ wechatReportData.reportName }}</div>
                </div>
                <div class="friend">
                    <div>我的聊天好友榜单</div>
                    <div v-for="friend in wechatReportData.friends" :key="friend.name">
                        <img :src="friend.avatarSrc" alt="">
                        <span class="friend-name">{{ friend.name }}</span>
                    </div>
                </div>
                <div class="sum-up">
                    {{ wechatReportData.summaryText }}
                </div>
                <div class="tags">
                    <div class="left">
                        <div v-for="tag in wechatReportData.leftTags" :key="tag.label">
                            <div class="tag-template">{{ tag.label }}</div>
                            <div>
                                <span class="tag-content">{{ tag.value }}</span>
                                <span class="tag-template">{{ tag.unit }}</span>
                            </div>
                        </div>
                    </div>
                    <div class="right">
                        <div v-for="tag in wechatReportData.rightTags" :key="tag.label">
                            <div class="tag-template">{{ tag.label }}</div>
                            <div v-if="tag.image">
                                <img :src="tag.image" alt="Tag Image">
                            </div>
                            <div v-else>
                                <span class="tag-content">{{ tag.value }}</span>
                            </div>
                        </div>
                        <div class="qrcode">
                            <img src="/url_qrcode.svg" alt="QrCode">
                        </div>
                    </div>
                </div>
                <div class="copyright">
                    <img src="/favicon.ico" alt="">
                    <span>memotrace.cn</span>
                </div>
                <!-- <div class="url">
                    <a :href="wechatReportData.websiteUrl" target="_blank">{{ wechatReportData.websiteUrlText }}</a>
                </div> -->
                <div class="bottom">
                    <div>{{ wechatReportData.bottomText }}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup name="Card">
import {
    wechatReportData
} from "../js/getdata.js";

import domtoimage from 'dom-to-image';
// import html2canvas from 'html2canvas';

function captureImage() {
    console.log('captureImage');
}
const nicknames = ['于晏','彦祖','语嫣','小鱼儿','竹西','淮左','天乐','晏清','江宁','星空漫步者',
    '彩虹游侠','梦想追逐者','雨中漫步者','静谧之音','闪电旅行者','绿野仙踪','晴空万里','心灵之旅','影子游戏者','绚烂星辰',
    '未来之光','流星飞逝','跃动音符','游走的灵魂','独行侠客','无尽探索者','缤纷色彩','落日余晖','跳跃的火花',
    '幻梦之翼','星空漫步者','雨后彩虹','风吹麦浪','流年之歌','静谧之湖','月光倾城','闪电少女','青春之舞','晨曦之光','小幸运','花开富贵','天籁之音','绯红之夜',
    '繁星点点','笑忘书','烟雨迷踪','梦想家园','星河流水','倾城之恋',"星辰", "橙光", "花未眠", "静水深流", "青柠之夏", 
    "月影", "长安客", "风起", "白云间", "雾中行者", 
    "旧梦", "年华似水", "栀子花开", "清风寄语", "碧落黄泉", 
    "时光碎片", "晨光", "北风吹雪", "南巷", "桃源梦里", 
    "小鹿乱撞", "随心所欲", "归途", "沧海一粟", "夜半星辰", 
    "蝶舞天涯", "萤火微光", "白茶清欢", "半城烟沙", "浅浅笑颜", 
    "回眸一笑", "未眠星空", "岁月沉香", "风雪夜归人", "故人依旧", 
    "落花流水", "满天星", "遥望星河", "月上枝头", "浅梦", 
    "初霜", "霓裳", "暖阳", "寒梅傲雪", "夜未央", 
    "静谧时光", "一苇渡江", "微风吹过", "花落倾城", "南风轻语", 
    "画中人", "清欢渡", "琉璃", "萧萧", "千秋月", 
    "微醺时刻", "旧时光", "心若向阳", "纸短情长", "秋水伊人", 
    "青鸟", "月白风清", "余光", "初夏微凉", "枕边风", 
    "星海", "长风", "无名", "镜花水月", "寒江雪", 
    "星火", "岚风", "云端梦境", "初晴", "镜中月", 
    "斜阳", "听风", "雾里看花", "流年", "千帆过尽", 
    "归人", "云卷云舒", "陌上花开", "星尘", "晚风吹", 
    "北冥有鱼", "江月初照", "灯火阑珊", "白驹过隙", "月华流照", 
    "无垠星海", "花间一壶酒", "岁月如梦", "梨花飘雪", "晨曦微光","Dreamer", "星尘", "风中追梦", "Moonlight", "浅笑安然", 
    "Sunrise", "清风逐影", "BlueOcean", "微光拾忆", "Memory Lane", 
    "小星星", "Glorious Dawn", "风铃之声", "Starlight", "迷途漫步者", 
    "Whisper", "夜色流转", "Cherry Blossom", "宁静的心", "Timeless Echo", 
    "南风起", "Silent Steps", "Light Seeker", "迷雾森林", "银河漫游者", 
    "Wanderlust", "流年碎影", "Star Wanderer", "枫叶飘零", "Autumn Breeze", 
    "心之所向", "SkyWalker", "破晓", "Ocean's Heart", "岁月的歌", 
    "Evergreen", "寂静之森", "Cloud Chaser", "鱼的记忆", "Sea Whisper", 
    "梦里花落", "Twilight Glow", "星辰大海", "Echoes of Time", "夜行者", 
    "Velvet Night", "小鹿游弋", "Lost Horizon", "明日梦想家", "Silent Voyage", 
    "风之物语", "Luminous Soul", "归心似箭", "Mystic Moon", "千里追光", 
    "Free Spirit", "暮光之城", "Glittering Stars", "浮生一梦", "Sky Symphony", 
    "月影摇曳", "Ethereal Glow", "孤岛旅人", "Journey of Dreams", "晨曦暖阳", 
    "Soul Whisperer", "星空迷航", "Amber Moon", "悠然见南山", "Horizon Chase", 
    "迷雾之巅", "Crystal River", "清欢入梦", "Light Beyond", "无尽星河", 
    "NorthWind", "时间的沙", "Aurora Dream", "夜雨声烦", "Midnight Wanderer", 
    "风过无痕", "Stellar Flame", "如梦似幻", "Time Traveler", "逐光追影", 
    "Dream Horizon", "千纸鹤", "Silent Moon", "空谷幽兰", "Endless Echo", 
    "归去来兮", "Echoing Winds", "一叶知秋", "Golden Rays", "海风轻语"
    ];
const avatars = [
    'https://blog.lc044.love/static/img/a774ab7a32635db7b4254c8ff7caaa89.Camera_XHS_16984826124131040g2sg30qo1ggopgqe05oce.webp',
    'https://blog.lc044.love/static/img/52181bc0eafe53966ad1302e70b5cce1.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/fe496dc2a2c4ce5d4c3b019ec1ca8469.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/9f36df276cb01ffed6c3fd5ea30647d9.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/23075e9e559161e51f99a46d09140e23.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/2ba6e9df6909246f48ebce9caee80a5d.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/b2443d6aae526c8bf14405ff594f6f9d.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/b0d159f66be0d16ddd3f353a33de2828.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/a0794bdc18cac8e1e8b856241ac1ecba.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/4f55f6afa6835b64e9f324f86ee76587.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/b1c0e5f308ea671d0a822e48c091d374.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/77fb79c818e688f400e4305bde73d9d3.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/03ad57dbbcfc0b34d11060d44c1ac1d1.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/a7576dc81f07ad844724c99165eb808c.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/79a781eeff7ffbba45f82a3a7e6c62e1.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/691691521b35d38f259d18ef5c2574c9.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/cbcf835fa3d0b39d8144194e7ad48abc.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/339e55db324b20393622c62a026903c6.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/d331d8af4a7fd5ba5d331c3ecf54108f.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/c5be69e9a9693a61abe04c1157f05fb5.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/b4f94fd3ea760b6254b7b0a32a58d3be.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/b049a49a84cfbaa7206026d3aca09ee8.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/6064a74d42c62bd1adc85a314837e895.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/f3bc1a9a7880ef54bc2df76ddd274958.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/dad3e96afe71253d2a099b5e6d3a3f8f.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/1370f1b03d6408b5a4a81ad369bf11c9.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/7a6fd8638bde8e1d02a4053755ad10f8.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/3e6d9b653e2dc2fd4894df5da10a62c3.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/9edf244031ba36bcea6e0e03ada7faff.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/e3ac421f69222173981d1db2ea44a6f6.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/4d71b25fa8326f585be164bf186c5b69.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/9895a0e3d0f95529f07e3c5e96b17fe4.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/fafa090d602b50a63ee3adf6407ad6f8.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/dfef8d8d9c1a0123643499b8732305d1.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/a1155588cf1a4da58473702c251bff2a.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/53ccd5d1f7ecfcc9954834ba6b1baf1f.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/2fb4e328c95ee392614a6bd4b32494c9.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/98004dd8ff371aa8c8346ca224b29c32.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/18ce816083c1a45ed958120d4a567046.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/7b0c6acb04c2a151b1ab71904d58ab45.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/4b32e143aeb4ba72db234bad8f081005.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/4752f3b1535523ec747363303dc0d83b.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/0a9cf7fd58abe029a091889047cc5c44.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/2589140b315bfa9b553b5a409500f882.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/a6e6d67400fbb1a28389648600c60e16.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/ad877a5487a9f6b581cd4e2f690d2316.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/928920cbaa783b14c2f970b0d7be1071.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/747c4976cbb92cb5759000fb802285c9.clipboard-2024-12-28.webp',
    'https://blog.lc044.love/static/img/e3afff0c6931364419e18db8ed8a62fe.clipboard-2024-12-28.webp'
];
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function getRandomElementsFromArray(array, n) {
    if (n >= array.length) {
        return shuffleArray(array);
    } else {
        const shuffled = shuffleArray(array.slice());
        return shuffled.slice(0, n);
    }
}
const privacy = () => {
    const virtual_friends = [];
    const nickname_ = getRandomElementsFromArray(nicknames,6);
    const avatar_ = getRandomElementsFromArray(avatars,6);
    for(let i= 0;i<6;i++){
        virtual_friends.push(
            {
                name:nickname_[i],
                avatarSrc:avatar_[i]
            }
        );
    }
	
    wechatReportData.friends = virtual_friends;
};

const download = () => {
    var element = document.getElementById('capture');
    // 设置比例参数，例如2表示两倍分辨率
    var scale = 2;

    // 获取元素的实际尺寸
    var width = element.offsetWidth;
    var height = element.offsetHeight;

    domtoimage.toBlob(element, {
        width: width * scale,
        height: height * scale,
        style: {
            transform: 'scale(' + scale + ')',
            transformOrigin: 'top left',
            width: width + 'px',
            height: height + 'px'
        }
    }).then(function (blob) {
            var link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = '我的年度聊天报告-memotrace.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
        .catch(function (error) {
            console.error('oops, something went wrong!', error);
        });
}
const handleInput = (event) => {
      wechatReportData.nickname = event.target.value;
    };
</script>

<style scoped>
.tool{
    margin-right: 20px;
    height:100vh;
    animation: fadeIn 5s;
}

.login-wrapper {
    background-color: #fff;
    width: 250px;
    height: 500px;
    position: relative;
    border-radius: 15px;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%);
    padding: 0 50px;
    box-shadow: 2px 2px 10px 0 rgba(0, 0, 0, 0.5);
}

.login-wrapper .header {
    font-size: 30px;
    font-weight: bold;
    text-align: center;
    line-height: 200px;
}

.login-wrapper .form-wrapper .input-item{
    display: block;
    width: 100%;
    margin-bottom: 20px;
    border: 0;
    padding: 10px;
    border-bottom: 1px solid rgb(128,125,125);
    font-size: 15px;
    outline: none;
}

.login-wrapper .form-wrapper .input-item::placeholder{
    text-transform: uppercase;
}
.login-wrapper .form-wrapper .btn {
    text-align: center;
    padding: 5px;
    background-image: linear-gradient(to right,#a6c1ee, #fbc2eb);
    color: #fff;
    width: 100%;
    margin-top: 40px;
    font-weight: bold;
    cursor:pointer;
}

.login-wrapper .msg{
    text-align: center;
    line-height: 80px;
}

.login-wrapper .msg a{
    text-decoration-line: none;
    color: #fbc2eb;
}
.loader {
    border: 16px solid #f3f3f3;
    border-top: 16px solid #dd512e;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    animation: spin 2s linear infinite;
    transform: translate(-50%, -50%)
}
/* 定义旋转动画 */
@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}
.card-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    /* background-image: linear-gradient(180deg,#5ee7df,#b490ca); */
    perspective: 1000px;
    /* overflow: hidden; */
}

.card-background {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 800px;
    width: 450px;
    /* background-image: linear-gradient(200deg, #fbc2eb, #a6c1ee); */
    perspective: 1000px;
}

.card {
    position: relative;
    width: 360px;
    height: 580px;
    margin: 20px;
    /* background-image: linear-gradient(200deg, #a6c1ee, #fbc2eb, #fff); */
    background: radial-gradient(200% 100% at bottom center, #f7f7b6, #e96f92, #75517d);
	background: radial-gradient(220% 105% at top center, #75517d 40%, #e96f92 65%, #f7f7b6);
    border-radius: 20px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #fff;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
    flex-shrink: 0;
    animation: fadeIn 1s;
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

.card .avatar {
    position: absolute;
    top: 30px;
    left: 30px;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    overflow: hidden;
}

.card .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.card .avatar::before {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, transparent 50%, #704e78);
}

.card .title {
    position: absolute;
    top: 20px;
    right: 30px;
    color: #333;
}

.card .title .nickname {
    font-size: 12px;
    max-width: 120px;
    flex-grow: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    /* color: #3e3e37; */
}

.card .title .reportname {
    font-size: 20px;
    font-weight: bold;
}

.card .friend {
    position: absolute;
    top: 144px;
    left: 34px;
    display: block;
    color: #333;

}

.friend-name {
    margin-left: 10px;
}

.card .friend>:first-child {
    max-width: 200px;
    font-size: 16px;
    line-height: 20px;
}

.card .friend div {
    font-size: 14px;
    font-weight: bold;
    margin: 5px 0;
}

.card .friend div img {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    vertical-align: middle
}

.card .friend div span {
    vertical-align: middle
}

.card .sum-up {
    position: absolute;
    top: 80px;
    right: 30px;
    height: 245px;
    color: #333;
    font-size: 48px;
    font-family: 黑体;
    font-weight: bold;
    writing-mode: vertical-rl;
}

.card .tags {
    position: absolute;
    width: 100%;
    height: 200px;
    top: 340px;
    display: flex;
}

.card .tags .left,
.card .tags .right {
    width: 50%;
    color: #333;
}

.card .tags .left {
    padding-left: 34px;
}

.card .tags .right img {
    max-width: 50px;
}

.card .tags .right .qrcode {
    position: absolute;
    bottom: 0;
    right: 30px;
    bottom: -5px;
    z-index: 1;
}

.card .tags .right .qrcode img {
    width: 50px;
    height: 50px;
}

.tag-template {
    font-size: 14px;
    /* font-weight: bold; */
    margin: 5px 0px 2px 0px;
    font-family: 黑体;
}

.tag-content {
    font-size: 20px;
    font-weight: bold;

}

.card .copyright {
    position: absolute;
    height: 24px;
    bottom: 10px;
    left: 18px;
}

.card .copyright img {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    overflow: hidden;
    vertical-align: middle
}

.card .copyright span {
    font-size: 13px;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: bold;
    color: #333;
    vertical-align: middle
}

.card .url {
    position: absolute;
    top: 20px;
    right: 30px;
    font-size: 14px;
}

.card .url a {
    text-decoration: none;
    color: #111;
    font-size: 10px;
}

.card .bottom {
    position: absolute;
    bottom: 12px;
    left: 165px;
    color: #8f8383;
    font-size: 11px;
    text-align: right;
}

.card .bottom a {
    text-decoration: none;
    color: #8f8383;
}

@media screen and (max-width: 1080px) {
	.tool{
        display: none;
    }
}

@media screen and (max-width: 400px) {
    .card {
        transform: scale(0.8);
    }
    .card .sum-up{
        font-size: 42px;
    }
    @keyframes fadeIn {
        0% {
            opacity: 0;
            transform: scale(0.5);
        }

        100% {
            opacity: 1;
            transform: scale(0.8);
        }
    }
}
</style>