import axios from '@/plugins/axios';
import { API_LOCATION } from '@/../app.config';

const resource = {
  namespaced: true,
  state: {
    data: {},
  },
  actions: {
    get({ commit }, params) {
      axios.get(`${API_LOCATION}/get_resource`, { params })
        .then(({ data }) => {
          commit('updateData', data);
        })
        .catch(({ response }) => {
          console.log('Error', response.data);
        });
    },
    post({ commit }, params) {
      axios.post(`${API_LOCATION}/get_resource`, params)
        .then(({ data }) => {
          commit('updateData', data);
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
export default resource;
