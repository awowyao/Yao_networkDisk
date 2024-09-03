<template>
	<view class="box" id='QbDownLoadBox'>
		<view class="torrentInput">
		  <el-input
			v-model="torrent"
			:autosize="{ minRows: 8, maxRows: 10 }"
			type="textarea"
			placeholder="输入种子链接"
			
		  />
		</view>
		<view>
			<el-tree :props="props" :load="loadNode" node-key="id" @node-expand="handleBucketClick" @node-collapse="handleBucketClick"  @node-click="handleBucketClick" lazy />
		</view>
		<el-button type="success" @click="AddQb">开始下载</el-button>
	</view>
	<el-dialog v-model="QbStartDownloadVisible" title="Warning" :width="dialogWidth" >
		<span>{{dialogMsg}}</span>
		<template #footer>
			<span class="dialog-footer">
				<el-button @click="QbStartDownloadVisible = false">取消</el-button>
				<el-button type="primary" @click="SetQb">
					确定
				</el-button>
			</span>
		</template>
	</el-dialog>
</template>

<script>
	import axios from 'axios'
	import { ElLoading, ElMessage } from 'element-plus'
	export default {
		data() {
			return {
				torrent:'',
				defaultProps:'',
				nodedata: {},
				QbStartDownloadVisible:false,
				dialogMsg:'',
				dialogWidth:'30%',
				node: {}, // tree 节点对象
				props: {
					label: 'name',
					children: 'zones',
					isLeaf: 'leaf',
				},
				qbPath:'',
			}
		},
		mounted() {
			if (document.body.clientWidth < 500) {
				this.dialogWidth = '80%'
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
			handleBucketClick: function (data, node) {
				this.qbPath = data.path + data.name
			},
			loadNode(node, resolve) {

				var token = this.checkUser()
				// console.log(node, resolve)
				// console.log(node.level)
				if (node.level === 0) {
					axios({
						url:'/nas/GetDisk?',
						params: {
							route: '/'
						},
						method: 'get',
						headers:{
							'token': token
						},
					}).then((res) => {
						return resolve(res.data.data)
					})
					
				}else {
					axios({
						url:'/nas/GetDisk?',
						method: 'get',
						headers:{
							'token': token
						},
						params: {
							route: node.data.path + node.data.name + '/'
						}
					}).then((res) => {
						return resolve(res.data.data)
					})
				}
			},
			AddQb() {
				if (this.torrent){
					this.dialogMsg = '是否要添加到'+this.qbPath
					this.QbStartDownloadVisible = true
				}else {
					ElMessage({
						message: "链接不能为空",
						type: 'warning',
					})
				}

			},
			SetQb() {
				var Box = document.getElementById("QbDownLoadBox");
				var token = this.checkUser()
				this.QbStartDownloadVisible = false
				const loading = ElLoading.service({
				  lock: true,
				  text: 'Loading',
				  target: Box,
				  // background: 'rgba(0, 0, 0, 0.7)',
				})
				if(this.torrent){
					axios({
						data: {
							path:this.qbPath,
							torrent:this.torrent
						},
						url:'/nas/setQbittor',
						method: 'post',
						headers:{
							'token': token
						},
					}).then((res) => {
						
						loading.close()
						ElMessage({
							message: "添加成功",
							type: 'success',
						})
						this.torrent = ''
						// return resolve(res.data.data)
					}).catch(()=> {
						loading.close()
						ElMessage({
							message: "添加失败",
							type: 'warning',
						})
					})
				}else {
					loading.close()
					ElMessage({
						message: "链接不能为空",
						type: 'warning',
					})
				}
			}
		}
	}
</script>

<style scoped src="../../../static/css/qbDownloadCss.css"></style>