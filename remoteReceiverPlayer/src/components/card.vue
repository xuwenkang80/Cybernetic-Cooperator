<script setup>
	defineProps({
	    playerCard: {
			type: Object,
			required: true,
		},
	    ownCard: {
			type: Boolean,
			required: true
		},
		index:Number,
		playerIndex:Number,
		areaIndex:{
			type:Number,
			default:1
		},
		isOption: {
			type: Boolean,
			default: true
		},
		isHint: {
			type: Boolean,
			default: true
		}
	})
</script>
<template>
	<view class="contain centering">
		<transition name="fade">
			<view v-if="isOption && isSelected" class="option centering">
				<view v-if="ownCard" class="optionSelections">
					<view class="circleButton centering" @click="buttonClick('play')"><text>↑</text></view>
					<view class="circleButton centering" @click="buttonClick('discard')"><text>×</text></view>
				</view>
				<view v-else class="optionSelections">
					<view class="circleButton centering" :style="'background-color:' + (playerCard.color=='unknown'?'black':playerCard.color)" @click="buttonClick('color')"></view>
					<view class="circleButton centering" @click="buttonClick('number')"><text>{{playerCard.number}}</text></view>
				</view>
			</view>
		</transition>
		<view :class="'card '+ (isSelected?'cardSelected':'cardUnselected')"  :style="'border:8px solid '+ (playerCard.color=='unknown'?'black':playerCard.color)" v-on:click="onSelect">
			<view v-if="isHint" class="overlay centering">
				<view v-if="playerCard.hintColor!='unknown'" class="hintItem centering"><view class="colorCircle" :style="'background-color:' + (playerCard.hintColor=='unknown'?'black':playerCard.hintColor)"></view></view>
				<view v-if="playerCard.hintNumber!=-1" class="hintItem centering"><text>{{playerCard.hintNumber}}</text></view>
			</view>
			
			<text :style="'color: ' + (playerCard.color=='unknown'?'black':playerCard.color)">{{playerCard.number==-1?'?':playerCard.number}}</text>
		</view>
	</view>
</template>

<script>
	import PubSub from 'pubsub-js';
	export default {
		data(){
			return{
				isSelected:false,
				isTurn:false,
				canHint:true,
				canDiscard:false
			}
		},
		mounted(){
			PubSub.subscribe('cardSelected'+this.areaIndex,(_,data)=>{
				if(this.playerIndex!=data.playerIndex || this.index!=data.index)this.isSelected = false;
			})
			PubSub.subscribe('turn',(_,msg)=>{
				this.isTurn = true
			})
			PubSub.subscribe('hintStatus',(_,msg)=>{
				switch(msg){
					case 0:
						this.canHint = false
						this.canDiscard = true
						break
					case 8:
						this.canDiscard = false
						this.canHint = true
						break
					default:
						this.canDiscard = true
						this.canHint = true
						break
				}
			})
			PubSub.subscribe('onPlayerAction',(_,msg)=>{
				PubSub.publish('cardSelected'+this.areaIndex,{playerIndex:-1,index:-1})
				this.isSelected = false
				this.isTurn =false
			})
		},
		methods:{
			onSelect(){
				if((!this.isOption) || (!this.isTurn))return
				PubSub.publish('cardSelected'+this.areaIndex,{playerIndex:this.playerIndex,index:this.index})
				this.isSelected = !this.isSelected;
			},
			buttonClick(msg){
				if((msg=='color'||msg=="number") && (!this.canHint)){
					alert('没有可用的提示')
					return
				}
				if(msg=='discard' && (!this.canDiscard)){
					alert('提示已满')
					return
				}
				PubSub.publish('cardSelected'+this.areaIndex,{playerIndex:-1,index:-1})
				PubSub.publish('action',{action:msg,index:this.index,playerIndex:this.playerIndex})
				this.isSelected = false
				this.isTurn = false
			}
			
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

.contain{
	position: relative;
	width: 110px;
	height: 150px;
	margin-left:16px;
	margin-right:16px;
	text-align: center;
	align-items: center;
	justify-content: center;
	display: flex;
	flex-direction: column;
	bottom: -16px;
}

.card{
	position: absolute;
	width: 100%;
	height: 100%;
	text-align: center;
	align-items: center;
	justify-content: center;
	display: flex;
	color: black;
	border-radius: 30px 30px 30px 30px;
	transition:all 0.2s;
	background-color: white;
	cursor: pointer;
}

.card text{
	user-select: none;
	font-size: 60px;
}
.cardSelected{
	transform: translateY(-18px);
	box-shadow:0 0 10px gray;
	transition: all 0.2s ease;
}

.card:hover{
	box-shadow:0 0 10px gray;
	transition:all 0.2s ease;
	z-index: 100;
}

.option{
	position: absolute;
	bottom: -10px;
}

.fade-enter-active,
.fade-leave-active{
  transition: all 0.2s ease;
}
.fade-enter-from,
.fade-leave-to{
  opacity: 0;
}

.optionSelections{
	display: flex;
	flex-direction: row;
}

.circleButton{
	width: 40px;
	height: 30px;
	border-radius: 10px 10px 10px 10px;
	background-color: gray;
	margin-left: 10px;
	margin-right: 10px;
	color: white;
	cursor: pointer;
}

.circleButton:hover{
	box-shadow:0 0 10px gray;
	transition:all 0.2s ease;
}

.circleButton:active{
	background-color: silver;
}

.circleButton text{
	user-select: none;
	margin-top:5px;
}

.colorCircle{
	margin-top:5px;
	width: 10px;
	height: 10px;
	border-radius: 5px 5px 5px 5px;
}

.overlay{
	display: flex;
	flex-direction: row;
	position: absolute;
	top:0px;
	width: 100%;
	height: 10%;
}

.hintItem{
	margin-left:10px;
	margin-right:10px;
}

.hintItem text{
	font-size: medium;
	margin-top: 5px;
}
</style>