import axios from '@/plugins/axios';

const collection = {
  namespaced: true,
  actions: {
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
    change({ rootState }, params) {
      axios.post('/collection/change/', { params }, {
        headers: {
          'Authorization': `Token ${rootState.user.token}`,
        },
      });
    },
  },
};

export default collection;
