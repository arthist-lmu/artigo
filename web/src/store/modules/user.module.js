import axios from '@/plugins/axios';

const user = {
  namespaced: true,
  state: {
    data: {},
    token: null,
    loggedIn: false,
  },
  actions: {
    get({ commit, state }) {
      axios.get('/auth/user/', {
        headers: {
          'Authorization': `Token ${state.token}`,
        },
      })
        .then(({ data }) => {
          commit('updateData', data);
          commit('updateLoggedIn', true);
        });
    },
    login({ dispatch, commit }, params) {
      axios.post('/auth/login/', params)
        .then(({ data }) => {
          commit('updateToken', data);
          commit('updateLoggedIn', true);
          dispatch('get');
        });
    },
    logout({ commit, state }) {
      axios.get('/auth/logout/', {
        headers: {
          'Authorization': `Token ${state.token}`,
        },
      })
        .then(() => {
          commit('updateData', {});
          commit('updateToken', {});
          commit('updateLoggedIn', false);
        });
    },
    register(context, params) {
      axios.post('/auth/registration/', params);
    },
  },
  mutations: {
    updateLoggedIn(state, loggedIn) {
      state.loggedIn = loggedIn;
    },
    updateToken(state, { key }) {
      state.token = key;
    },
    updateData(state, data) {
      state.data = data;
    },
  },
};

export default user;
