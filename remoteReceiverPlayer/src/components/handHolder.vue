<script setup>
	import hand from './hand.vue'
	defineProps({
	    playerHands: {
			type: Array,
			required: true,
		},
	    ownCard: {
			type: Array,
			required: true,
		},
		currentPlayerId:{
			type:Number,
			default:-1,
		}
	})
</script>
<template>
	<view ref="hands" class='hands' :style="'width:'+ calcWidth + 'px'">
		<view v-for="(item, index) in playerHands">
			<hand :playerHand="item" :ownCard="ownCard[index]" :playerIndex="index"></hand>
		</view>
	</view>
</template>

<script>
import PubSub from 'pubsub-js';
export default{
	data(){
		return {
			calcWidth:710,
		}
	},
	mounted() {
		PubSub.subscribe('ready',(_,msg)=>{
			this.calcWidth = this.playerHands[0].length * 142;
			this.$refs.hands.style.width=this.calcWidth+'px';
		})
	}
}
</script>

<style>
.hands{
	display: flex;
	flex-direction: column;
	width: 500px;
	height: 850px;
}
</style>