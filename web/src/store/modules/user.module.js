import axios from '@/plugins/axios';

const user = {
  namespaced: true,
  state: {
    data: {},
    token: null,
    isAnonymous: true,
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
        });
    },
    login({ commit, state }, params) {
      if (state.token) {
        axios.post('/auth/login/', params, {
          headers: {
            'Authorization': `Token ${state.token}`,
          },
        })
          .then(({ data }) => {
            commit('updateToken', data);
          });
      } else {
        axios.post('/auth/login/', params)
          .then(({ data }) => {
            commit('updateToken', data);
          });
      }
    },
    logout({ commit, state }) {
      axios.post('/auth/logout/', {
        headers: {
          'Authorization': `Token ${state.token}`,
        },
      })
        .then(() => {
          commit('updateData', {});
          commit('updateToken', {});
        });
    },
    register({ commit }, params) {
      axios.post('/auth/registration/', params)
        .then(({ data }) => {
          commit('updateToken', data);
        });
    },
    resetPassword({ state }, params) {
      axios.post('/auth/password/reset/', params, {
        headers: {
          'Authorization': `Token ${state.token}`,
        },
      });
    },
    resetPasswordConfirm({ state }, params) {
      axios.post('/auth/password/reset/confirm/', params, {
        headers: {
          'Authorization': `Token ${state.token}`,
        },
      });
    },
  },
  mutations: {
    updateToken(state, { key }) {
      state.token = key;
    },
    updateData(state, data) {
      state.data = data;
      state.isAnonymous = data.is_anonymous;
      delete state.data.is_anonymous;
    },
  },
};

export default user;
