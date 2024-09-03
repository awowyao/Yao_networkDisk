<!-- eslint-disable vue/multi-word-component-names -->
<template >
    <el-container style="width: 100vw;height:100vh;" @click="closeRightMenu">
        <el-aside width="auto"><common-aside></common-aside></el-aside>
        <el-container>
            <el-header><common-header></common-header></el-header>
            <!-- <common-Tab></common-Tab> -->
            <el-main allowfullscreen="true"><router-view ></router-view></el-main>
        </el-container>
    </el-container>
</template>

<script>
import CommonHeader from '../components/CommonHeader.vue'
import CommonAside from '../components/CommonAside.vue'
// import CommonTab from '../components/CommonTab.vue'

export default {
  components: {
    CommonHeader,
    CommonAside
    // CommonTab
  },
  methods: {
	  closeRightMenu() {
	  	var obj = document.getElementById("menu");
		if (obj) {
			obj.style.cssText = "display:none;";
		}
	  	
	  }
  }
}

</script>

<style lang="scss" scoped>
.el-header {
    background-color: #545c64;
}
</style>
