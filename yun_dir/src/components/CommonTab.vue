<template>
  <div>
    <el-tag
      v-for="tag in dynamicTags"
      :key="tag"
      class="mx-1"
      closable
      :disable-transitions="false"
      @close="handleClose(tag)"
    >
      {{ tag }}
    </el-tag>
  </div>
</template>

<script>
export default {}

</script>

<style lang="scss" scoped>
</style>
