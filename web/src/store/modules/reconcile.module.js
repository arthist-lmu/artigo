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
    post({ commit }, params) {
      params = { lang: i18n.locale, ...params };
      axios.post('/reconcile/', { params })
        .then(({ data }) => {
          commit('updateData', data);
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
