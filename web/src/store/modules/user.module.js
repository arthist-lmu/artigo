import axios from '@/plugins/axios';
import { API_LOCATION } from '@/../app.config';

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
      axios.get(`${API_LOCATION}/get_csrf_token`, {
        params, withCredentials: true,
      })
        .then(() => {
          const csrftoken = getCookie('csrftoken');
          if (state.csrfToken !== csrftoken) {
            commit('updateCSRFToken', csrftoken);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    get({ commit }, params) {
      axios.post(`${API_LOCATION}/get_user`, { params })
        .then((res) => {
          if (res.data.status === 'ok') {
            commit('updateData', res.data.data);
            commit('updateLoggedIn', true);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    login({ commit }, params) {
      axios.post(`${API_LOCATION}/login`, { params })
        .then((res) => {
          if (res.data.status === 'ok') {
            commit('updateData', res.data.data);
            commit('updateLoggedIn', true);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    logout({ commit, state }) {
      const params = state.userData;
      axios.post(`${API_LOCATION}/logout`, { params })
        .then((res) => {
          if (res.data.status === 'ok') {
            commit('updateData', {});
            commit('updateLoggedIn', false);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    register({ commit }, params) {
      axios.post(`${API_LOCATION}/register`, { params })
        .then((res) => {
          if (res.data.status === 'ok') {
            commit('updateData', res.data.data);
            commit('updateLoggedIn', true);
          }
        })
        .catch((error) => {
          console.log(error);
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
