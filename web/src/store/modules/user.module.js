import axios from '@/plugins/axios';

const user = {
  namespaced: true,
  state: {
    data: {},
    loggedIn: false,
  },
  actions: {
    get({ commit }, params) {
      axios.get('/rest-auth/user/', params)
        .then(({ data }) => {
          commit('updateData', data);
          commit('updateLoggedIn', true);
        });
    },
    login({ commit }, params) {
      axios.post('/rest-auth/login/', params)
        .then(({ data }) => {
          commit('updateData', data);
          commit('updateLoggedIn', true);
        });
    },
    logout({ commit, state }) {
      const params = state.userData;
      axios.post('/rest-auth/logout/', params)
        .then(() => {
          commit('updateData', {});
          commit('updateLoggedIn', false);
        });
    },
    register({ commit }, params) {
      axios.post('/rest-auth/registration/', params)
        .then(({ data }) => {
          commit('updateData', data);
          commit('updateLoggedIn', true);
        });
    },
  },
  mutations: {
    updateCSRFToken(state, token) {
      state.csrfToken = token;
    },
    updateLoggedIn(state, loggedIn) {
      state.loggedIn = loggedIn;
    },
    updateData(state, data) {
      state.data = data;
    },
  },
};

export default user;
