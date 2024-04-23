<script setup>
	import card from './card.vue';
	defineProps({
	    cards: {
			type: Array,
			required: true,
		},
		areaIndex:{
			type:Number,
			required:true,
		}
	})
</script>
<template>
	<view class="verticalPile">
		<view v-for="(item, index) in cards">
			<card style="margin-bottom:-120px" :playerCard="item" :ownCard="false" :index="index" :playerIndex="notPlayer" :areaIndex="areaIndex" :isOption="false" :isHint="false"></card>
		</view>
	</view>
</template>

<script>
export default{
	data(){
		return{
			notPlayer:-1
		}
	}
}
</script>

<style>
.verticalPile{
	width: 142px;
	height: 300px;
	position: relative;
	display: flex;
	flex-direction: column;
}
</style>