// import axios from 'axios'
export default {

  state: {
    ifMenu: false,
	ifphoneMenu: false,
    currentMenu: [],
    current_Menu: [],
    filedata: {
      dir: [],
      file: []
    },
    menu: []
  },
  mutations: {
    selectMenu (state, val) {
      if (!val) {
        state.currentMenu = []
      } else {
        // console.log(val)
        state.currentMenu = val.split('/')
		if (state.currentMenu.includes('media')) {
			var i = state.currentMenu.indexOf('media')
			state.currentMenu.splice(i, 1)
		}
      }

      // val.name === 'Home' ? state.currentMenu = null : state.currentMenu = val
    },
    collapseMenu (State) {
		// State.ifCollapse = true
		// console.log(State.ifCollapse)
		State.ifMenu = !State.ifMenu

    },
	phoneMenu (State) {
		// State.ifCollapse = true
		// console.log(State.ifCollapse)
		State.ifphoneMenu = !State.ifphoneMenu
	
	}
  },

  actions: {}
}
