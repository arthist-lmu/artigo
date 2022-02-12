const utils = {
  namespaced: true,
  state: {
    status: {
      loading: false,
      error: false,
    },
    message: {
      type: null,
      detail: null,
      timestamp: null,
    },
  },
  actions: {
    setStatus({ commit }, params) {
      commit('updateStatus', params);
    },
    setMessage({ commit }, params) {
      commit('updateMessage', params);
    },
  },
  mutations: {
    updateStatus(state, { loading, error }) {
      state.status.loading = loading;
      state.status.error = error;
    },
    updateMessage(state, { type, detail, timestamp }) {
      state.message.type = type;
      state.message.detail = detail;
      state.message.timestamp = timestamp;
    },
  },
};

export default utils;
