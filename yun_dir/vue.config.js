const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  css: {
    loaderOptions: {
      sass: {
        additionalData: '@import "./src/assets/scss/_variable.scss";'
      }
    }
  },
  devServer: {
    proxy: 'http://127.0.0.1:8000',
		},
	lintOnSave:false //关闭eslint检查
}
)
