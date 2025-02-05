import axios from 'axios';
import store from './store';

const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_URL,
});

axiosInstance.interceptors.request.use(
  config => {
    const token = store.state.authToken;
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

axiosInstance.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Remove token via the store
      store.commit('setAuthToken', null);
      import('./router').then(({ default: router }) => {
        router.push({ name: 'UserLogin' });
      });
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
