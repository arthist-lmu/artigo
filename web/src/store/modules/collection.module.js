import axios from '@/plugins/axios';
import { API_LOCATION } from '@/../app.config';

const collection = {
  namespaced: true,
  state: {
    data: {},
  },
  actions: {
    get({ commit }, params) {
      axios.get(`${API_LOCATION}/get_collection`, { params })
        .then(({ data }) => {
          commit('updateData', data);
          console.log('collection', data);
        })
        .catch(({ response }) => {
          console.log('Error', response.data);
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
