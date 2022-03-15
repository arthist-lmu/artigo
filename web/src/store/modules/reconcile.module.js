import axios from '@/plugins/axios';
import i18n from '@/plugins/i18n';

const reconcile = {
  namespaced: true,
  state: {
    data: {
      reconciliations: [],
    },
  },
  actions: {
    post({ commit, rootState }, params) {
      params = { lang: i18n.locale, ...params };
      axios.post('/reconcile/', { params }, {
        headers: {
          'Authorization': `Token ${rootState.user.token}`,
        },
      })
        .then(({ data }) => {
          commit('updateData', data);
        });
    },
    add({ rootState }, params) {
      axios.post('/reconcile/add/', { params }, {
        headers: {
          'Authorization': `Token ${rootState.user.token}`,
        },
      });
    },
    remove({ rootState }, params) {
      axios.post('/reconcile/remove/', { params }, {
        headers: {
          'Authorization': `Token ${rootState.user.token}`,
        },
      });
    },
  },
  mutations: {
    updateData(state, data) {
      state.data.reconciliations = data.reconciliations;
    },
  },
};

export default reconcile;
