const settings = {
  namespaced: true,
  state: {
    display: {
      tags: true,
      metadata: true
    }
  },
  actions: {
    setDisplay({ commit }, params) {
      commit('updateDisplay', params)
    }
  },
  mutations: {
    updateDisplay(state, { type, value }) {
      state.display[type] = value
    }
  }
}

export default settings
