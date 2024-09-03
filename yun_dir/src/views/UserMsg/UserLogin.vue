<template>
	<view class="LoginApp">
		<view class="LogsinBox" @keyup.enter="UserLogin">
			<h1 class="LoginH1">登录</h1>
			<view class="LoginFrom">
				<view class="UserFrom">
					<span class="LoginText">账号:</span>
					<el-input class="LoginInput" v-model="UserName" placeholder="请输入账号" clearable />
				</view>
				<span id="LoginUserNameID" class="UserErrowText">账号不能为空</span>
				<view class="UserFrom">
					<span class="LoginText">密码:</span>
					<el-input class="LoginInput" v-model="UserPwd" type="password" placeholder="请输入密码" show-password />
				</view>
				<span id='LoginUserPWDID' class="UserErrowText LoginUserPwd">密码不能为空</span>
			</view>
			<view class="UserBotton">
				<el-button class="UserBottonD" color="#626aef" :disabled="LoginVlue"
					@click="UserLogin"  >登录
				</el-button>
				<el-button class="UserBottonD" color="#626aef" @click="GoSign">注册</el-button>
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
				UserName:'',
				UserPwd:''
			}
		},
		methods: {
			UserLogin() {
				axios({
					url:'/nas/userApi/Login',
					data: {
						'userName':this.UserName,
						'userPwd':this.UserPwd,
					},
					method: 'post',
					headers:{
						
					}
				}).then((res) => {
					this.$cookies.set('Token', res.data.token, 60*60*24*7 );
					this.$cookies.set('UserName', res.data.userName+'as_d*ax_csd', 60*60*24*7 );
					this.$cookies.set('UserSpeed', res.data.speed+'as_d', 60*60*24*7 );
					ElMessage({
						message: '登录成功',
						type: 'success',
					})
					this.$router.push({
						name: 'Home',
					})
					
				}).catch((error) => {
					if (error.response.status == 401){
						ElMessage({
							message: error.response.data.msg,
							type: 'warning',
						})
					}
					else if(error.response.status == 403){
						ElMessage({
							message: error.response.data.msg,
							type: 'warning',
						})
						this.UserPwd='';
					}
				})
			},
			GoSign() {
				this.$router.push({
					name: 'Sign',
				})
			}
		}
	}
</script>

<style scoped src="../../static/css/UserLoginCss.css"></style>