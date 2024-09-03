<template>

	<el-menu active-text-color="#ffd04b" background-color="#545c64" class="el-Nasmenu" default-active="2"
		:collapse="ifMenu" text-color="#fff">
	
		<el-menu-item :index="item.path" v-for="item in noChildren" :key="item.path" @click="clickMenu(item)">
			<el-icon><component :is="item.icon"/></el-icon>
			<span>{{item.label}}</span>
		</el-menu-item>
		<el-sub-menu :index="index+''" v-for="(item,index) in hesChildren" :key="item.path">
			<template #title>
				<el-icon><component :is="item.icon"/></el-icon>
				<span>{{item.label}}</span>
			</template>
			<el-menu-item-group>
				<el-menu-item :index="childern.path" v-for="childern in item.childern" :key="childern.path"
					@click="clickMenu(childern)">
					<el-icon><component :is="childern.icon"/></el-icon>
					{{childern.label}}
				</el-menu-item>
				
			</el-menu-item-group>
			
		</el-sub-menu>
		<view class="MenuSizeProgressView" v-show="!ifMenu">
			<view class="MenuSizeProgress">
				<el-progress :text-inside="true" :stroke-width="28" :percentage="percentage" :color="MenuSizicustomColors" />
			</view>
			<view class="MenuSizeProgressText">
				<text>{{uesSize}}/{{totalSize}}</text>
			</view>
		</view>
	</el-menu>
	
	<el-drawer v-model="phoneMenuI" :direction="direction" size="100%"  title='菜单选项'
		custom-class="PhoneMenuDrawer"   :show-close='false'>
		<template #header="{ close, titleId, titleClass }">
		  <h4 :id="titleId" :class="titleClass">菜单选项</h4>
		  <el-button type="danger" @click="closephoneMenu">
			<el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>
			关闭
		  </el-button>
		</template>
		<template #default>
			<view class="phoneMenuItems">
				<view class="phoneMenuItem" @click="GoIndex">
					首页
				</view>
				<view class="phoneMenuItem" @click="GoQbDownload">
					下载种子
				</view>
				<view class="phoneMenuItem" @click="GoQbDownloadData">
					下载状态
				</view>
				<view class="phoneMenuItem" @click="GoUserManage">
					用户管理
				</view>
				<view class="phoneMenuItem" @click="GoSystem">
					系统状态
				</view>
			</view>
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
	export default {
		computed: {
			noChildren() {
				return this.asiderMenu.filter(item => !item.childern)
			},
			hesChildren() {
				return this.asiderMenu.filter(item => item.childern)
			},
			ifMenu() {
				return this.$store.state.tab.ifMenu
			},
			phoneMenuI() {
				return this.$store.state.tab.ifphoneMenu
			}
		},
		data() {
			return {
				percentage:0,
				totalSize:0,
				uesSize:0,
				MenuSizicustomColors: [
				  { color: '#5cb87a', percentage: 20 },
				  { color: '#1989fa', percentage: 40 },
				  { color: '#6f7ad3', percentage: 60 },
				  { color: '#e6a23c', percentage: 80 },
				  { color: '#f56c6c', percentage: 100 },
				],
				asiderMenu: [
					{
						path: '/',
						name: 'Home',
						label: '首页',
						icon: 'House'
					},
					{
						path: '/updata',
						name: 'updata',
						label: '上传进度',
						icon: 'Upload'
					},
					{
						label: '存储',
						icon: 'Download',
						childern: [{
							path: '/',
							name: 'Home',
							label: '硬盘',
							icon: 'DocumentAdd'
						},
						{
							path: '/aliHome',
							name: 'aliHome',
							label: '阿里云oss',
							icon: 'PieChart'
						}]
					},
					{
						label: 'TB下载管理',
						icon: 'Download',
						childern: [{
							path: '/qbDownload',
							name: 'qbDownload',
							label: '下载种子',
							icon: 'DocumentAdd'
						},
						{
							path: '/DownloadData',
							name: 'DownloadData',
							label: '下载状态',
							icon: 'PieChart'
						}]
					},
					{
						label: '管理',
						icon: 'Tools',
						childern: [{
							path: '/UserManage',
							name: 'UserManage',
							label: '用户管理',
							icon: 'UserFilled'
						},
						{
							path: '/SystemManage',
							name: 'SystemManage',
							label: '系统管理',
							icon: 'Platform'
						},
						{
							path: '/UserManage',
							name: 'UserManage',
							label: '设置',
							icon: 'setting'
						}]
					}
				],
				direction: 'ltr',
				onis:'false'
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
				this.$router.push({
					name: item.name
				})
				// this.$store.commit('selectMenu', item)
			},
			closephoneMenu() {
				this.$store.commit('phoneMenu')
			},
			GoIndex() {
				this.$router.push({
					name: 'Home',
					
				})
				this.closephoneMenu()
			},
			GoQbDownload() {
				this.$router.push({
					name: 'qbDownload',
				
				})
				this.closephoneMenu()
			},
			GoQbDownloadData() {
				this.$router.push({
					name: 'DownloadData',
					
				})
				this.closephoneMenu()
			},
			GetUserSize() {
				var token = this.checkUser()
				axios({
					url:'/nas/sys/GetSize',
					method:'get',
					headers:{
						'token': token
					}
				}).then((res)=>{
					this.percentage = res.data.percentage
					this.totalSize = res.data.totalSize
					this.uesSize = res.data.uesSize
				}).catch((error) =>{
					if(error.response.status == 403) {
						this.$router.push({
							name: 'Login',
						})
					}
				})
			},
			GoUserManage() {
				this.$router.push({
					name: 'UserManage',
					
				})
				this.closephoneMenu()
			},
			GoSystem() {
				this.$router.push({
					name: 'SystemManage',
					
				})
				this.closephoneMenu()
			}
		},
		created() {
			this.GetUserSize()
		}
	}
</script>

<style lang="scss" scoped>

</style>
<style scoped src="../static/css/CommonAsideCss.css"></style>
