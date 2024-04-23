<script setup>
	import cardPile from './cardPile.vue';
	defineProps({
		cards:{
			type:Array,
			required: true,
		},
		
		areaIndex:{
			type:Number,
			required:true,
		}
	})
</script>

<template>
	<view class="horizontalStack" :style="'background:' + (areaIndex==2?'antiquewhite':'azure') ">
		<view class="pile" v-for="(item, index) in cards">
			<cardPile :cards="item" :areaIndex="areaIndex"></cardPile>
		</view>
		<view class="areaName centering">
			<text>{{areaIndex==2?'Field':'Discard'}}</text>
		</view>
	</view>
</template>

<script>
</script>

<style>
.centering{
	text-align: center;
	align-items: center;
	justify-content: center;
	display: flex;
}

.horizontalStack{
	position: relative;
	height:320px;
	width: 710px;
	display: flex;
	flex-direction: row;
	background-color: azure;
	border-radius: 30px 30px 30px 30px;
	margin-left:30px;
	margin-top:10px;
	margin-bottom: 10px;
}

.areaName{
	position: absolute;
	width: 100%;
	bottom:2px;
}
</style>