import axios from '@/plugins/axios';

const resource = {
  namespaced: true,
  state: {
    data: {},
  },
  actions: {
    get({ commit }, params) {
      axios.get('/resource', { params })
        .then(({ data }) => {
          commit('updateData', data);
        });
    },
    post({ commit }, params) {
      axios.post('/resource', params)
        .then(({ data }) => {
          commit('updateData', data);
        });
    },
  },
  mutations: {
    updateData(state, data) {
      state.data = data;
    },
  },
};

export default resource;
