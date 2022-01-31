import axios from 'axios';
import i18n from '@/plugins/i18n';
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
  const message = { type: 'error', timestamp: new Date() };
  if (response.data.detail == null) {
    message.detail = i18n.t('error.general');
  } else {
    message.detail = response.data.detail;
  }
  store.dispatch('utils/setStatus', status, { root: true });
  store.dispatch('utils/setMessage', message, { root: true });
  return response.data;
});
export default instance;
