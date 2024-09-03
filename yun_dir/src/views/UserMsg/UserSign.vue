<template>
<view class="LoginApp">
		<view class="LogsinBox AddUser">

			<h1 class="LoginH1">注册</h1>
			<view class="LoginFrom">
				<view class="UserFrom">
					<span class="LoginText">账号:</span>
					<el-input class="LoginInput" v-model="AddUserName" placeholder="请输入账号" clearable />
				</view>
				<span id="AddUserNameID" class="UserErrowText">账号不能为空</span>
				<view class="UserFrom">
					<span class="LoginText">密码:</span>
					<el-input class="LoginInput" v-model="AddUserPwd" type="password" placeholder="请输入密码"
						show-password />
				</view>
				<span id='AddUserPWDID' class="UserErrowText">密码不能少于8位至少要有数字和字母</span>
				<view class="UserFrom">
					<span class="LoginText">邮箱:</span>
					<el-input class="LoginInput" v-model="AddUserElmer" placeholder="请输入邮箱" clearable />
				</view>
				<span id='AddUserElmerID' class="UserErrowText">邮箱不能为空或格式不正确</span>
				<view class="UserBotton">
					<el-button class="UserBottonD" color="#626aef" :disabled="AddUserVlue" :dark="isDark" @click="AddUser">注册</el-button>
					<el-button class="UserBottonD" color="#626aef" :dark="isDark" @click="GoLogin">去登录</el-button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import { ElLoading, ElMessage } from 'element-plus'
	import axios from 'axios'
	
	export default {
		data() {
			return {
				isLogin: false,
				AddUserName:'',
				AddUserPwd:'',
				AddUserElmer:'',
			}
		},
		methods: {
			AddUser() {
				axios.post('/nas/userApi/Sign', {
					
					'userName':this.AddUserName,
					'userPwd':this.AddUserPwd,
					'userEmail':this.AddUserElmer,
					
				}).then((res) =>{
					// window.localStorage.setItem('UserToken', res.data.))
					ElMessage({
						message: res.data.msg,
						type: 'success',
					})
					this.GoLogin()
				}).catch((error) => {
					if (error.response.status == 401){
						ElMessage({
							message: error.response.data.msg,
							type: 'warning',
						})
					}
				})
			
			},
			GoLogin() {
				this.$router.push({
					name: 'Login',
				})
			}
		}
	}
</script>

<style scoped src="../../static/css/UserLoginCss.css"></style>