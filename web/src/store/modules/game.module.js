import axios from '@/plugins/axios';

const game = {
  namespaced: true,
  state: {
    params: {},
    dialog: false,
    tags: [],
    entry: {},
    rounds: 5,
    roundId: 1,
    sessionId: null,
  },
  actions: {
    get({ commit, rootState, state }, params) {
      if (Object.keys(params).length === 0) {
        params = { session_id: state.sessionId };
      } else {
        commit('updateParams', params);
      }
      axios.get('/game/', {
        params,
        headers: {
          'Authorization': `Token ${rootState.user.token}`,
        },
      })
        .then(({ data }) => {
          commit('updateData', data);
        });
    },
    post({ commit, rootState }, params) {
      axios.post('/game/', { params }, {
        headers: {
          'Authorization': `Token ${rootState.user.token}`,
        },
      })
        .then(({ data }) => {
          commit('updateTags', data);
        });
    },
  },
  mutations: {
    updateParams(state, params) {
      state.params = params;
    },
    updateDialog(state, dialog) {
      state.dialog = dialog;
    },
    updateData(state, {
      session_id, rounds, round_id, data,
    }) {
      state.tags = [];
      state.entry = data;
      state.rounds = rounds;
      state.roundId = round_id;
      state.sessionId = session_id;
    },
    updateTags(state, { tags }) {
      tags.forEach((tag) => {
        state.tags.push(tag);
      });
    },
  },
};

export default game;
