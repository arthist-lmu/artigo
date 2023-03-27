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
    itemsPerPage: 48,
  },
  actions: {
    post({ commit, dispatch, state }, params) {
      if (mixins.methods.keyInObj('offset', params)) {
        params = { ...state.params, ...params };
      }
      params.limit = state.itemsPerPage;
      if (params.aggregate === undefined) {
        params.aggregate = { fields: ['tags'] };
      }
      commit('resetData', params);
      if (!params.external) {
        if (!state.backBtn) {
          dispatch('setURLParams', params);
        } else {
          commit('toggleBackBtn');
        }
      }
      axios.post('/search/', params)
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
      axios.post('/search/', params)
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
      Object.entries(urlParams).forEach(([key, values]) => {
        if (['true', 'false'].includes(values)) {
          query[key] = values === 'true';
        } else {
          query[key] = urlParams[key].split(',');
        }
      });
      dispatch('post', { query });
    },
    setURLParams(context, params) {
      const urlParams = new URLSearchParams();
      if (params.query) {
        if (typeof params.query === 'string') {
          urlParams.append('all-text', params.query);
        } else if (params.query instanceof Object) {
          Object.entries(params.query).forEach(([key, values]) => {
            if (values instanceof Set) {
              values = Array.from(values);
            }
            if (values instanceof Array) {
              values = values.join(',');
            }
            urlParams.append(key, values);
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
    updateData(state, {
      total, offset, entries, aggregations,
    }) {
      state.data.total = total;
      state.data.offset = offset;
      state.data.entries = entries;
      state.data.aggregations = aggregations;
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
