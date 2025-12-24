<template>
	<div class="container">
		<header class="clearfix">
			<h2>四季感悟</h2>
			<div class="support-note">
				<span class="note-ie">对不起，请使用最新浏览器.</span>
			</div>
		</header>
		<section class="main">
			<ul class="timeline">
				<li class="event" v-for="(item, index) in quarterData" :key="index">
					<input type="radio" :id="'radio' + index" name="tl-group" v-model="selected" :value="index" />
					<label></label>
					<div :class="`thumb user-${item.season}`" @click="selectRadio(index)">
						<span>{{ item.season }}</span>
					</div>
					<div class="content-perspective" @click="selectRadio(index)">
						<div class="content">
							<div class="content-inner">
								<h3>{{ item.title }}</h3>
								<p>{{ item.text }}</p>
							</div>
						</div>
					</div>
				</li>
			</ul>
			<div
				style="color:rebeccapurple; padding-left: 115px; font-weight: bold;font-size: 20px; padding-top: 20px;; padding-bottom: 20px;">
				- 未完待续 -</div>
		</section>
	</div><!-- /container -->
</template>

<script setup name="Emotion">
import { ref } from "vue";
import { quarterData } from "../js/getdata.js";
const selected = ref(0);
console.log("quarterData:", quarterData)


function selectRadio(value) {
	selected.value = value;
}

</script>

<style scoped>
/* General Demo Style */
@charset "UTF-8";

*,
*:after,
*:before {
	-webkit-box-sizing: border-box;
	-moz-box-sizing: border-box;
	box-sizing: border-box;
	padding: 0;
	margin: 0;
}

.clearfix:before,
.clearfix:after {
    content: " ";
    display: table;
}

.clearfix:after {
    clear: both;
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
a {
	color: #555;
	text-decoration: none;
}

.container {
	width: 100%;
	position: relative;
	animation: fadeIn 1s;
}

.container > header,
.main {
	width: 100%;
	max-width: 1060px;
	margin: 0 auto;
	padding: 0 30px 0 0;
}

.container > header {
	padding: 10px 10px 0px 10px;
	font-family: 华文中宋;
}

.container > header h1 {
	margin: 0;
	font-weight: 400;
	color: #41838e;
	font-size: 16px; 
	text-shadow: 0 1px 1px rgba(255,255,255,0.4);
}

.container > header h1 span {
	color: white;
}

.container > header h2 {
	padding: 10px 0;
	margin: 0;
	font-size: 32px;
	line-height: 58px;
	color: #fff;
	font-weight: 500;
	position: relative;
	background: transparent url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAI0lEQVQIW2P8DwSMQMCABBhBgiA+sgRYBboEXBuyBIpZMAkAW1YUAh9deX8AAAAASUVORK5CYII=) repeat-x bottom left;
	text-shadow: 4px 4px 0px #41838e;
}

.container > header h2 span {
	display: block;
	font-weight: 700;
	text-transform: uppercase;
	letter-spacing: 10px;
	font-size: 18px;
	color: white;
	text-shadow: none;
}

/* Header Style */
.codrops-top {
	font-size: 11px; 
	line-height: 24px; 
	background: #fff;
	background: rgba(255, 255, 255, 0.8);
	text-transform: uppercase;
	z-index: 9999;
	position: relative;
	box-shadow: 1px 0px 2px rgba(0,0,0,0.2);
}

.codrops-top a {
	padding: 0px 10px;
	letter-spacing: 1px;
	color: #333;
	text-shadow: 0 -1px 0 #fff;
	display: inline-block;
}

.codrops-top a:hover {
	background: rgba(255,255,255,0.8);
	color: #000;
}

.codrops-top span.right {
	float: right;
}

.codrops-top span.right a {
	float: left;
	display: block;
}

.support-note {
	clear: both;
}

.support-note span{
	color: white;
	font-size: 16px;
	display: none;
	font-weight: bold;
	text-align: center;
	padding: 5px 0;
}

@font-face {
	font-family: 'fontawesome-selected';
	src: url("font/fontawesome-selected.eot");
	src: 
	url("font/fontawesome-selected.eot?#iefix") format('embedded-opentype'), 
	url("font/fontawesome-selected.woff") format('woff'), 
	url("font/fontawesome-selected.ttf") format('truetype'), 
	url("font/fontawesome-selected.svg#fontawesome-selected") format('svg');
	font-weight: normal;
	font-style: normal;
}

.timeline {
	position: relative;
	list-style-type: none;
	padding: 30px 0 5px 0;
	font-family: 华文中宋;
}

.timeline:before {
	content: '';
	position: absolute;
	width: 5px;
	height: 100%;
	top: 0;
	left: 135px;
	background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAJUlEQVQIW2NkQAP/gYARWQwkAOLDBeECjEAAkkEWAKtEFwAJAgAZEBP+oM1IkwAAAABJRU5ErkJggg==);
}

.event {
	position: relative;
	margin-bottom: 40px;
	padding-right: 30px;
}

.thumb {
	position: absolute;
	width: 80px;
	height: 80px;
	box-shadow: 
		0 0 0 8px rgba(65,131,142,1), 
		0 1px 1px rgba(255,255,255,0.5);
	background-repeat: no-repeat;
	border-radius: 50%;
	-webkit-transform: scale(0.8) translateX(24px);
	-moz-transform: scale(0.8) translateX(24px);
	-o-transform: scale(0.8) translateX(24px);
	-ms-transform: scale(0.8) translateX(24px);
	transform: scale(0.8) translateX(24px);
	cursor: pointer;
}

.thumb:before {
	content: '';
	position: absolute;
	height: 8px;
	z-index: -1;
	background: transparent url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAICAYAAADA+m62AAAAPElEQVQYV2NkQAP/gYARCNDFUQRgirAphitEl0TngxXisg5ZnBGXIpgbYfIYjkb3BNxGbBLYxIgyEaQRAA8KKAWYsZtjAAAAAElFTkSuQmCC);
	width: 51px;
	top: 42px;
	left: 100%;
	margin-left: 8px;
}

.thumb span {
	color: #41838e; 
	width: 100%;
	text-align: center;
	font-weight: 700;
	font-size: 24px;
	text-transform: uppercase;
	position: absolute;
	bottom: -50px;
}

.user-春 {
	background-image: url(/春.jpg);
    background-size: cover; /* 关键属性：使图片覆盖整个div */
    background-position: center; /* 居中显示图片 */
    background-repeat: no-repeat; /* 防止图片重复 */
}

.user-夏 {
	background-image: url(/夏.svg);
    background-size: contain; /* 关键属性：使图片覆盖整个div */
    background-position: center; /* 居中显示图片 */
    background-repeat: no-repeat; /* 防止图片重复 */
}

.user-秋 {
	background-image: url(/秋.jpg);
    background-size: cover; /* 关键属性：使图片覆盖整个div */
    background-position: center; /* 居中显示图片 */
    background-repeat: no-repeat; /* 防止图片重复 */
}

.user-冬 {
	background-image: url(/冬.svg);
    background-size: cover; /* 关键属性：使图片覆盖整个div */
    background-position: center; /* 居中显示图片 */
    background-repeat: no-repeat; /* 防止图片重复 */
}

/* Transparent Checkbox/radio hack: leave the checkbox on top, hide it with opacity 0 */

.event label,
.event input[type="radio"] {
	width: 24px;
	height: 24px;
	left: 128px;
	top: 36px;
	position: absolute;
	display: block;
	/* opacity: 0; */
}

.event input[type="radio"] {
	opacity: 0;
	z-index: 10;
	cursor: pointer;
}



.event label:after {
	font-family: 'fontawesome-selected';
	content: '\e702';
	background: #fff;
	border-radius: 50%;
	color: #41838E;
	font-size: 26px;
	height: 100%;
	width: 100%;
	left: -2px;
	top: -3px;
	line-height: 24px;
	position: absolute;
	text-align: center;
}

.content-perspective {
	margin-left: 200px;
	position: relative;

	-webkit-perspective: 600px;
	-moz-perspective: 600px;
	-o-perspective: 600px;
	-ms-perspective: 600px;
	perspective: 600px;
}

.content-perspective:before {
	content: '';
	width: 37px;
	left: -51px;
	top: 45px;
	position: absolute;
	height: 1px;
	z-index: -1;
	background: #fff;
}

.content {
	-webkit-transform: rotateY(10deg);
	-moz-transform: rotateY(10deg);
	-o-transform: rotateY(10deg);
	-ms-transform: rotateY(10deg);
	transform: rotateY(10deg);

	-webkit-transform-origin: 0 0;
	-moz-transform-origin: 0 0;
	-o-transform-origin: 0 0;
	-ms-transform-origin: 0 0;
	transform-origin: 0 0;

	-webkit-transform-style: preserve-3d;
	-moz-transform-style: preserve-3d;
	-ms-transform-style: preserve-3d;
	-o-transform-style: preserve-3d;
	transform-style: preserve-3d;
}

.content-inner {
	position: relative;
	padding: 20px;
	color: #333;
	border: none;
	border-left: 5px solid #41838e;
	box-shadow: 0 4px 6px rgba(0,0,0,0.1);
	background: #fff;
}

.content-inner h3 {
	font-size: 26px;
	padding: 5px 0 5px 0;
	color: #41838e;
}

.content-inner p {
	font-size: 18px;
	max-height: 0px;
	overflow: hidden;
	color: transparent;
	color: rgba(0,0,0,0);
	text-align: left;
}

.content-inner:before {
	font-family: 'fontawesome-selected';
	content: '◀';
	font-weight: normal;
	font-size: 54px;
	line-height: 54px;
	position: absolute;
	width: 30px;
	height: 30px;
	color: #41838e;
	left: -28px;
	top: 20px;
	z-index: -1;
}

/* Transitions */

.thumb,
.thumb span,
.content-inner h3 {
	-webkit-transition: all 0.6s ease-in-out 0.2s;
	-moz-transition: all 0.6s ease-in-out 0.2s;
	-o-transition: all 0.6s ease-in-out 0.2s;
	-ms-transition: all 0.6s ease-in-out 0.2s;
	transition: all 0.6s ease-in-out 0.2s;
}

.content-inner {
	-webkit-transition: box-shadow 0.8s linear 0.2s;
	-moz-transition: box-shadow 0.8s linear 0.2s;
	-o-transition: box-shadow 0.8s linear  0.2s;
	-ms-transition: box-shadow 0.8s linear 0.2s;
	transition: box-shadow 0.8s linear 0.2s;
}

.content {
	-webkit-transition: -webkit-transform 0.8s cubic-bezier(.59,1.45,.69,.98) 0.2s;
	-moz-transition: -moz-transform 0.8s cubic-bezier(.59,1.45,.69,.98) 0.2s;
	-o-transition: -o-transform 0.8s cubic-bezier(.59,1.45,.69,.98) 0.2s;
	-ms-transition: -ms-transform 0.8s cubic-bezier(.59,1.45,.69,.98) 0.2s;
	transition: transform 0.8s cubic-bezier(.59,1.45,.69,.98) 0.2s;
}

.content-inner p {
	-webkit-transition: max-height 0.5s linear, color 0.3s linear;
	-moz-transition: max-height 0.5s linear, color 0.3s linear;
	-o-transition: max-height 0.5s linear, color 0.3s linear;
	-ms-transition: max-height 0.5s linear, color 0.3s linear;
	transition: max-height 0.5s linear, color 0.3s linear;
}

/* Checked */

.event input[type="radio"]:checked + label:after {
	content: '\2714';
	color: #F26328;
	box-shadow: 0 0 0 5px rgba(255, 255, 255, 0.8);
}

.event input[type="radio"]:checked ~ .content-perspective:before {
	background: #F26328;
}

.event input[type="radio"]:checked ~ .content-perspective .content-inner h3 {
	color: #F26328;
}

.event input[type="radio"]:checked ~ .content-perspective .content {
	-webkit-transform: rotateY(-5deg);
	-moz-transform: rotateY(-5deg);
	-o-transform: rotateY(-5deg);
	-ms-transform: rotateY(-5deg);
	transform: rotateY(-5deg);
}

.event input[type="radio"]:checked ~ .content-perspective .content-inner {
	border-color: #F26328;
	box-shadow: 10px 0px 10px -6px rgba(0, 0, 0, 0.1);
}

.event input[type="radio"]:checked ~ .content-perspective .content-inner p {
	max-height: 260px; /* Add media queries */
	color: rgba(0,0,0,0.6);
	-webkit-transition-delay: 0s, 0.6s;
	-moz-transition-delay: 0s, 0.6s;
	-o-transition-delay: 0s, 0.6s;
	-ms-transition-delay: 0s, 0.6s;
	transition-delay: 0s, 0.6s;
}

.event input[type="radio"]:checked ~ .content-perspective .content-inner:before {
	color: #F26328;
}

.event input[type="radio"]:checked ~ .thumb {
	-webkit-transform: scale(1);
	-moz-transform: scale(1);
	-o-transform: scale(1);
	-ms-transform: scale(1);
	transform: scale(1);
	box-shadow: 
		0 0 0 8px rgba(242,99,40,1), 
		0 1px 1px rgba(255,255,255,0.5);
}

.event input[type="radio"]:checked ~ .thumb span {
	color: white;
}

.event input[type="radio"]:checked ~ .thumb:before {
	background: transparent url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAICAYAAADA+m62AAAAPUlEQVQYV2NkQAOfUjX+882+wYgujiIAU4RNMVwhuiQ6H6wQl3XI4oy4FMHcCJPHcDS6J2A2EqUQpJhohQBbNyaHFmzEqgAAAABJRU5ErkJggg==);
}

.content-inner p,
.thumb span,
.event label {
	-webkit-backface-visibility: hidden;
}

@media screen and (max-width: 850px) { 
	.content-inner h3 {
		font-size: 20px;
	}

	.content-inner p {
		font-size: 14px;
		text-align: justify;
	}

	.event input[type="radio"]:checked ~ .content-perspective .content-inner p {
		max-height: 500px; 
	}
}

@media screen and (max-width: 540px) {
	.container > header {
		padding: 0px 30px 0px 30px;
		font-family: 华文中宋;
	}
	.timeline::before {
		left: 80px;
	}

	.event { 
		padding-right: 0px;
		margin-bottom: 30px;
	}


	.thumb {
		-webkit-transform: scale(0.5);
		-moz-transform: scale(0.5);
		-o-transform: scale(0.5);
		-ms-transform: scale(0.5);
		transform: scale(0.5);
	}

	.event input[type="radio"] {
		width: 100px;
		height: 100px;
		left: 0px;
		top: 0px;
	}

	.thumb:before,
	.event input[type="radio"]:checked ~ .thumb:before {
		background: none;
		width: 0;
	}

	.event label {
		display: none;
		
	}

	.content-perspective:before {
		
	}
    .content-perspective {
        margin-left: 100px;
        position: relative;

        -webkit-perspective: 600px;
        -moz-perspective: 600px;
        -o-perspective: 600px;
        -ms-perspective: 600px;
        perspective: 600px;
    }

    .content-perspective:before {
        height: 0px; 
        content: '';
        width: 37px; 
        left: -51px;
        top: 45px;
        position: absolute;
        height: 1px;
        z-index: -1;
        background: #fff;
    }

	.content {
		-webkit-transform: rotateX(-10deg);
		-moz-transform: rotateX(-10deg);
		-o-transform: rotateX(-10deg);
		-ms-transform: rotateX(-10deg);
		transform: rotateX(-10deg);
	}

	.event input[type="radio"]:checked ~ .content-perspective .content {
		-webkit-transform: rotateX(10deg);
		-moz-transform: rotateX(10deg);
		-o-transform: rotateX(10deg);
		-ms-transform: rotateX(10deg);
		transform: rotateX(10deg);
	}

	.content-inner {
		border-left: none;
		border-top: 5px solid #41838e;
	}

	.event input[type="radio"]:checked ~ .content-perspective .content-inner {
		border-color: #F26328;
		box-shadow: 0 10px 10px -6px rgba(0, 0, 0, 0.1);
	}

	.content-inner:before {
		font-family: 'fontawesome-selected';
		content: '';
		font-weight: normal;
		font-size: 24px;
		line-height: 24px;

		position: absolute;
		width: 30px;
		height: 30px;
		color: #41838e;
		left: -10px;
		top: 19px;
		z-index: -1;
	}
	.content-inner h3 {
		font-size: 20px;
	}

	.content-inner p {
		font-size: 12px;
		text-align: justify;
	}
	.event input[type="radio"]:checked ~ .content-perspective .content-inner p {
		max-height: 300px; 
	}
    .event input[type="radio"]:checked ~ .thumb {
        -webkit-transform: scale(0.5);
        -moz-transform: scale(0.5);
        -o-transform: scale(0.5);
        -ms-transform: scale(0.5);
        transform: scale(0.5);
        box-shadow: 
            0 0 0 8px rgba(242,99,40,1), 
            0 1px 1px rgba(255,255,255,0.5);
    }
}


@media screen and (max-width: 360px) {
	.event { 
		padding-right: 0px;
		margin-bottom: 10px;
	}
}


</style>