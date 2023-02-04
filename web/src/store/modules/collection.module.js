import axios from '@/plugins/axios';

const collection = {
  namespaced: true,
  state: {
    data: {
      collections: [],
    },
  },
  actions: {
    post({ commit, rootState }, params) {
      axios.post('/collection/', { params }, {
        headers: {
          'Authorization': `Token ${rootState.user.token}`,
        },
      })
        .then(({ data }) => {
          commit('updateData', data);
        });
    },
    add({ rootState }, params) {
      const formData = new FormData();
      formData.append('name', params.name);
      params.files.forEach((file) => {
        formData.append('files', file);
      });
      axios.post('/collection/add/', formData, {
        headers: {
          'Authorization': `Token ${rootState.user.token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
    },
    remove({ rootState }, params) {
      axios.post('/collection/remove/', { params }, {
        headers: {
          'Authorization': `Token ${rootState.user.token}`,
        },
      });
    },
  },
  mutations: {
    updateData(state, data) {
      state.data.collections = data.collections;
    },
  },
};

export default collection;
