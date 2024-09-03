<template>
	<el-table :data="tableData" min-height="250" style="width: 100%;padding-bottom: 20px;">
		<el-table-column prop="id" label="id" :width="WindowsWidth.id" />
		<el-table-column prop="userName" label="用户名" :width="WindowsWidth.userName"/>
		<el-table-column prop="limitSpeed" label="限速" :width="WindowsWidth.limitSpeed">
			<template #default="scope">
				<el-radio-group v-model="scope.row.limitSpeed" size="small">
				  <el-radio label="是" style="margin-right: 16px;" border>是</el-radio>
				  <el-radio label="否" border>否</el-radio>
				</el-radio-group>
			</template>
		</el-table-column>
		<el-table-column label="用户权限"  :width="WindowsWidth.userLv">
			<template #default="scope">
				<el-radio-group v-model="scope.row.lv" size="small">
				  <el-radio label="1" style="margin-right: 16px;" border>普通</el-radio>
				  <el-radio label="2" style="margin-right: 16px;" border>不限速</el-radio>
				  <el-radio label="3" border>管理</el-radio>
				</el-radio-group>
			</template>
		</el-table-column>
		
		<el-table-column prop="operate"  min-width="180">
			<template #header>
			    <el-button type="primary" size="small" plain @click="AddUserVisible = true">添加用户</el-button>
			</template>
			<template #default="scope">
				<el-button link type="primary" size="small" @click="deleteUser(scope.row)">删除</el-button>
				<el-button link type="primary" size="small" @click="UpUserMsg(scope.row)">保存修改</el-button>
		    </template>
		</el-table-column>
	</el-table>
	
	 <el-dialog v-model="AddUserVisible" title="添加用户" :width="dialogWidth">
		<view class="UserBox">
			<view style="width: 80%;display: block;">
				<view class="UserFrom">
					<span class="LoginText">账号:</span>
					<el-input class="LoginInput" v-model="AddUserName" placeholder="请输入账号" clearable />
				</view>
				<view class="UserFrom">
					<span class="LoginText">密码:</span>
					<el-input class="LoginInput" v-model="AddUserPwd" type="password" placeholder="请输入密码"
						show-password />
				</view>
				<view class="UserFrom">
					<span class="LoginText">邮箱:</span>
					<el-input class="LoginInput" v-model="AddUserElmer" placeholder="请输入邮箱" clearable />
				</view>
			</view>
			 
		</view>
	    
	    <template #footer>
	      <span class="dialog-footer">
	        <el-button @click="AddUserVisible = false">取消</el-button>
	        <el-button type="primary" @click="AddUser">
	          添加
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
				WindowsWidth:{
					'id':'50',
					'userName': '150',
					'limitSpeed':'200',
					'userLv':'300',
					'operate':'250'
					
				},
				AddUserVisible:false,
				dialogWidth:'30%',
				AddUserName:'',
				AddUserPwd:'',
				AddUserElmer:'',
				ss:'1',
				tableData: []
			}
		},
		methods:{
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
			deleteUser(e) {
				const token = this.checkUser()
				axios({
					url:'/nas/User/DeleteUserManage',
					data:{
						UserId:e.id
					},
					method: 'post',
					headers:{
						'token': token
					}
				}).then((res) => {
					ElMessage({
						message: res.data.msg,
						type: 'success',
					})
					this.GetUserList()
					
				})
			},
			GetUserList(){
				const token = this.checkUser()
				axios({
					url:'/nas/User/GetUsersManage',
				
					method: 'get',
					headers:{
						'token': token
					}
				}).then((res) => {
					this.tableData = res.data.UsersList

				})
		
			},
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
					this.GetUserList()
					
				}).catch((error) => {
					if (error.response.status == 401){
						ElMessage({
							message: error.response.data.msg,
							type: 'warning',
						})
					}
				})
				this.AddUserVisible = false
			
			},
			UpUserMsg(User) {
				const token = this.checkUser()
				axios({
					url:'/nas/userApi/UpUserManage',
					data:{
						'UserId':User.id,
						'UserLv':User.lv,
						'UserSeepd':User.limitSpeed,
					},
					method: 'post',
					headers:{
						'token': token
					}
				}).then((res) =>{
					// window.localStorage.setItem('UserToken', res.data.))
					ElMessage({
						message: res.data.msg,
						type: 'success',
					})
					this.GetUserList()
					
				}).catch((error) => {
					if (error.response.status == 401){
						ElMessage({
							message: error.response.data.msg,
							type: 'warning',
						})
					}
				})
			}
		},
		mounted() {
			this.GetUserList()
			if (document.body.clientWidth < 700) {
				this.WindowsWidth = {
					'id':'40',
					'userName': '100',
					'limitSpeed':'150',
					'userLv':'260',
					'operate':'180'
					
				}
				this.dialogWidth = '80%'
			}
		}
		
	}
</script>
<style>
	.UserBox {
		width: 100%;
		/* padding: 0 100px; */
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
</style>
<style scoped src="../../static/css/UserLoginCss.css"></style>