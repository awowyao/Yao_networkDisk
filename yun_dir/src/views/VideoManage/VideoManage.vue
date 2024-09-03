<template>
	<div>
		<div id="dplayer" ref="mydplayer"></div>
		<div class="videoListBox">
			<h1 class="videoListTitle">当前目录下的视频</h1>
			<p class="videoListP" v-for="item in videoList">
				<spen v-if="item.data == thisVideoName" style="color: #22b50c;">{{item.data}}</spen>
				<spen v-else @click="GoVideo(item.data)">{{item.data}}</spen>
			</p>
		</div>
	</div>

</template>

<script>
	import DPlayer from 'dplayer'
	import axios from 'axios'
	import screenfull from 'screenfull'
	import {
		mapState
	} from 'vuex'

	export default {
		computed: {
			...mapState({
				current: state => state.tab.currentMenu
			})
		},
		data() {
			return {
				videoName: '',
				videoList:[],
				thisVideoName:'',
				dp:'',
			}
		},
		methods: {
			getVideoList(url, Route) {
				var Sorted = this.$route.query.Sorted;
				var token = this.$cookies.get('Token')
				axios({
					url:'/nas/GetGoute',
					params: {
						route: '/' + url,
						timeSorted: Sorted,
						mode: 3
					},
					method: 'get',
					headers:{
						'token': token
					}
				}).then((res) => {
					this.videoList = res.data.file
					for(var i =0;i<this.videoList.length;i++){
						if(this.videoList[i].data == this.thisVideoName){
							this.video(Route, this.videoList[i].videoZm)
							break
						}
					}
					
				})
				
				
				
			},
			GoVideo(url) {
				var Route = this.current.slice(0, -1).join('/')
				var Sorted = this.$route.query.Sorted;
				location.href='/video?route=media/' + Route + '/' + url+"&Sorted="+Sorted
			},
			video(url, zm) {
				this.dp = new DPlayer({
					container: document.getElementById('dplayer'),
					
					video: {
						url: url, // 视频路径
						// url:require('F:/动漫下载测试文件夹/备份/好看的/2.mp4'),
						// url:'http://192.168.2.242:5001/AnimentPalyApi/ShenShiPlay/?path=MZIlkAecAmTQqjRzz8xtTHOdpl/7Bv5bJMRq8/jDbim9v3/v61CVoC/BFfjILfh8JB6jzz9BohBumLcBm5x27Fr96HDd5Vxa5FfiNAQJcD/6CKLh8NlIA%2BbWeVHHrXMN381r1FNeIHiWFLsTTozzT5nZ%2Bo4wtkR1alHRsumXvsusf0Y1QJGShcqpqqyVSZ/UcwjlNPXaBi6VDLuXTenkA0YvxiUkIwG8csMEiWqIYKVRacCzjb5j8BKktHUkw7IGtD5TkM569Dn6rHg6blM%2BuMiQEQQl3qUQ2QQ1ntiV0TGquqX385Rp824xtIJRqrKDiHIMuuj0XRRm1TATmwGzTw==',
					},
					subtitle: {
					    url: 'media/' + zm,
						type:'webvtt',
						// url: 'http://localhost:8080/static/icon/2.vtt',
					    color: '#ffffff',
						fontSize: '30px',
						bottom: '4%'
					},
					autoplay: true, // 自动播放
					theme: '#b7daff', // 主题色
					lang: 'zh-cn', // 语言
					// screenshot: true,  //截图
					hotkey: true, // 热键：→快进等
					// logo: require('./1.png'), // 左上方log
					volume: 0.7, // 默认音量
					mutex: true, // 互斥
					// 右键选项
					// danmaku:true,
					highlight: [],
					    
				})
				this.dp.play()
				// 执行API
				// this.dp.on('play', () => { 
				// 	let width = document.documentElement.clientWidth
				// 	let height = document.documentElement.clientHeight
				// 	if(width > height) {
				// 		this.dp.fullScreen.request()
				// 		// screenfull.toggle(this.$refs.mydplayer);
				// 	}
					
				// })
				
				var videoPageList = []
				for(var i=0;i<this.videoList.length;i++) {
					videoPageList.push(this.videoList[i].data)
				}
				var pageIndex = videoPageList.indexOf(this.thisVideoName)
				var Route = this.current.slice(0, -1).join('/')
				var Sorted = this.$route.query.Sorted;
				if(pageIndex < (this.videoList.length-1)){
					this.dp.on('ended', function() {
						location.href='/video?route=media/' + Route + '/' + videoPageList[pageIndex+1] + "&Sorted="+Sorted
					})
				}
				
				
			}
		},
		
		mounted() {
			const Route = this.$route.query.route;
			this.$store.commit('selectMenu', Route)
			let VideoNameList = Route.split('/')
			var VideoName = VideoNameList.slice(-1)[0]
			this.thisVideoName = VideoName;
			document.title = VideoName
			window.addEventListener("resize", this.renderResize, false)
			this.getVideoList(this.current.slice(0, -1).join('/'), Route)

			// var UserName = this.$cookies.get('UserName')
			// VideoNameList.splice(1,0,UserName)
			// var VideoPath = VideoNameList.join('/')
			
		}
	}
</script>


<style scoped src="../../static/css/VideoCss.css"></style>