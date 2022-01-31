import axios from '@/plugins/axios';

const api = {
  namespaced: true,
  state: {
    data: {},
    jobId: null,
  },
  actions: {
    search({ commit, dispatch }, params) {
      axios.post('/search', { params })
        .then(({ data }) => {
          if (data.job_id !== undefined) {
            commit('updateJobId', data.job_id);
            setTimeout(() => dispatch('checkSearch'), 500);
          } else {
            commit('updateData', data);
          }
        });
    },
    checkSearch({ commit, dispatch, state }) {
      const params = { job_id: state.jobId };

      axios.post('/search', { params })
        .then(({ data }) => {
          if (data.job_id !== undefined) {
            commit('updateJobId', data.job_id);
            setTimeout(() => dispatch('checkSearch'), 500);
          } else {
            commit('updateData', data);
          }
        });
    },
  },
  mutations: {
    updateData(state, data) {
      state.data = data;
    },
    updateJobId(state, jobId) {
      state.jobId = jobId;
    },
  },
};
export default api;
