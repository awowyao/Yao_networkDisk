<template>
	<div id="DirScrropEditor" style="width: 100%;height: 100%;">
		<div>
			<!-- 引入了 QuillEditor 组件，通过 :options 属性传递编辑器的选项参数，通过 v-model:content 实现双向绑定编辑器中的内容content 变量 -->
			<QuillEditor style="font-size: 16px;" ref="quillEditor"  :options="editorOption" v-model:content="content" contentType="html"/>
		</div>
		<el-button class="EditorElButton" @click="savaFileText" type="primary">保存</el-button>
	</div>

</template>

<script>
	import { mapState } from 'vuex'
	import { QuillEditor, Quill } from '@vueup/vue-quill';
	import { ElLoading, ElMessage } from 'element-plus'
	import '@vueup/vue-quill/dist/vue-quill.snow.css'
	import hljs from 'highlight.js'
	import 'highlight.js/styles/monokai-sublime.css'
	import axios from 'axios'
	export default {
		computed: {
		  ...mapState({
		    current: state => state.tab.currentMenu
		  })
		},
		components: {
			QuillEditor
		},
		data() {
			return {
				content: '',
				editorOption: {
					theme: 'snow',
					// formats:['code-block'],
					modules: {
						syntax: {
						            highlight: text => {
						                return hljs.highlightAuto(text).value; // 这里就是代码高亮需要配置的地方
						                }
						        },
						toolbar: false
					},
					placeholder: '本文件无内容'
				}
			}
		},
		mounted() {
			this.GetFileText()
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
			GetFileText() {
				const Route = this.$route.query.route
				this.$store.commit('selectMenu', Route)
				var token = this.checkUser()
				// alert(Route)
				// const quillEditor = ref()
				var home = document.getElementById("DirScrropEditor");
				const loading = ElLoading.service({
				  lock: true,
				  text: 'Loading',
				  target: home,
				  // background: 'rgba(0, 0, 0, 0.7)',
				})
				axios( {
					url:'/nas/GetFileText',
					data: {
						path: Route,
					},
					method: 'post',
					headers:{
						'token': token
					}
				}).then((res) => {
					this.content = '<pre>'+ res.data.text +'</pre>'
					this.$refs.quillEditor.setHTML(this.content)
					loading.close()
					// alert(this.content)
				})
				// alert(this.$refs.quillEditor.getText())
				// this.$refs.quillEditor.formatText(0, 2);
		
				
			},
			savaFileText() {
				const text = this.$refs.quillEditor.getText()
				const Route = this.$route.query.route
				var token = this.checkUser()
				// alert(Route)
				// const quillEditor = ref()
				axios( {
					url:'/nas/setFileText',
					data: {
						path: Route,
						fileText:text
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
					// alert(this.content)
				})
			}
		}

	}
</script>

<style>
	.EditorElButton{
		position: absolute;
		right: 20px;
		width: 110px;
	}
	#DirScrropEditor {
		position: relative;
	}
</style>