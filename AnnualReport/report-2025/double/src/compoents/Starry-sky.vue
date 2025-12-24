<template>
	<div class="cosmic-background">
		<div class="celestial-bodies">
			<div v-for="starIndex in totalStars" :key="starIndex" class="celestial-star" ref="celestialStar"></div>
		</div>
		
	</div>
	<a href="https://github.com/LC044/AnnualReport" target="_blank" class="github">
		<img src="/icon/github-dark.svg" alt="Logo" />
	</a>
</template>

<script setup name="CosmicSky">
import { ref, onMounted } from 'vue';

const props = defineProps({
	totalStars: {
		type: Number,
		default: () => 800,
	},
	viewDistance: {
		type: Number,
		default: () => 800,
	},
});

// Celestial star references
const celestialStar = ref();

onMounted(() => {
	const starsArray = celestialStar.value;
	starsArray.forEach((star) => {
		const movementSpeed = 0.12 + Math.random() * 1;
		const randomDistance = props.viewDistance + Math.random() * 300;
		star.style.transformOrigin = `0 0 ${randomDistance}px`;
		star.style.transform = `translate3d(0,0,-${randomDistance}px) rotateY(${Math.random() * 360}deg) rotateX(${Math.random() * -45}deg) scale(${movementSpeed},${movementSpeed})`;
	});
});
</script>

<style scoped>
.cosmic-background {
	width: 100%;
	height: 100vh;
	position: fixed;
	top: 0;
	left: 0;
	z-index: -100;
	background: radial-gradient(200% 100% at bottom center, #f7f7b6, #e96f92, #75517d, #1b2947);
	background: radial-gradient(220% 105% at top center, #1b2947 10%, #75517d 40%, #e96f92 65%, #f7f7b6);
	background-attachment: fixed;
}

@keyframes cosmicRotate {
	0% {
		transform: perspective(400px) rotateZ(20deg) rotateX(-40deg) rotateY(0);
	}
	100% {
		transform: perspective(400px) rotateZ(20deg) rotateX(-40deg) rotateY(-360deg);
	}
}

.celestial-bodies {
	transform: perspective(500px);
	transform-style: preserve-3d;
	position: fixed;
	perspective-origin: 50% 100%;
	left: 50%;
	animation: cosmicRotate 66s infinite linear;
	bottom: 0;
	z-index: -99;
}

.celestial-star {
	width: 2px;
	height: 2px;
	background: #f7f7b8;
	position: fixed;
	top: 0px;
	left: 0;
	backface-visibility: hidden;
}

.github {
	position: fixed;
	bottom: 20px;
	right: 20px;
	z-index: 100;
	opacity: 1;
}

.github img {
	width: 18px; /* 调整 logo 大小 */
	height: auto;
}
</style>
