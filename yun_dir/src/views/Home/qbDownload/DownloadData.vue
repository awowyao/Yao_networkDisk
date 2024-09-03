<template>
	<view class="box">
		<view class="QbDataItems">
			<view class="QbDataItem">
				<view class="QbTitle">
					名称
				</view>
				<view class="QbSize">
					文件大小
				</view>
				<view class="QbProgress">
					下载进度
				</view>
				<view class="QbState">
					状态
				</view>
				<view class="QbSpeed">
					下载速度
				</view>
			</view>
			<view class="QbDataItem" v-for="(item, index) in QbData" :key="index"
				@dblclick="startQbT(item.QbHash, item.state)" @contextmenu.prevent="openRightMenu($event, item.QbHash)"
				@touchstart="QbTouchstart($event, item.QbHash)" @touchmove="QbTouchend($event)"
				@touchend="QbTouchend($event)">
				<view class="QbTitle">
					{{item.name}}
				</view>
				<view class="QbSize">
					{{item.Size}}
				</view>
				<view class="QbProgress">
					<el-progress :percentage="item.Progress" status="success" v-if="item.Progress==100" />
					<el-progress :percentage="item.Progress" v-else />
				</view>
				<view class="QbState">
					{{item.state}}
				</view>
				<view class="QbSpeed">
					{{item.dlspeed}}
				</view>
			</view>
		</view>
	</view>
	<div class="menuDiv" id="menu">
		<ul class="RightMenu">
			<li>打开</li>
			<li @click="deleteQb('删除')">删除</li>
			<li @click="deleteQb('彻底删除')">彻底删除</li>
		</ul>
	</div>
</template>

<script>
	import axios from 'axios'
	import { ElMessage } from 'element-plus'
	export default {
		data() {
			return {
				QbData: [],
				ProgressStatus: '',
				selectQbHash: '',
				timeOutEvent:0,
				UpDownloadData:0,

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
			getQbDownloadData() {
				var token = this.checkUser()
				axios({
					url:'/nas/getQbDownloadData',
					method: 'get',
					headers:{
						'token': token
					},
				}).then((res) => {
					this.QbData = res.data.QbData;
				})
			},
			startQbT(Qb_Hash, state) {
				var token = this.checkUser()
				var mode = 0
				if (state == '暂停' || state == '完成') {
					mode = 1
				} else if (state == '删除') {
					mode = 3
				} else if (state == '彻底删除') {
					mode = 4
				} else {
					mode = 2
				}
				axios({
					data: {
						"QbHash": Qb_Hash,
						"mode": mode,
					},
					url:'/nas/ControlQb',
					method: 'post',
					headers:{
						'token': token
					},
				}).then((res) => {
					ElMessage({
						message: "操作成功",
						type: 'success',
					})
				}).catch(() => {
					ElMessage({
						message: "操作失败",
						type: 'success',
					})
				})
			},
			QbTouchstart(e, QbHash) {
				let _this = this;
				clearTimeout(_this.timeOutEvent);
				_this.timeOutEvent = setTimeout(function() {
					_this.timeOutEvent = 0;
					//  处理长按事件...
					_this.selectQbHash = QbHash
					var curPosX = e.changedTouches[0].clientX
					var curPosY = e.changedTouches[0].clientY
					var obj = document.getElementById("menu");
					obj.style.cssText = "top:" + curPosY + "px;left:" + curPosX + "px; display:flex;";
				}, 650);
			},
			//手如果在600毫秒内就释放，则取消长按事件
			QbTouchend() {
				let _this = this;
				clearTimeout(_this.timeOutEvent);
				if (_this.timeOutEvent !== 0) {
					//  处理单击事件
					
					var obj = document.getElementById("menu");
					obj.style.cssText = "display:none;";
				}
			},
			openRightMenu(e, QbHash) {
				// 获取当前位置x
				this.selectQbHash = QbHash
				var curPosX = e.x
				var curPosY = e.y
				var obj = document.getElementById("menu");
				obj.style.cssText = "top:" + curPosY + "px;left:" + curPosX + "px; display:flex;";
			},
			deleteQb(mode) {
				this.startQbT(this.selectQbHash, mode)
			}
		},
		created() {
			// this.$nextTick(() => {
			// 	setInterval(this.getQbDownloadData, 2500);
			// });
			this.UpDownloadData = setInterval(() =>{               
				this.getQbDownloadData()
			}, 1500)
			
			document.oncontextmenu = function (e) {
			  e.preventDefault();
			};
		},
		watch: {
			$route: {
				handler: function(val, oldVal){
					if(val.path != '/DownloadData'){
						clearInterval(this.UpDownloadData);
					}
				},
			}
		},
	}
</script>

<style scoped src="../../../static/css/DownloadDataCss.css"></style>