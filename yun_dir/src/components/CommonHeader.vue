<template>
	<header>
		<div class="l-content">
			<el-button @click="collapseMenu" type="primary" icon="Edit" class="Menu windows" />

			<el-button @click="IphoneMenu" type="primary" icon="Edit" class="Menu phone" />
			<el-breadcrumb separator="/">
				<el-breadcrumb-item @click="clickMenu()" >首页</el-breadcrumb-item>
				<el-breadcrumb-item class="HeaderTabMenu"  @click="clickMenu(index)" v-for="(i,index) in current" :key="index">

					{{i}}
				</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="r-content">
			<view class="UpContent">
				<el-button v-if="nowPaht=='1'" class="windows" type="primary" style="margin-right: 20px;" @click="updataOpen">
				      Upload<el-icon class="el-icon--right"><Upload /></el-icon>
				</el-button>
				<el-upload class="upload-demo"
				 action 
				:http-request="handleUpload"
				:show-file-list='false'
				v-if="nowPaht=='2'"
				>
					<el-button  class="windows" type="primary" style="margin-right: 20px;">点击上传</el-button>
					
				</el-upload>
				<el-button v-if="nowPaht=='1'" class="phone" type="primary" style="margin-right: 20px;" @click="updataOpen" icon="Upload" />
				<el-dropdown trigger="click">
					<span class="el-dropdown-link">
						<el-avatar icon="UserFilled" /><el-icon class="el-icon--right"><arrow-down /></el-icon>
					</span>
					<template #dropdown>
						<el-dropdown-menu>
							<el-dropdown-item icon="Plus" @click="GoLogin" v-if="userMsg.UserName == ''">登录</el-dropdown-item>
							<el-dropdown-item icon="Plus"  v-else>{{userMsg.UserName}}</el-dropdown-item>
							<el-dropdown-item icon="CirclePlusFilled" @click="GoSign" v-if="userMsg.UserName == ''">注册</el-dropdown-item>
						</el-dropdown-menu>
					</template>
				</el-dropdown>
			</view>
			
		</div>
	</header>
	
	<el-drawer v-model="updataDrawer" :direction="direction" :size="updataWidth"  title='文件上传'
		custom-class="PhoneMenuDrawer"   :show-close='false'>
		<template #header="{ close, titleId, titleClass }">
		  <h4 :id="titleId" :class="titleClass">文件上传</h4>
		  <el-button type="danger" @click="updataDrawer = false">
			<el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>
			关闭
		  </el-button>
		</template>
		<template #default>
			  <el-upload 
			    class="upload-demo"
			    drag
			    action="/nas/upload"
				name="file"
			    multiple
				:on-success="UpDataSuccess"
				:headers="Updataheaders"
				:data="UpDataDic"
			  >
			    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
			    <div class="el-upload__text">
			      托转上传或 <em>点击上传</em>
			    </div>
			    <template #tip>
			      <div class="el-upload__tip">
			        上传列表
			      </div>
			    </template>
			  </el-upload>
		</template>
		<template #footer>
			<view class="MenuSizeProgress">
				<el-progress :text-inside="true" :stroke-width="28" :percentage="percentage" :color="MenuSizicustomColors" />
			</view>
			<view class="MenuSizeProgressText" style="color: #666666;">
				<text>{{uesSize}}/{{totalSize}}</text>
			</view>
		</template>
	</el-drawer>
</template>

<script>
	import axios from 'axios'
import {
		mapState
	} from 'vuex'

	export default {
		computed: {
			...mapState({
				current: state => state.tab.currentMenu,
				uploadList: state => state.upload.uploadData
			})
		},

		data() {
			return {
				suerImg: require('../assets/images/baox.png'),
				updataDrawer:false,
				updataWidth:'40%',
				token:'',
				UpDataDic:{},
				Updataheaders:{},
				userMsg:{
					UserName:'',
					UserCover:'',
					UserEmail:'',
				},
				nowPaht:'1',
				
			}
		},
		watch: {
			$route: {
				handler: function(val, oldVal){
					if(val.path == '/'){
						this.nowPaht = '1'
					}else if(val.path = 'aliHome'){
						this.nowPaht = '2'
					}
				},
			}
		},
		methods: {
			
			collapseMenu() {
				this.$store.commit('collapseMenu')
			},
			IphoneMenu() {
				this.$store.commit('phoneMenu')
			},
			clickMenu(path) {
				let Route = this.$route.query.route
				if (Route){
					Route = Route.split('/')
					if (Route.includes('media')) {
						var i = Route.indexOf('media')
						Route.splice(i, 1)
					}
					const NewRoute = Route.slice(0, path + 1)
					// var nextPath = this.$route.path
					// if (nextPath[0] != '/') {
					// 	nextPath = '/'+nextPath
					// }
					
					this.$router.push('/?route=' + NewRoute.join('/'))
				}
				else {
					Route = []
				}
			},
			GoLogin() {
				this.$router.push({
					name:'Login'
				})
			},
			GoSign() {
				this.$router.push({
					name:'Sign'
				})
			},
			GetUserMsg(token) {
				axios({
					url:'/nas/userApi/GetUserMsg',
					method: 'post',
					headers:{
						'token': token
					}
				}).then((res) => {
					this.userMsg.UserName = res.data.userName
					this.userMsg.UserEmail = res.data.userEmail
					this.userMsg.UserCover = res.data.user_cover
				}).catch((error)=>{
					if(error.response.status == 403){
						this.$router.push({
							name: 'Login',
						})
					}
				})
			},
			updataOpen() {
				let Route = this.$route.query.route
				if (!Route) {
					Route = ''
				}
				this.token = this.$cookies.get('Token')
				this.UpDataDic = {
					'route':Route
				}
				this.Updataheaders = {
					'token': this.token
				}
				this.updataDrawer = true
			},
			handleUpload(option) {
				// 获取文件的后缀名
				var that = this;
				var obj = option.file.name
				let OSS = require('ali-oss')
				let Route = this.$route.query.route
				if (!Route) {
					Route = ''
				}
				let client = new OSS({
				  region: 'oss-cn-beijing',
				  secure: true,  // secure: 配合region使用，如果指定了secure为true，则使用HTTPS访问  
				  accessKeyId: 'LTAI5tF1BuAgVXZtax29gNzp',
				  accessKeySecret: 'h6zXOrNPwddoRIfxip2UqxmGl7r1fH',
				  bucket: 'awowyao'
				})
				
				
				var objName = obj
				let checkpoint;
				const dataDic = {
				  fileUploadPercent: 0,
				  fileName: objName,
				  fileTime: '',
				  fileSpeed: ''
				}
				that.uploadList.push(dataDic)
				var ListIndex =  that.uploadList.length - 1
				for (let i = 0; i < 5; i++) {
				  try {
				    const result = client.multipartUpload(''+objName, option.file, {
				      checkpoint,
				      async progress(percentage, cpt) {
						that.uploadList[ListIndex].fileUploadPercent = Math.floor(percentage * 100)
						console.log(cpt)
				      },
				    });
				    break; // 跳出当前循环
					  
				  } catch (e) {
				    console.log(e);
				  }
				}
			}
		},
		created() {
			var token = this.$cookies.get('Token')
			if(token) {
				this.GetUserMsg(token)
			}
			if (document.body.clientWidth < 600) {
				this.updataWidth = '100%'
			}
		}
	}
</script>

<style lang="scss" scoped>
	header {
		display: flex;
		height: 100%;
		align-items: center;
		justify-content: space-between;
	}

	.l-content {
		display: flex;
		align-items: center;

		.el-button {
			margin-right: 20px;
		}

		// justify-content: space-between;
	}
	.HeaderTabMenu:hover {
		cursor:pointer;
		color: #409eff;
	}
	.r-content {
		float: right;
	}
	
</style>

<style lang="scss">
	.el-breadcrumb__item {
		.el-breadcrumb__inner {
			color: rgb(196, 196, 196);
			font-weight: normal;
		}
		.el-breadcrumb__inner:hover {
			color: #409eff;
		}
		&:last-child {
			.el-breadcrumb__inner {
				color: rgb(255, 255, 255);
				cursor: default;
			}
			.el-breadcrumb__inner:hover {
				color: rgb(255, 255, 255);
				cursor: default;
			}
		}
	}
</style>
<style scoped src="../static/css/CommonHeaderSize.css"></style>