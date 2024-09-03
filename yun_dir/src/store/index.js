// import Vue from 'vue'
// import Vuex from 'vuex'

// Vue.use(Vuex)
// export default new Vuex.Store({
//   modeiles: {
//     tab
//   }
// })
import { createStore } from 'vuex'
import tab from './tab'
import upload from './upload'
// Vue.use(createStore)
export default createStore({
  state: {
    // upload: []
  },
  getters: {
  },
  mutations: {

  },
  actions: {
  },
  modules: {
    upload,
    tab

  }
})
