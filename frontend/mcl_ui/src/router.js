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
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
