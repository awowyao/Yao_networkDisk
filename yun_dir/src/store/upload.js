
import axios from 'axios'
export default {

  state: {
    uploadData: []
  },
  mutations: {
    uploadData (state, e) {
      const fileAd = e[1]
	  const token = e[2]
      const dataDic = {
        fileUploadPercent: 0,
        fileName: e[0].name,
        fileTime: '',
        fileSpeed: ''
      }
      state.uploadData.push(dataDic)
      const ListNub = state.uploadData.length - 1
      //   console.log(state.uploadData)
      //   this.upload(file, dataDic)
      //   console.log(e)
      const file = e[0]
      const param = new FormData() // 创建form对象y
      param.append('file', file)// 通过append向form对象添加数据
      param.append('route', fileAd)// 通过append向form对象添加数据
       // FormData私有类对象，访问不到，可以通过get判断值是否传进去
      let lastTime = 0
      //   const lastSize = progressEvent.loaded
      let lastSize = 0
			
      const config = {
        headers: { 'Content-Type': 'multipart/form-data',
								'token': token},
        onUploadProgress: (progressEvent) => {
          if (progressEvent.lengthComputable) { // 是否存在进度
            let percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            if (lastTime === 0) {
              lastTime = new Date().getTime()
              lastSize = progressEvent.loaded
            }

            /* 计算间隔 */
            const nowTime = new Date().getTime()
            const intervalTime = (nowTime - lastTime) / 1000// 时间单位为毫秒，需转化为秒
            const intervalSize = progressEvent.loaded - lastSize
            /* 重新赋值以便于下次计算 */
            lastTime = nowTime
            lastSize = progressEvent.loaded

            // 计算速度
            let speed = intervalSize / intervalTime
            const bSpeed = speed// 保存以b/s为单位的速度值，方便计算剩余时间
            let units = 'b/s'// 单位名称
            if (speed / 1024 > 1) {
              speed = speed / 1024
              units = 'k/s'
            }
            if (speed / 1024 > 1) {
              speed = speed / 1024
              units = 'M/s'
            }
            /* 计算剩余时间 */
            const leftTime = ((progressEvent.total - progressEvent.loaded) / bSpeed)

            lastTime = nowTime
            lastSize = progressEvent.loaded
            state.uploadData[ListNub].fileSpeed = speed.toFixed(1) + units
            state.uploadData[ListNub].fileTime = leftTime.toFixed(1)
            if (percentCompleted === 100) {
              percentCompleted = 99
            }
            state.uploadData[ListNub].fileUploadPercent = percentCompleted
            // console.log('进度：', state.uploadData[ListNub].fileUploadPercent)
            // this.$forceUpdate()
          }
        }

      }
      axios.post('/nas/upload', param, config)
        .then(response => {
          console.log(response.data)
          state.uploadData[ListNub].fileUploadPercent = 100
        })
    },
    Getpush (state, file) {
      const dataDic = {
        fileUploadPercent: 0,
        fileName: '',

        fileTime: '',
        fileSpeed: ''
      }
      state.uploadData.push(dataDic)
      const ListNub = state.uploadData.length - 1

      this.uploadData(file, state.uploadData[ListNub])
    //   console.log(state.uploadData.length)
    }

  },

  actions: {}
}
