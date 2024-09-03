<template>
	<view class="CpuBox">
		<h2 class="BoxTitle">系统信息</h2>
		<view class="UseNuber">
			<el-progress width="230" type="dashboard" :percentage="SystemMsg.cpuUse">
				<template #default="{ percentage }">
					<span class="percentage-value">{{ percentage }}%</span>
					<span class="percentage-label">CPU使用率</span>
				</template>
			</el-progress>
		</view>
	
		<view class="TemNuber">
			<el-progress  width="230" type="dashboard" :percentage="SystemMsg.CpuTem">
				<template #default="{ percentage }">
					<span class="percentage-value">{{ percentage }}℃</span>
					<span class="percentage-label">CPU温度</span>
				</template>
			</el-progress>
		</view>
		
		<view class="MemoryNuber">
			<el-progress width="230" type="dashboard" :percentage="SystemMsg.MemoryUse">
				<template #default="{ percentage }">
					<span class="percentage-value">{{ percentage }}%</span>
					<span class="percentage-label">内存使用率</span>
				</template>
			</el-progress>
		</view>
		
	</view>
	<h2 class="BoxTitle">当前网络</h2>
	<div style="width: 100%;height: 400px" id="NowNetMsg"></div>
	<h2 class="BoxTitle">当前硬盘IO</h2>
	<div style="width: 100%;height: 400px" id="DiskDow"></div>
</template>

<script>
	import axios from 'axios'
	import * as echarts from 'echarts'
	import 'echarts/lib/component/tooltip'
import { ref } from 'vue'
	export default {
		data() {
			return {
				SystemMsg:{
					'CpuTem':0,
					'cpuUse':0,
					'MemoryUse':0,
				},
				echartsMsg:{
					'timeStart':'',
					'timeEnd':'',
					'netType':'kb',
					'diskType':'kb',
					'recvData':[],
					'sentData':[],
					'readData':[],
					'writeData':[],
					titleShow:true
					
				},
				echartsDow:ref(),
				DiskNowDow:ref(),
				'UpSysData':'',
			}
		},
		watch: {
			$route: {
				handler: function(val, oldVal){
					if(val.path != '/SystemManage'){
						clearInterval(this.UpSysData);
					}
				},
			}
		},
		methods: {
			checkUser() {
				var token = this.$cookies.get('Token')
				if (token){
					return token
				}else {
					this.$router.push({
						name: 'Login',
					})
				}
			},
			getSystemMsg() {
				const token = this.checkUser()
				axios({
					url:'/nas/sys/SystemMonitorApi',
					method: 'get',
					headers:{
						'token': token
					}
				}).then((res) => {
					this.SystemMsg.CpuTem = res.data.cpuTem
					this.SystemMsg.cpuUse = res.data.cupPer
					this.SystemMsg.MemoryUse = res.data.memoryInfo
					if (!this.echartsMsg.timeStart) {
						this.echartsMsg.timeStart = res.data.time_start
					}
					this.echartsInit(this.echartsMsg.timeStart, res.data.time_end, res.data.recv, res.data.sent)
					this.DiskechartsInit(this.echartsMsg.timeStart, res.data.time_end, res.data.read, res.data.write, res.data.diskType)
				}).catch((error) =>{
					if(error.response.status == 403) {
						clearInterval(this.UpSysData);
					}
				})
			},
			echartsInit(TimeStart,TimeEnd, recvData,sentData) {
				var nowNetSpeedRecv =  recvData[1]
				var nowNetSpeedSent =  sentData[1]
				var nowNetSpeedRecvUnit = 'kb'
				var nowNetSpeedSentUnit = 'kb'
				if (recvData[1]>=1024){
					nowNetSpeedRecvUnit = 'mb'
					nowNetSpeedRecv = (nowNetSpeedRecv/1024).toFixed(2)
					// recvData[1] = (recvData[1]/1024).toFixed(2)
					// sentData[1] = (sentData[1]/1024).toFixed(2)
				}else if(sentData[1]>=1024) {
					nowNetSpeedSentUnit = 'mb'
					nowNetSpeedSent = (nowNetSpeedSent/1024).toFixed(2)
				}
		

				this.echartsMsg.recvData.push(recvData)
				this.echartsMsg.sentData.push(sentData)
				// var ledata = ['上行速度'+sentData[1], '下行速度'+recvData[1]]
				this.echartsDow.setOption({
					title: {
						show:this.echartsMsg.titleShow,
					    text: "上行: "+ nowNetSpeedSent+ nowNetSpeedSentUnit+  '/s  下行: '+ nowNetSpeedRecv + nowNetSpeedRecvUnit+'/s',
					    left: 'center',
					    // top: 0
						// textStyle:{
						// 	 fontSize:1
						// }
					  },
			        xAxis: {
			            type: 'time',
			            min: TimeStart,
			            max: TimeEnd,
						// data:[1:00,3:00,6:00,9:00,12:00,15:00,18:00,21:00,24:00]
			            
			        },
			        yAxis: {
						name:'bits per second('+this.echartsMsg.netType+'/s)',
						nameLocation:'end',
						nameGap:30,
						type: 'value',
						min:0,
						axisLabel: {
							formatter: function(value) {
								if(value>=1024) {
									return (value/1024).toFixed(2) + 'mb'
								}else{
									return value + 'kb'
								}
							}
						},
						splitLine: {
							show: false
						}
			        },
					legend: {
					  left: 'right',
					  data: ['上行速度', '下行速度'],
						selected: {
						  上行速度: true,
						  下行速度: true,
						}
					  
					},
					tooltip:{
						show:true,
						trigger:'item',
						formatter: function (params) {
							var netTy = 'kb'
							var netSpeed = params.value[1]
							if (netSpeed>=1024){
								netSpeed = (netSpeed/1024).toFixed(2)
								netTy = 'mb'
							}
							return params.seriesName + '</br>'+ params.value[0] + ':    ' + netSpeed + netTy+"/s";
						// return params.value[0] + '</br>'+params.seriesName+':' + params.value[1] + "kb/s";
						},
					},
			        series: [{	//数据
						name: '下行速度',
						type: 'line',
						// step:true, //是否支持骤变，false有段数据为空时为渐变
						// showSymbol: false,
						// hoverAnimation: false,
						data: this.echartsMsg.recvData,
						itemStyle:{
							color:'rgb(0,204,0)',
						},
					},
					{	//数据
						name: '上行速度',
						type: 'line',
						// step:true, //是否支持骤变，false有段数据为空时为渐变
						// showSymbol: false,
						// hoverAnimation: false,
						data: this.echartsMsg.sentData,
						itemStyle:{
							color:'rgb(0, 170, 255)',
						},
					},]
			    })
			},
			DiskechartsInit(TimeStart,TimeEnd, readData,writeData) {
				
				var nowDiskSpeedRead =  readData[1]
				var nowDiskSpeedWrite =  writeData[1]
				var nowDiskSpeedReadUnit = 'kb'
				var nowDiskSpeedWriteUnit = 'kb'
				if (readData[1]>=1024){
					nowDiskSpeedReadUnit = 'mb'
					nowDiskSpeedRead = (nowDiskSpeedRead/1024).toFixed(2)
					// recvData[1] = (recvData[1]/1024).toFixed(2)
					// sentData[1] = (sentData[1]/1024).toFixed(2)
				}else if(writeData[1]>=1024) {
					nowDiskSpeedWriteUnit = 'mb'
					nowDiskSpeedWrite = (nowDiskSpeedWrite/1024).toFixed(2)
				}
				
				this.echartsMsg.readData.push(readData)
				this.echartsMsg.writeData.push(writeData)
				// var ledata = ['上行速度'+sentData[1], '下行速度'+recvData[1]]
				this.DiskNowDow.setOption({
					title: {
						show:this.echartsMsg.titleShow,
						text: "读: "+ nowDiskSpeedRead +nowDiskSpeedReadUnit+'/s  写: '+ nowDiskSpeedWrite + nowDiskSpeedWriteUnit+'/s',
						left: 'center',
						// top: 0
						// textStyle:{
						// 	 fontSize:1
						// }
					  },
					xAxis: {
						type: 'time',
						min: TimeStart,
						max: TimeEnd,
						// data:[1:00,3:00,6:00,9:00,12:00,15:00,18:00,21:00,24:00]
						
					},
					yAxis: {
						type: 'value',
						min:0,
						// boundaryGap: [0, '30%'],//坐标轴两边留白策略
						axisLabel: {
							formatter: function(value) {
								if(value>=1024) {
									return (value/1024).toFixed(2) + 'mb'
								}else{
									return value + 'kb'
								}
							}
						},
						splitLine: {
							show: false
						}
					},
					legend: {
					  left: 'right',
					  data: ['读io', '写io'],
						selected: {
						  读io: true,
						  写io: true,
						}
					  
					},
					tooltip:{
						show:true,
						trigger:'item',
						formatter: function (params) {
							var diskTy = 'kb'
							var diskSpeed = params.value[1]
							if (diskSpeed>=1024){
								diskSpeed = (diskSpeed/1024).toFixed(2)
								diskTy = 'mb'
							}
							// params = params.value[0];
							return params.seriesName + '</br>'+ params.value[0] + ':    ' + diskSpeed + diskTy+"/s";
						// return params.value[0] + '</br>'+params.seriesName+':' + params.value[1] + "kb/s";
						},
					},
					series: [{	//数据
						name: '读io',
						type: 'line',
						// step:true, //是否支持骤变，false有段数据为空时为渐变
						// showSymbol: false,
						// hoverAnimation: false,
						data: this.echartsMsg.readData,
						itemStyle:{
							color:'rgb(0,204,0)',
						},
					},
					{	//数据
						name: '写io',
						type: 'line',
						// step:true, //是否支持骤变，false有段数据为空时为渐变
						// showSymbol: false,
						// hoverAnimation: false,
						data: this.echartsMsg.writeData,
						itemStyle:{
							color:'rgb(0, 170, 255)',
						},
					},]
				})
			}
		
		},
		created() {
			this.UpSysData = setInterval(() =>{
				this.getSystemMsg()
			}, 2500)
		},
		mounted() {
			this.echartsDow = echarts.init(document.getElementById('NowNetMsg'))
			this.DiskNowDow = echarts.init(document.getElementById('DiskDow'))
			if (document.body.clientWidth < 500) {
				this.echartsMsg.titleShow = false
			}
			this.echartsInit(0,0, [],[])
		}
	}
</script>

<style>
	.percentage-value {
	  display: block;
	  margin-top: 10px;
	  font-size: 36px;
	}
	.percentage-label {
	  display: block;
	  margin-top: 10px;
	  font-size: 16px;
	}
</style>
<style scoped src="../../static/css/SystemManageCss.css"></style>