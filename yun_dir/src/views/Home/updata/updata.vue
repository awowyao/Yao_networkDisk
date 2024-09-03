<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="upload" v-for="i in uploadList" :key="i">
        <!-- <input class="file" name="file" type="file" accept="*" @change="update($event,i)"/> -->
        <p>{{i.fileName}}</p>
        <!-- <p>test</p> -->
        <el-progress :text-inside="true" :stroke-width="20" :percentage="i.fileUploadPercent" />
        <div class="status">
          <span v-if="i.fileSpeed != ''">速度：{{i.fileSpeed}}</span><span v-if="i.fileTime != ''">剩下时间:{{i.fileTime}}</span>
        </div>

        <!-- <div>{{item.fileUploadPercent}}</div> -->
        <!-- <Progress text-inside :percent="item.fileUploadPercent" /> -->
    </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
export default {
  data () {
    return {
      list: [{ fileUploadPercent: 0 }, { fileUploadPercent: 0 }, { fileUploadPercent: 0 }, { fileUploadPercent: 0 }, { fileUploadPercent: 0 }]
    }
  },
  computed: {
    ...mapState({
      uploadList: state => state.upload.uploadData,
			
    })
  },
  methods: {
    update (e, item) {
      const file = e.target.files[0]
      const param = new FormData() // 创建form对象y
      param.append('file', file)// 通过append向form对象添加数据
      console.log(param.get('file')) // FormData私有类对象，访问不到，可以通过get判断值是否传进去
      const config = {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.lengthComputable) { // 是否存在进度
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            // this.progressBar = percentCompleted

            item.fileUploadPercent = percentCompleted
            console.log('进度：', item.fileUploadPercent)
            this.$forceUpdate()
          }
        }

      }
      axios.post('/nas/upload', param, config)
        .then(response => {
          console.log(response.data)
        })
    }
  }
}
</script>

<style lang="scss" scoped>
.status{

    display: flex;
    height: 100%;
    align-items: center;
    justify-content: space-between;
}
.upload{
  margin-bottom: 20px;
}
</style>
