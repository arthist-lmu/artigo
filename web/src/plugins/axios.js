import axios from 'axios';
import store from '@/store';
import mixins from '@/mixins';
import { API_LOCATION } from '@/../app.config';

const instance = axios.create({
  baseURL: API_LOCATION,
  withCredentials: true,
});

instance.interceptors.request.use((request) => {
  const status = { loading: true, error: false, timestamp: null };
  store.dispatch('utils/setStatus', status, { root: true });
  return request;
});

instance.interceptors.response.use((response) => {
  const status = { loading: false, error: false, timestamp: new Date() };
  store.dispatch('utils/setStatus', status, { root: true });
  return response;
}, ({ response }) => {
  const status = { loading: false, error: true, timestamp: new Date() };
  store.dispatch('utils/setStatus', status, { root: true });
  const message = { type: 'error', timestamp: new Date() };
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
  if (!message.details) {
    message.details = ['unknown_error'];
  }
  console.log(message);
  store.dispatch('utils/setMessage', message, { root: true });
  return new Promise(() => { });
});

export default instance;
