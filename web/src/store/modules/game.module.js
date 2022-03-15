import axios from '@/plugins/axios';

const game = {
  namespaced: true,
  state: {
    tags: [],
    entry: {},
    rounds: 5,
    roundId: 1,
    seconds: 0,
  },
  actions: {
    get({ commit, rootState, state }, params) {
      if (state.roundId !== state.rounds) {
        axios.get('/game/', {
          params,
          headers: {
            'Authorization': `Token ${rootState.user.token}`,
          },
        })
          .then(({ data }) => {
            commit('updateData', data);
          });
      }
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
    updateData(state, { round_id, rounds, gameround }) {
      state.roundId = round_id;
      state.rounds = rounds;
      state.entry = gameround;
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
