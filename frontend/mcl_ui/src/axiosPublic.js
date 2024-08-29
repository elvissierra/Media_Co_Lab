import axios from 'axios';

const axiosPublic = axios.create({
  baseURL: 'http://localhost:8000/api/',  // Replace with your API base URL
});

export default axiosPublic;
