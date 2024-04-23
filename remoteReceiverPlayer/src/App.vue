<script setup>
import handHolder from './components/handHolder.vue'
import cardPileHolder from './components/cardPileHolder.vue'
import errorDisp from './components/errorDisp.vue';
import card from './components/card.vue';
</script>

<template>
	<view class="cover centering" v-if="!gameStarted">
		<text>Waiting for players</text>
	</view>
	<view class="cover centering" style="z-index: 200;" v-if="gameEnded">
		<text>Game Ended. Score:{{score}}</text>
	</view>
	<view v-show="ready" class="container">
		<view ref="playerHands" class="playerHands centering" :style="'width:'+calcWidth+'px'">
			<handHolder :playerHands="playerHands" :ownCard="ownCards"></handHolder>
		</view>
		<view class="gameZones">
			<view class="field">
				<cardPileHolder :cards="fieldCards" :areaIndex="fieldArea"></cardPileHolder>
			</view>
			<view class="discard">
				<cardPileHolder :cards="discardCards" :areaIndex="discardArea"></cardPileHolder>
			</view>
			<view class="info">
				<card :playerCard="{color:'unknown',number:deckCount,hintColor:'unknown',hintNumber:-1}" :ownCard="false" :isOption="false" :isHint="false" :areaIndex="deckArea" :index="deckArea"></card>
				<view class="hintDisp centering"><text>{{hints}}</text></view>
				<errorDisp :errorCount="error"></errorDisp>
			</view>
		</view>
	</view>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}

.cover{
	background: #88888888;
	width: 100%;
	height: 100%;
	position: absolute;
}

.cover text{
	font-size: 100px;
}

.info{
	position: relative;
	margin-top:10px;
	width: 710px;
	height: 100px;
	display: flex;
	flex-direction: row;
	padding-left: 20px;
}

.field{
	display: flex;
	flex-direction: column;
}

.container{
	width: 100%;
	height: 100%;
	display: flex;
	flex-direction: row;
}

.centering{
	text-align: center;
	align-items: center;
	justify-content: center;
	display: flex;
}

.playerHands{
	width: 50%;
	height: 100%;
	position: relative;
}

.hintDisp{
	position: relative;
	width: 50px;
	height: 50px;
	border-radius: 25px 25px 25px 25px;
	background-color: royalblue;
}

.hintDisp text{
	font-size: 40px;
	color: white;
}
</style>

<script>
	import PubSub from 'pubsub-js';
	export default{
		data(){
			return{
				calcWidth:500,
				playerHands:[[]],
				ownCards:[false,false,false,false,false],
				number:2,
				fieldArea:2,
				discardArea:3,
				deckArea:4,
				path:"ws://127.0.0.1:9999",
				socket:"",
				colors:["unknown","red","yellow","blue","green","silver"],
				currentPlayerIndex:0,
				thisPlayerIndex:0,
				error:0,
				fieldCards:[[],[],[],[],[]],
				discardCards:[[],[],[],[],[]],
				hints:0,
				ready:false,
				deckCount:50,
				gameStarted:false,
				score:0,
				gameEnded:false
			}
		},
		mounted(){
			this.init()
			PubSub.subscribe('onStart',(_,msg)=>{
				this.hints = 8
				let playerHandColor = msg.handColor
				let playerHandNumber = msg.handNumber
				for(var i = 0;i<playerHandColor.length;++i){
					if(playerHandColor[i][0]==-1){
						this.thisPlayerIndex=i
						this.ownCards[i] = true
						console.log('this is player '+i)
					}
					if(i!=0)
						this.playerHands.push([])
					for(var j = 0;j<playerHandColor[i].length;++j){
						this.playerHands[i].push({color:this.colors[playerHandColor[i][j]+1],number:playerHandNumber[i][j],hintColor:'unknown',hintNumber:-1})
						this.deckCount -= 1
					}
				}
				this.gameStarted = true
				PubSub.publish('ready',{})
				this.ready = true
				console.log('ready')
				this.calcWidth = this.playerHands[0].length * 142
			})
			PubSub.subscribe('onGameEnd',(_,msg)=>{
				console.log('Game ended.Score:'+msg.score)
				this.gameEnded = true
			})
			PubSub.subscribe('onTurnStart',(_,msg)=>{PubSub.publish('playerActive',msg.index)})
			PubSub.subscribe('onHintColor',(_,msg)=>{
				for(var i = 0;i<msg.hintColor.length;++i)
					if(msg.hintColor[i] != -1)
						this.playerHands[this.thisPlayerIndex][i].hintColor = this.colors[msg.hintColor[i]+1]
			})
			PubSub.subscribe('onHintNumber',(_,msg)=>{
				for(var i = 0;i<msg.hintColor.length;++i)
					if(msg.hintNumber[i] != -1)
						this.playerHands[this.thisPlayerIndex][i].hintNumber = msg.hintNumber[i]
			})
			PubSub.subscribe('action',(_,msg)=>{
				console.log('got action:')
				console.log(msg)
				switch(msg.action){
					case 'play':
						this.send({actionType:2,target:msg.index})
						break
					case 'discard':
						this.send({actionType:3,target:msg.index})
						break
					case 'color':
						let m = new Map([['unknown',-1],['red',0],['yellow',1],['blue',2],['green',3],['silver',4]])
						this.send({
							actionType:0,
							target:msg.playerIndex,
							color:m.get(this.playerHands[msg.playerIndex][msg.index].color)
						})
						break
					case 'number':
						this.send({actionType:1,target:msg.playerIndex,number:this.playerHands[msg.playerIndex][msg.index].number})
						break
				}
			})
			PubSub.subscribe('onPlayerAction',(_,msg)=>{
				console.log('playerAction')
				console.log(msg)
				switch(msg.actionType){
					case 0:
						this.hints -= 1
						for(var i = 0;i<this.playerHands[msg.target].length;++i)
							if(this.playerHands[msg.target][i].color == this.colors[msg.color+1])
								this.playerHands[msg.target][i].hintColor = this.colors[msg.color+1]
						break
					case 1:
						this.hints -= 1
						for(var i = 0;i<this.playerHands[msg.target].length;++i)
							if(this.playerHands[msg.target][i].number == msg.number)
								this.playerHands[msg.target][i].hintNumber = msg.number
						break
					case 2:
						if(this.fieldCards[msg.play[0]].length==0 && msg.play[1]==1 || (this.fieldCards[msg.play[0]].length!=0 && this.fieldCards[msg.play[0]][this.fieldCards[msg.play[0]].length-1].number == msg.play[1] - 1)){
							this.score += 1
							this.fieldCards[msg.play[0]].push({
								color:this.colors[msg.play[0]+1],
								number:msg.play[1],
								hintColor:'unknown',
								hintNumber:-1
							})
							if(msg.play[1]==5 && this.hints != 8)
								this.hints += 1
						}else{
							this.error += 1
							this.discardCards[msg.play[0]].push({
								color:this.colors[msg.play[0]+1],
								number:msg.play[1],
								hintColor:'unknown',
								hintNumber:-1
							})
						}
						if(msg.draw[1]==0){
							this.playerHands[msg.index].splice(msg.target,1)
						}
						else{
							this.deckCount -= 1
							this.playerHands[msg.index][msg.target]={
								color:this.colors[msg.draw[0] + 1],
								number:msg.draw[1],
								hintColor:'unknown',
								hintNumber:-1
							}
						}
						break
					case 3:
						this.hints += 1
						this.discardCards[msg.discard[0]].push({
							color:this.colors[msg.discard[0] + 1],
							number:msg.discard[1],
							hintColor:'unknown',
							hintNumber:-1
						})
						if(msg.draw[1]==0)
							this.playerHands[msg.index].splice(msg.target,1)
						else{
							this.deckCount -= 1
							this.playerHands[msg.index][msg.target]={
								color:this.colors[msg.draw[0] + 1],
								number:msg.draw[1],
								hintColor:'unknown',
								hintNumber:-1
							}
						}
						break
				}
				PubSub.publish('hintStatus',this.hints)
			})
		},
		methods: {
		        init: function () {
		            if(typeof(WebSocket) === "undefined"){
		                alert("您的浏览器不支持socket")
		            }else{
		                // 实例化socket
		                this.socket = new WebSocket(this.path)
		                // 监听socket连接
		                this.socket.onopen = this.open
		                // 监听socket错误信息
		                this.socket.onerror = this.error
		                // 监听socket消息
		                this.socket.onmessage = this.getMessage
		            }
		        },
		        open: function () {
		            console.log("socket连接成功")
		        },
		        error: function () {
		            console.log("连接错误")
		        },
		        getMessage: function (msg) {
		            console.log(msg)
					const reader = new FileReader();
					reader.readAsText(msg.data, "UTF-8");
					reader.onload = (e) => {
					//字符串和json格式
					let message = JSON.parse(reader.result);
					//result = JSON.stringify(reader.result);
					console.log('websocked收到', message);
					PubSub.publish(message.event,message)
					}
		        },
		        // 发送消息给被连接的服务端
		        send: function (params) {
					let txt = new TextEncoder()
		            this.socket.send(txt.encode(JSON.stringify(params)))
					console.log('sent:'+params)
		        },
		        close: function () {
		            console.log("socket已经关闭")
		        }
		    },
		    destroyed () {
		        // 销毁监听
		        this.socket.onclose = this.close
		    }
	}
</script>
