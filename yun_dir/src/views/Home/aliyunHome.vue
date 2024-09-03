<!-- eslint-disable vue/multi-word-component-names -->
<template>
	<div ref="select_frame" style="width: 100%; height: 100%;" id="DirScrropHome" class="RightClick">
		<div class="DataListItems RightClick">
			<view class="DataListItem feiclick" v-for="(item,j)  in ReadDir.dir" :key="j" @click="Get_Dir(item.data)"
				@touchstart="goTouchstart($event, item.data)" @touchmove="goTouchend($event)"
				@touchend="goTouchend($event)" @contextmenu.prevent="openRightMenu($event, item.data)">
				<view class="DataImgView feiclick">
					<el-image class="feiclick" style="width: 100%; height: 100%" :src="item.cover" fit="scale-down" />
				</view>
				<p class="feiclick">{{ item.data }}</p>
			</view>
			<view class="DataListItem feiclick" v-for="(item,j) in ReadDir.file" :key="j" @click="Get_file(item.data)"
				@touchstart="goTouchstart($event, item.data, true)" @touchmove="goTouchend($event)"
				@touchend="goTouchend($event)" @contextmenu.prevent="openRightMenu($event, item.data, true)">
				<view class="DataImgView feiclick">
					<el-image class="feiclick" style="width: 100%;height: 100%;" :src="'media/' + item.cover"
						fit="scale-down" v-if="item.FileType=='Video'"/>
					<el-image class="feiclick" style="width: 100%;height: 100%;" :src="'media/' + item.cover"
						fit="scale-down" v-else-if="item.FileType=='img'" />
					<el-image class="feiclick" style="width: 100%;height: 100%;" :src="item.cover"
						fit="scale-down" v-else />
				</view>
				<p class="feiclick">{{ item.data }}</p>
			</view>
		</div>
	</div>
	<div class="menuDiv" id="menu">
		<ul class="RightMenu">
			<li @click="OpenFileToDir" v-if="menuSelect !== ''">打开</li>
			<li @click="CreateDirNameVisible = true" v-if="menuSelect == ''">新建文件夹</li>
			<li @click="CreatefileNameVisible = true" v-if="menuSelect == ''">新建文件</li>
			<li @click="MoveDirNameVisible = true" v-if="menuSelect !== ''">移动</li>
			<li v-if="fileUrl !== '#' && menuSelect !== ''"><a :href="fileUrl" download>下载</a></li>
			<li @click="centerDialogVisible = true">删除</li>
		</ul>
	</div>
	<el-dialog v-model="centerDialogVisible" title="Warning" :width="dialogWidth" >
		<span>{{selectPath}}</span>
		<template #footer>
			<span class="dialog-footer">
				<el-button @click="centerDialogVisible = false">取消</el-button>
				<el-button type="primary" @click="deleteFileToDir">
					确定
				</el-button>
			</span>
		</template>
	</el-dialog>
	<el-dialog v-model="CreateDirNameVisible" :width="dialogWidth" title="新建文件夹">
		<el-input v-model="CreateDirName" placeholder="文件夹名称" maxlength="10" show-word-limit />
		<template #footer>
		<el-button @click="CreateDirNameVisible = false">取消</el-button>
			<el-button type="primary" @click="createDir">
				确定
			</el-button>
		</template>
	</el-dialog>
	
	<el-dialog v-model="CreatefileNameVisible" :width="dialogWidth" title="新建文件">
		<el-input v-model="CreatefileName" placeholder="文件名称" maxlength="10" show-word-limit />
		<template #footer>
		<el-button @click="CreatefileNameVisible = false">取消</el-button>
			<el-button type="primary" @click="createFile">
				确定
			</el-button>
		</template>
	</el-dialog>
	
	<el-dialog v-model="MoveDirNameVisible" :width="dialogWidth" title="移动文件夹">
		<el-tree :props="props" :load="loadNode" node-key="id" @node-expand="handleBucketClick" @node-collapse="handleBucketClick"  @node-click="handleBucketClick" lazy />
		<template #footer>
		<el-button @click="MoveDirNameVisible = false">取消</el-button>
			<el-button type="primary" @click="moveFileToDir">
				确定
			</el-button>
		</template>
	</el-dialog>
	
</template>

<script>
	import axios from 'axios'
	import {
		mapState
	} from 'vuex'
	import {
		DropdownInstance
	} from 'element-plus'
	import { ElLoading } from 'element-plus'
	export default {
		computed: {
			...mapState({
				current: state => state.tab.currentMenu,
				Data: state => state.tab.filedata

			})
		},
		// updated() {
		// 	// console.log(123456)
		// 	// this.updata()

		// },
		watch: {
			$route: {
				handler: function(val, oldVal){
					if(val.path == 'aliHome'){
						this.updata(oldVal)
					}
				},
			}
		},
		data() {
			return {
				ReadDir: {
					dir: [],
					file: [],
					screenWidth: null,
					elcolSpan: 7
				},
				dd: [],
				ff: [],
				node: {}, // tree 节点对象
				props: {
					label: 'name',
					children: 'zones',
					isLeaf: 'leaf',
				},
				timeOutEvent: 0,
				menuVisible: true,
				selectPath: '',
				centerDialogVisible: false,
				dialogWidth: '30%',
				menuSelect: '',
				CreateDirNameVisible:false,
				CreateDirName:'',
				CreatefileNameVisible:false,
				CreatefileName:'',
				MoveDirNameVisible:false,
				movePath:'',
				fileUrl:'#'

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
			clickMenu(item) {
				const Route = this.$route.query.route
				// this.$router.push({ name: item.name })
				this.$store.commit('selectMenu', Route)
			},
			OpenFileToDir() {
				if (this.fileUrl == '#') {
					this.Get_Dir(this.menuSelect)
				}
				else {
					this.Get_file(this.menuSelect)
				}
			},
			Get_Dir(path) {

				let Route = this.$route.query.route
				if (!Route) {
					Route = ''
				} else {
					Route = Route + '/'
				}
				// this.$router.push('/nas?route=' + path)
				this.$router.push({
					name: 'aliHome',
					query: {
						route: Route + path
					}
				})
				// window.location.href= '#/?route='+Route + path;

			},
			Get_file(path) {
				const Route = this.$route.query.route ? this.$route.query.route : ''

				let FileW = path.split('.')
				FileW = FileW.slice(-1)[0]
				if (FileW === 'mp4' || FileW === 'avi' || FileW === 'mkv') {
					if(!Route){
						this.$router.push('/video?route=media' + Route + '/' + path)
					}else{
						this.$router.push('/video?route=media/' + Route + '/' + path)
					}
				}else if(FileW === 'txt' || FileW === 'py' || FileW==='js' || FileW==='vue' || FileW==='html') {
					if (!Route){
						this.$router.push('/Editor?route='+path)
					}else{
						this.$router.push('/Editor?route=' + Route + '/' + path)
					}
					
				}

			},
			updata(oldpath='#') {
				let Route = this.$route.query.route
				var token = this.checkUser()
				var home = document.getElementById("DirScrropHome");
				const loading = ElLoading.service({
				  lock: true,
				  text: 'Loading',
				  target: home,
				  // background: 'rgba(0, 0, 0, 0.7)',
				})
				this.$store.commit('selectMenu', Route)
				if (!Route) {
					Route = ''
				}
				axios({
					url:'/nas/Oss/GetGoute',
					params: {
						route: '/' + Route
					},
					method: 'get',
					headers:{
						'token': token
					}
				}).then((res) => {
					this.dd = res.data.dir
					this.ff = res.data.file
					this.ReadDir.dir = this.dd
					this.ReadDir.file = this.ff
					loading.close()
				}).catch((error)=>{
					// console.log(oldpath)
					if (oldpath !== '#') {
						this.$router.push({
							name: 'aliHome',
							query: oldpath.query

						})
					}
					else if(error.response.status == 403) {
						this.$router.push({
							name: 'Login',
						})
					}
					// this.$router.back()
					loading.close()
				})

			},

			goTouchstart(e, fileName, file=false) {
				let _this = this;
				clearTimeout(_this.timeOutEvent);
				_this.timeOutEvent = setTimeout(function() {
					_this.timeOutEvent = 0;
					//  处理长按事件...
					_this.menuSelect = fileName
					let Route = _this.$route.query.route
					if (!Route) {
						Route = ''
					}
					_this.selectPath = '/' + Route + '/' + fileName
					if (file) {
						_this.DownloadFile()
					}else {
						this.fileUrl = '#'
					}
					var curPosX = e.changedTouches[0].clientX
					var curPosY = e.changedTouches[0].clientY
					var obj = document.getElementById("menu");
					obj.style.cssText = "top:" + curPosY + "px;left:" + curPosX + "px; display:flex;";
				}, 500);
			},
			//手如果在600毫秒内就释放，则取消长按事件
			goTouchend() {
				let _this = this;
				clearTimeout(_this.timeOutEvent);
				if (_this.timeOutEvent !== 0) {
					//  处理单击事件
					var obj = document.getElementById("menu");
					obj.style.cssText = "display:none;";
				}
			},
			openRightMenu(e, fileName, file=false) {
				this.menuSelect = fileName
				// alert(fileName)

				let Route = this.$route.query.route
				if (!Route) {
					Route = '/' + fileName
					this.selectPath = Route
				} else {
					this.selectPath = '/' + Route + '/' + fileName
				}
				if (file) {
					this.DownloadFile()
				}else {
					this.fileUrl = '#'
				}
				// 获取当前位置x
				var curPosX = e.x
				var curPosY = e.y
				var obj = document.getElementById("menu");
				obj.style.cssText = "top:" + curPosY + "px;left:" + curPosX + "px; display:flex;";
			},
			createDir() {
				var token = this.checkUser()
				var Route = this.$route.query.route
				if (!Route) {
					Route = '/'
					
				}else {
					Route = '/' + Route
				}
				axios({
					url:'/nas/Oss/createDir',
					data: {
						path: Route,
						dirName: this.CreateDirName,
					},
					method: 'post',
					headers:{
						'token': token
					}
				}).then((res) => {
					this.CreateDirNameVisible = false
					this.updata()
				})
			},
			createFile() {
				var token = this.checkUser()
				var Route = this.$route.query.route
				if (!Route) {
					Route = '/'
					
				}else {
					Route = '/' + Route
				}
				axios({
					url:'/nas/createFile',
					data: {
						path: Route,
						dirName: this.CreatefileName,
					},
					method: 'post',
					headers:{
						'token': token
					}
				}).then((res) => {
					this.CreatefileNameVisible = false
					this.updata()
				})
			},
			deleteFileToDir() {
				var token = this.checkUser()
				var Type = 'file'
				if (this.fileUrl== '#') {
					Type = 'dir'
				}
				axios( {
					url:'/nas/Oss/DeleteUserManage',
					data: {
						path: this.selectPath,
						t:Type
					},
					method: 'post',
					headers:{
						'token': token
					}
				}).then((res) => {
					this.centerDialogVisible = false
					this.updata()
				})
			},
			handleBucketClick: function (data, node) {
				this.movePath = data.path
			},
			moveFileToDir() {
				var token = this.checkUser()
				axios({
					url:'/nas/Oss/moveDirFile',
					method: 'post',
					headers:{
						'token': token
					},
					data: {
						oldPath: this.selectPath,
						NewPath: this.movePath,
					},
				}).then((res) => {
					this.MoveDirNameVisible = false
					this.updata()
				})
			},
			loadNode(node, resolve) {
				var token = this.checkUser()

				// console.log(node, resolve)
				// console.log(node.level)
				if (node.level === 0) {
					axios({
						url:'/nas/Oss/GetDisk',
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
						url:'/nas/Oss/GetDisk',
						params: {
							route: node.data.path
						},
						method: 'get',
						headers:{
							'token': token
						},
					}).then((res) => {
						return resolve(res.data.data)
					})
				}
			},
			DownloadFile() {
				const Route = this.$route.query.route ? this.$route.query.route : ''
				this.fileUrl = 'media/' + this.selectPath
			},
			RightMouse() {
					document.addEventListener('mouseup', (e) => {
					if(e.button == 2){
						if (e.target.className !== 'feiclick' && e.target.className !== 'el-image__inner' && e.target
								.className !== 'el-image__wrapper' && e.target.className !== 'el-image__error' && (e.target.className=='RightClick' || e.target.className=='DataListItems RightClick')) {
								this.menuSelect = ''
								var curPosX = e.clientX
								var curPosY = e.clientY
								var obj = document.getElementById("menu");
								obj.style.cssText = "top:" + curPosY + "px;left:" + curPosX + "px; display:flex;";
								
							}    
					}
				})
				document.addEventListener('contextmenu', (e) => {
						// console.log(e.clientX)
						e.preventDefault();
						// alert(this.menuSelect)
						// alert(123456)
						// this.menuSelect = ''
						// var curPosX = e.clientX
						// var curPosY = e.clientY
						// var obj = document.getElementById("menu");
						// obj.style.cssText = "top:" + curPosY + "px;left:" + curPosX + "px; display:flex;";
				})
				document.oncontextmenu = function (e) {
			      e.preventDefault();
			    };
			},
		},
		mounted() {
			this.RightMouse()
			this.updata()
			if (document.body.clientWidth < 500) {
				this.dialogWidth = '80%'
			}
			this.$refs.select_frame.ondragleave = (e) => {
				e.preventDefault() // 阻止离开时的浏览器默认行为
			}
			this.$refs.select_frame.ondrop = (e) => {
				e.preventDefault() // 阻止拖放后的浏览器默认行为
				const data = e.dataTransfer.files // 获取文件对象
				if (data.length < 1) {
					return // 检测是否有文件拖拽到页面
				}
				// console.log(e.dataTransfer.files)
				var token = this.checkUser()
				for (let i = 0; i < e.dataTransfer.files.length; i++) {
					var Route = this.$route.query.route
					if (!Route) {
						Route = ''
					}
					this.$store.commit('uploadData', [e.dataTransfer.files[i], Route, token])
				}
			}
			this.$refs.select_frame.ondragenter = (e) => {
				e.preventDefault() // 阻止拖入时的浏览器默认行为
				this.$refs.select_frame.border = '2px dashed red'
			}
			this.$refs.select_frame.ondragover = (e) => {
				e.preventDefault() // 阻止拖来拖去的浏览器默认行为
			}
			this.screenWidth = document.body.clientWidth
			window.onresize = () => { // 屏幕尺寸变化就重新赋值
				return (() => {
					this.screenWidth = document.body.clientWidth
					if (this.screenWidth < 500) {
						this.$store.commit('collapseMenu')
						this.dialogWidth = '80%'
					}
				})()
			}
		},

	}
</script>

<style lang="scss" scoped>
	.el-row {
		margin-bottom: 20px;
		//   background-color: rgb(0, 0, 0);
	}

	.el-card {
		min-width: 100%;
		height: 100%;
	}

	.el-row:last-child {
		margin-bottom: 0;
	}

	.el-col {
		border-radius: 4px;
		height: 180px;
	}

	.grid-content {
		border-radius: 4px;
		min-height: 36px;
	}

	.menuDiv {}
</style>
<style scoped src="../../static/css/homeCss.css"></style>
<style scoped src="../../static/css/homeSize.css"></style>