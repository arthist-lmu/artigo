import axios from '@/plugins/axios';

const statistics = {
  namespaced: true,
  state: {
    data: {},
    scores: {},
  },
  actions: {
    get({ commit }, params) {
      axios.get('/statistics/', { params })
        .then(({ data }) => {
          commit('updateData', data);
        });
    },
    scores({ commit }, params) {
      axios.get('/scores/', { params })
        .then(({ data }) => {
          commit('updateScores', data);
        });
    },
  },
  mutations: {
    updateData(state, data) {
      state.data = data;
    },
    updateScores(state, scores) {
      state.scores = scores;
    },
  },
};

export default statistics;
