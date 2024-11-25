import axios from 'axios';
import router from './router'; // Adjust the path to your router file

// Create an Axios instance
const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_URL,
});

// Request interceptor to add the Authorization header
axiosInstance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Response interceptor to handle 401 Unauthorized
axiosInstance.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // If 401 Unauthorized, log out the user
      localStorage.removeItem('authToken');
      router.push({ name: 'UserLogin' });  // Redirect to the login page
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;