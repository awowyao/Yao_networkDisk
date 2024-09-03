import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import '@/assets/scss/reset.scss'
import VueCookies from "vue-cookies";
// elementPlus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'


// VueDPlayer
// import VueDPlayer from 'vue-dplayer'
// import 'vue-dplayer/dist/vue-dplayer.css'

const app = createApp(App)
app.use(store).use(router)
app.use(ElementPlus)
app.use(VueCookies);

// app.use(VueDPlayer)
// app.prototype.$http = http

// app.config.productionTip = false
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')
