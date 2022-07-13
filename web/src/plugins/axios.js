import axios from 'axios';
import store from '@/store';
import mixins from '@/mixins';

let baseURL = 'http://localhost:8000';
const { VUE_APP_API } = process.env;
if (VUE_APP_API) {
  baseURL = `https://${VUE_APP_API}`;
}

const instance = axios.create({
  baseURL,
  withCredentials: true,
});

instance.interceptors.request.use((request) => {
  const { params } = request.data || { params: {} };
  if (params === undefined || params.job_id === undefined) {
    const status = { loading: true, error: false, timestamp: null };
    store.dispatch('utils/setStatus', status, { root: true });
  }
  return request;
});

instance.interceptors.response.use((response) => {
  if (response.data.job_id === undefined) {
    const status = { loading: false, error: false, timestamp: new Date() };
    store.dispatch('utils/setStatus', status, { root: true });
  }
  return response;
}, ({ response }) => {
  const status = { loading: false, error: true, timestamp: new Date() };
  store.dispatch('utils/setStatus', status, { root: true });
  const message = { type: 'error', timestamp: new Date() };
  if (response !== undefined) {
    Object.keys(response.data).forEach((field) => {
      let values = response.data[field];
      if (!mixins.methods.isArray(values)) {
        values = [values];
      }
      message.details = values.map((value) => {
        value = value.replace(/\s/g, '_').replace(/\./g, '');
        return value.toLowerCase();
      });
    });
  }
  if (!message.details) {
    message.details = ['unknown_error'];
  }
  store.dispatch('utils/setMessage', message, { root: true });
  return new Promise(() => { });
});

export default instance;
