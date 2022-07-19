const utils = {
  namespaced: true,
  state: {
    status: {
      error: false,
      loading: false,
      timestamp: null,
    },
    message: {
      type: null,
      details: null,
      timestamp: null,
    },
    drawer: {
      width: 0,
    },
  },
  actions: {
    setStatus({ commit }, params) {
      commit('updateStatus', params);
    },
    setMessage({ commit }, params) {
      commit('updateMessage', params);
    },
    setDrawer({ commit }, params) {
      commit('updateDrawer', params);
    },
  },
  mutations: {
    updateStatus(state, { error, loading, timestamp }) {
      state.status.error = error;
      state.status.loading = loading;
      state.status.timestamp = timestamp;
    },
    updateMessage(state, { type, details, timestamp }) {
      state.message.type = type;
      state.message.details = details;
      state.message.timestamp = timestamp;
    },
    updateDrawer(state, { width }) {
      state.drawer.width = width;
    },
  },
};

export default utils;
