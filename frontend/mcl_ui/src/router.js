import { createRouter, createWebHistory } from 'vue-router'
import Page from './components/Page.vue'
import Home from './components/Home.vue'
import Organization from './components/Organization.vue'
import UserRegister from './components/UserRegister.vue'
import UserLogin from './components/UserLogin.vue'
import Teams from './components/Teams.vue'
import TeamDetail from './components/TeamDetail.vue'
import Media from './components/Media.vue'
import MediaDetail from './components/MediaDetail.vue'
import Labels from './components/Labels.vue'

// Define all components
// team users can create media and labels to team.medias
// need to be part of team to add objs
// media objs can be voted on and labels placed for urgency/priority
// comments can be added to media objs == discussions to determine engangement
// Uses: social media platforms, news, blog, etc. similar to bulletin boards

const routes = [
  {
    path: '/', name: 'Page', component: Page,
  },
  {
    path: '/home', name: 'Home', component: Home,
  },
  {
    path: '/register', name: 'UserRegister', component: UserRegister,
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
    path: '/organization', name: 'mclOrganization', component: Organization,
  },
  {
    path: '/teams', name: 'mclTeams', component: Teams,
  },
  {
    path: '/teams/:uuid', name: 'TeamDetail', component: TeamDetail,
  },
  {
    path: '/media', name: 'mclMedia', component: Media,
  },
  {
    path: '/media/:uuid', name: 'MediaDetail', component: MediaDetail,
  },
  {
    path: '/labels', name: 'mclLabels', component: Labels,
  },
];
// connected to base backend
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
