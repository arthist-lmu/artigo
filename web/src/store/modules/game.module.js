import axios from '@/plugins/axios';

const game = {
  namespaced: true,
  state: {
    params: {},
    dialog: {
      params: {},
    },
    input: {
      focus: false,
    },
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
    getURLParams({ commit }, urlParams) {
      const params = {};
      Object.keys(urlParams).forEach((field) => {
        let values = urlParams[field];
        if (values.includes(',')) {
          values = values.split(',');
        } else if (parseFloat(values)) {
          values = parseFloat(values);
        }
        params[field] = values;
      });
      if (params && Object.keys(params).length) {
        commit('updateDialog', { params });
      }
    },
  },
  mutations: {
    updateParams(state, params) {
      state.params = params;
    },
    updateDialog(state, { params }) {
      state.dialog.params = params;
    },
    updateInput(state, { focus }) {
      state.input.focus = focus;
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
