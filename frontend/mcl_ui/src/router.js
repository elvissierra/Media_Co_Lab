import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './components/HomePage.vue'
import UserLogin from './components/UserLogin.vue'
import Media from './components/Media.vue'
import Organization from './components/Organization.vue'
import Teams from '/components/Teams.vue'


const routes = [
  {
    path: '/', name: 'HomePage', component: HomePage,
  },
  {
    path: '/login', name: 'UserLogin', component: UserLogin, 
    beforeEnter: (to, from, next) => {
      if (localStorage.getItem('authToken')){
        next({ name: 'HomePage'})
      } else {
        next()
      }
    }
  },
  {
    path: '/organization', name: 'Organization', component: Organization,
  },
  {
    path: '/teams', name: 'Teams', component: Teams,
  },
  {
    path: '/media', name: 'Media', component: Media,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
