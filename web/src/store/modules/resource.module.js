import axios from '@/plugins/axios';
import { API_LOCATION } from '@/../app.config';

const resource = {
  namespaced: true,
  state: {
    data: {},
  },
  actions: {
    get({ commit }, params) {
      axios.post(`${API_LOCATION}/get_resource`, { params })
        .then((res) => {
          if (res.data.status === 'ok') {
            commit('updateData', res.data.data);
            console.log('resource', res.data.data);
          }
        })
        .catch((error) => {
          console.log(error);
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
