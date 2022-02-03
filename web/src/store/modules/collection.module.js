import axios from '@/plugins/axios';

const collection = {
  namespaced: true,
  state: {
    data: {},
  },
  actions: {
    get({ commit }, params) {
      axios.get('/collection', { params })
        .then(({ data }) => {
          commit('updateData', data);
          console.log('collection', data);
        });
    },
  },
  mutations: {
    updateData(state, data) {
      state.data = data;
    },
  },
};
export default collection;
