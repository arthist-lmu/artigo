import axios from '@/plugins/axios';
import router from '@/router';

const search = {
  namespaced: true,
  state: {
    data: {},
    jobId: null,
    backBtn: false,
  },
  actions: {
    post({ commit, dispatch, state }, params) {
      if (!params.sourceView) {
        if (!state.backBtn) {
          dispatch('setURLParams', params);
        } else {
          commit('toggleBackBtn');
        }
      }
      axios.post('/search', { params })
        .then(({ data }) => {
          if (data.job_id !== undefined) {
            commit('updateJobId', data.job_id);
            setTimeout(() => dispatch('checkPost'), 500);
          } else {
            commit('updateData', data);
          }
        });
    },
    checkPost({ commit, dispatch, state }) {
      const params = { job_id: state.jobId };
      axios.post('/search', { params })
        .then(({ data }) => {
          if (data.job_id !== undefined) {
            commit('updateJobId', data.job_id);
            setTimeout(() => dispatch('checkPost'), 500);
          } else {
            commit('updateData', data);
          }
        });
    },
    getURLParams({ dispatch }, urlParams) {
      const query = {};
      Object.keys(urlParams).forEach((field) => {
        query[field] = urlParams[field].split(',');
      });
      dispatch('post', { query });
    },
    setURLParams(context, params) {
      const urlParams = new URLSearchParams();
      if (params.query) {
        if (typeof params.query === 'string') {
          urlParams.append('all-text', params.query);
        } else if (params.query instanceof Object) {
          Object.keys(params.query).forEach((field) => {
            if (params[field] instanceof Array) {
              urlParams.append(field, params.query[field].join(','));
            } else {
              urlParams.append(field, params.query[field]);
            }
          });
        }
      }
      if (router.currentRoute.path.endsWith('/search')) {
        const href = `?${urlParams.toString()}`;
        window.history.pushState({}, null, href);
      } else {
        const query = Object.fromEntries(urlParams);
        router.push({ name: 'search', query });
      }
    },
  },
  mutations: {
    updateData(state, data) {
      state.data = data;
    },
    updateJobId(state, jobId) {
      state.jobId = jobId;
    },
    toggleBackBtn(state) {
      state.backBtn = !state.backBtn;
    },
  },
};
export default search;
