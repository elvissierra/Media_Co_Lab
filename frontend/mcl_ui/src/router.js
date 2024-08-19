import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import UserLogin from './components/UserLogin.vue';

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/login',
    name: 'UserLogin',
    component: UserLogin,
    beforeEnter: (to, from, next) => {
      if (localStorage.getItem('authToken')){
        next({ name: 'HomePage'})
      } else {
        next()
      }
    }
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
