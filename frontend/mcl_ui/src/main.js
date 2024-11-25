import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import axiosInstance from './axios'
import vuetify from './plugins/vuetify'
import store from './store'

const app = createApp(App)

// base backend endpoint
axios.defaults.baseURL = process.env.VUE_APP_URL;
app.config.globalProperties.$axios = axiosInstance

app.use(vuetify)
app.use(router)
app.use(store)

app.mount('#app')