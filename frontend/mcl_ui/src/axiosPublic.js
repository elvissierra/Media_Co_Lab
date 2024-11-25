import axios from 'axios';

const axiosPublic = axios.create({
  baseURL: process.env.VUE_APP_URL,  //API base path
});

export default axiosPublic;