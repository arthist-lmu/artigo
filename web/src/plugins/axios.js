import axios from 'axios'
import store from '@/store'
import useIsArray from '@/composables/useIsArray'

let baseURL = 'http://localhost:8000'
const { VITE_APP_API } = import.meta.env
if (VITE_APP_API) {
  baseURL = `https://${VITE_APP_API}`
}

const instance = axios.create({
  baseURL,
  withCredentials: true
})

instance.interceptors.request.use((request) => {
  const { params } = request.data || { params: {} }
  if (params === undefined || params.job_id === undefined) {
    const status = {
      loading: true,
      error: false,
      timestamp: null
    }
    store.dispatch('utils/setStatus', status, { root: true })
  }
  return request
})

instance.interceptors.response.use((response) => {
  if (response.data.job_id === undefined) {
    const status = {
      loading: false,
      error: false,
      timestamp: new Date()
    }
    store.dispatch('utils/setStatus', status, { root: true })
  }
  return response;
}, ({ response }) => {
  const status = {
    loading: false,
    error: true,
    timestamp: new Date()
  }
  store.dispatch('utils/setStatus', status, { root: true })
  const message = { type: 'error', timestamp: new Date() }
  if (response !== undefined) {
    Object.keys(response.data).forEach((field) => {
      let values = response.data[field]
      if (!useIsArray(values)) {
        values = [values]
      }
      message.details = values.map((value) => {
        value = value.replace(/\s/g, '_').replace(/\./g, '')
        return value.toLowerCase()
      })
    })
  }
  if (!message.details) {
    message.details = ['unknown_error']
  }
  store.dispatch('utils/setMessage', message, { root: true })
  return new Promise(() => { })
});

export default instance
