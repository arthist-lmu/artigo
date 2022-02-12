import axios from '@/plugins/axios';

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').every((cookie) => {
      if (cookie.trim().substring(0, name.length + 1) === `${name}=`) {
        cookieValue = cookie.trim().substring(name.length + 1);
        cookieValue = decodeURIComponent(cookieValue);
        return false;
      }
      return true;
    });
  }
  return cookieValue;
}
const user = {
  namespaced: true,
  state: {
    csrfToken: getCookie('csrftoken'),
    loggedIn: false,
    data: {},
  },
  actions: {
    getCSRFToken({ commit, state }, params) {
      axios.get('/get_csrf_token', {
        params, withCredentials: true,
      })
        .then(() => {
          const csrftoken = getCookie('csrftoken');
          if (state.csrfToken !== csrftoken) {
            commit('updateCSRFToken', csrftoken);
            console.log(`set token: ${csrftoken}`);
          }
        });
    },
    get({ commit }, params) {
      axios.get('/rest-auth/user', { params })
        .then(({ data }) => {
          commit('updateData', data);
          commit('updateLoggedIn', true);
        });
    },
    login({ commit }, params) {
      axios.post('/rest-auth/login', params)
        .then(({ data }) => {
          commit('updateData', data);
          commit('updateLoggedIn', true);
        });
    },
    logout({ commit, state }) {
      const params = state.userData;
      axios.post('/rest-auth/logout', { params })
        .then(() => {
          commit('updateData', {});
          commit('updateLoggedIn', false);
        });
    },
    register({ commit }, params) {
      axios.post('/rest-auth/registration', params)
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
