import axios from 'axios';
import store from '@/store';
import { API_LOCATION } from '@/../app.config';

const instance = axios.create({
  baseURL: API_LOCATION,
  withCredentials: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});

instance.interceptors.request.use((request) => {
  const status = { loading: true, error: false };
  store.dispatch('utils/setStatus', status, { root: true });
  return request;
});

instance.interceptors.response.use((response) => {
  const status = { loading: false, error: false };
  store.dispatch('utils/setStatus', status, { root: true });
  return response;
}, ({ response }) => {
  const status = { loading: false, error: true };
  store.dispatch('utils/setStatus', status, { root: true });
  const message = { type: 'error', timestamp: new Date() };
  message.detail = response.data.detail || 'unknown_error';
  console.log(message);
  if (message.detail !== 'not_authenticated') {
    store.dispatch('utils/setMessage', message, { root: true });
  }
  return new Promise(() => { });
});

export default instance;
