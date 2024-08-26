import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import axiosInstance from './axios'

const app = createApp(App)

// backend connection
axios.defaults.baseURL = 'http://localhost:8000/api/'
app.config.globalProperties.$axios = axiosInstance

app.use(router)

app.mount('#app')