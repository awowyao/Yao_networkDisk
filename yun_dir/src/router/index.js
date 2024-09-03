import {
	createRouter,
	createWebHashHistory,
	createWebHistory
} from 'vue-router'
// import HomeView from '../views/HomeView.vue'

const routes = [{
		// mode: 'history',
		path: '/',
		// name: '/',
		component: () => import('@/views/Main.vue'),
		children: [
			{
				path: '/',
				name: 'Home',
				meta:{'title':'云首页'},
				component: () => import('@/views/Home/Home.vue')
			},
			{
				path: '/aliHome',
				name: 'aliHome',
				meta:{'title':'阿里云首页'},
				component: () => import('@/views/Home/aliyunHome.vue')
			},
			{
				path: '/video',
				name: 'Video',
				component: () => import('@/views/VideoManage/VideoManage.vue')
			},
			{
				path: '/user',
				name: 'User',
				meta:{'title':'用户管理'},
				component: () => import('@/views/UserManage/UserManage.vue')
			},
			{
				path: '/updata',
				name: 'updata',
				meta:{'title':'上传'},
				component: () => import('@/views/Home/updata/updata.vue')
			},
			{
				path: '/upload',
				name: 'upload',
				component: () => import('@/views/Home/updata/upload.vue'),
				meta: {
					// title: '上传',
					keepAlive: true
				}
			},
			{
				path: '/qbDownload',
				name: 'qbDownload',
				meta:{'title':'离线下载状态'},
				component: () => import('@/views/Home/qbDownload/qbDownload.vue')
			},
			{
				path: '/DownloadData',
				name: 'DownloadData',
				meta:{'title':'离线下载添加'},
				component: () => import('@/views/Home/qbDownload/DownloadData.vue')
			},
			{
				path:'/UserManage',
				name:'UserManage',
				meta:{'title':'用户管理'},
				component: () => import('@/views/UserMsg/UserManage.vue')
				
			},
			{
				path:'/Editor',
				name:'Editor',
				meta:{'title':'文件编辑'},
				component: () => import('@/views/TextEditor/Editor.vue')
				
			},
			{
				path:'/SystemManage',
				name:'SystemManage',
				meta:{'title':'系统信息'},
				component: () => import('@/views/SystemManage/SystemManage.vue')
			}
		]
	},

	{
	  path: '/User/Login',
	  name: 'Login',
	  meta:{'title':'yun登录'},
	  // route level code-splitting
	  // this generates a separate chunk (about.[hash].js) for this route
	  // which is lazy-loaded when the route is visited.
	  component: () => import('@/views/UserMsg/UserLogin.vue')
	},
	{
	  path: '/User/Sign',
	  name: 'Sign',
	  meta:{'title':'yun注册'},
	  // route level code-splitting
	  // this generates a separate chunk (about.[hash].js) for this route
	  // which is lazy-loaded when the route is visited.
	  component: () => import('@/views/UserMsg/UserSign.vue')
	},
	// {
	//   path: '/AliyunUpload',
	//   name: 'AliyunUpload',
	//   // route level code-splitting
	//   // this generates a separate chunk (about.[hash].js) for this route
	//   // which is lazy-loaded when the route is visited.
	//   component: () => import('@/views/AliyunUpload/Upload.vue')
	// }
]

const router = createRouter({
  history: createWebHistory("/"),
  routes
})

router.beforeEach((to, from, next) => {
	if (to.matched.length === 0) {  // 如果未匹配到路由
	   from.name ? next({ name: from.name }) : next('/')
	 } else {
		window.document.title = to.meta.title
		next()  // 如果匹配到正确跳转
	 }
  
  next()
})

export default router
