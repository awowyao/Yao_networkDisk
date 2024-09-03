<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div id="select_frame">
    <div ref="select_frame" class="box">将文件拖拽到这里</div>
    <div class="filebox">
      <p v-if="fileList.length < 1">暂无文件</p>
      <ol>
        <li v-for="item in fileList" :key="item">{{ item.name }}</li>
      </ol>
    </div>
    <button style="outline:none;float:right;"  type="submit" class="btn btn-primary">解 析</button>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'patchCheck',
  data () {
    return {
      infoshow: false,
      fileList: []
    }
  },
  computed: {
    ...mapState({
      uploadList: state => state.upload
    })
  },
  mtehods: {},
  // components: {

  //   layout: Layout
  // },
  mounted () {
    this.$refs.select_frame.ondragleave = (e) => {
      e.preventDefault() // 阻止离开时的浏览器默认行为
    }
    this.$refs.select_frame.ondrop = (e) => {
      e.preventDefault() // 阻止拖放后的浏览器默认行为
      const data = e.dataTransfer.files // 获取文件对象
      if (data.length < 1) {
        return // 检测是否有文件拖拽到页面
      }
      // console.log(e.dataTransfer.files[0].name)
      // this.$store.commit('Getpush', e.dataTransfer.files[0])

      this.$store.commit('uploadData', e.dataTransfer.files[0])
      // const formData = new FormData()
    }
    this.$refs.select_frame.ondragenter = (e) => {
      e.preventDefault() // 阻止拖入时的浏览器默认行为
      this.$refs.select_frame.border = '2px dashed red'
    }
    this.$refs.select_frame.ondragover = (e) => {
      e.preventDefault() // 阻止拖来拖去的浏览器默认行为
    }
  }
}
</script>

<style lang="scss" scoped>
#select_frame{
  width: 100%;
  height: 100%;
}
.box{
  width: 100%;
  height: 100%;
}
</style>
