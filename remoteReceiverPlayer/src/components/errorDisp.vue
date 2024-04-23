<script setup>
	defineProps({
		errorCount:{
			type:Number,
			required:true
		}
	})
</script>
<template>
	<view v-for="(item, index) in errors">
		<view class="error"></view>
	</view>
</template>

<script>
export default{
	computed:{
		errors:{
			get(){
				return new Array(this.errorCount)
			}
		}
	}
}
</script>

<style>
.error{
	display: flex;
	position: relative;
	width: 50px;
	height: 50px;
	border-radius: 25px 25px 25px 25px;
	background-color: red;
}
</style>