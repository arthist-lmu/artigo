import axios from '@/plugins/axios';

const game = {
  namespaced: true,
  state: {
    tags: [],
    entry: {},
    rounds: 5,
    roundId: 1,
    sessionId: null,
    seconds: 0,
  },
  actions: {
    get({ commit, rootState, state }, params) {
      if (Object.keys(params).length === 0) {
        params = { session_id: state.sessionId };
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
    setSeconds({ commit }, seconds) {
      commit('updateSeconds', seconds);
    },
  },
  mutations: {
    updateData(state, {
      session_id, rounds, round_id, data,
    }) {
      state.sessionId = session_id;
      state.rounds = rounds;
      state.roundId = round_id;
      state.entry = data;
      state.tags = [];
    },
    updateTags(state, { tags }) {
      tags.forEach((tag) => {
        if (tag.valid) {
          state.tags.push(tag);
        }
      });
    },
    updateSeconds(state, seconds) {
      state.seconds = seconds;
    },
  },
};

export default game;
