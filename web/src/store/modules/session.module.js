import axios from '@/plugins/axios';

const session = {
  namespaced: true,
  state: {
    data: [],
  },
  actions: {
    get({ commit, rootState }, params) {
      axios.get('/session/', {
        params,
        headers: {
          'Authorization': `Token ${rootState.user.token}`,
        },
      })
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

export default session;
