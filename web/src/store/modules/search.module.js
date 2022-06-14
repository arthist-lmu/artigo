import axios from '@/plugins/axios';
import router from '@/router';
import mixins from '@/mixins';

const search = {
  namespaced: true,
  state: {
    data: {
      total: 0,
      offset: 0,
      entries: [],
      aggregations: [],
    },
    params: {},
    jobId: null,
    backBtn: false,
  },
  actions: {
    post({ commit, dispatch, state }, params) {
      if (mixins.methods.keyInObj('offset', params)) {
        params = { ...state.params, ...params };
      }
      commit('resetData', params);
      if (!params.sourceView) {
        if (!state.backBtn) {
          dispatch('setURLParams', params);
        } else {
          commit('toggleBackBtn');
        }
      }
      axios.post('/search/', { params })
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
      axios.post('/search/', { params })
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
            let values = params.query[field];
            if (values instanceof Set) {
              values = Array.from(values);
            }
            if (values instanceof Array) {
              urlParams.append(field, values.join(','));
            } else {
              urlParams.append(field, values);
            }
          });
        }
      }
      const query = Object.fromEntries(urlParams);
      router.push({ name: 'search', query });
    },
  },
  mutations: {
    resetData(state, params) {
      if (!router.currentRoute.path.endsWith('/search')) {
        state.data.total = 0;
        state.data.offset = 0;
        state.data.entries = [];
        state.data.aggregations = [];
      }
      state.params = params;
    },
    updateData(state, data) {
      state.data.total = data.total || 0;
      state.data.offset = data.offset || 0;
      state.data.entries = data.entries || [];
      state.data.aggregations = data.aggregations || [];
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
