import axios from '@/plugins/axios';

const collections = {
  namespaced: true,
  state: {
    data: {
      total: 0,
      offset: 0,
      entries: [],
    },
    itemsPerPage: 96,
  },
  actions: {
    get({ commit, rootState, state }, params) {
      params.limit = state.itemsPerPage;
      axios.get('/collections/', {
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
    updateData(state, { total, offset, entries }) {
      state.data.total = total;
      state.data.offset = offset;
      state.data.entries = entries;
    },
  },
};

export default collections;
