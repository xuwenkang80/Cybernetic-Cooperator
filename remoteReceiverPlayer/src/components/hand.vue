<script setup>
import card from './card.vue'
defineProps({
	    playerHand: {
			type: Array,
			required: true,
		},
		ownCard:{
			type:Boolean,
			required: true
		},
		playerIndex:{
			type:Number,
			default:1,
		},
	})
</script>
	
<template>
	<view ref="hand" :class="'hand ' + (isTurn?'turn':'unturn') + ' ' +(ownCard?'myHand':'notMyHand')">
		<view v-for="(item, index) in playerHand">
			<card :playerCard="item" :ownCard="ownCard" :index="index" :playerIndex="playerIndex" :areaIndex="handArea"></card>
		</view>
		<view class="playerNameHolder centering">
			<text>Player {{playerIndex + 1}}</text>
		</view>
	</view>
</template>

<script>
	import PubSub from 'pubsub-js';
	export default{
		data(){
			return{
				handArea:1,
				isTurn:false,
			}
		},
		mounted(){
			PubSub.subscribe('ready',(msg)=>{
				console.log('hand receives ready')
				this.$refs.hand.style.width = this.playerHand.length * 142 + 'px';
			})
			PubSub.subscribe('onTurnStart',(_,msg)=>{
				this.isTurn = (msg.index == this.playerIndex)
			})
		},
		methods:{
			
		}
	}
</script>

<style>
.centering{
	text-align: center;
	align-items: center;
	justify-content: center;
	display: flex;
}
	
.hand{
	position: relative;
	display: flex;
	flex-direction: row;
	width: 800px;
	height: 195px;
	margin-top:5px;
	margin-bottom:5px;
	
	border-radius: 30px 30px 30px 30px;
	transition: all 0.4s;
}

.turn{
	border:15px solid silver;
}

.myHand{
	background-color: gold;
}

.notMyHand{
	background-color: aliceblue;
}
.playerNameHolder{
	position: absolute;
	width: 100%;
	bottom:2px;
}
</style>