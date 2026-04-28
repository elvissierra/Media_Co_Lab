import { createRouter, createWebHistory } from 'vue-router'

import HomePage from './components/HomePage.vue'
import Organization from './components/Organization.vue'
import OrgRegister from './components/OrgRegister.vue'
import DemoOrganization from './components/DemoOrganization.vue'
import UserRegister from './components/UserRegister.vue'
import UserLogin from './components/UserLogin.vue'
import Teams from './components/Teams.vue'
import TeamCreate from './components/TeamCreate.vue'
import TeamDetail from './components/TeamDetail.vue'
import Media from './components/Media.vue'
import MediaDetail from './components/MediaDetail.vue'
import Labels from './components/Labels.vue'

const requireAuth = (_to, _from, next) => {
  if (!localStorage.getItem('authToken')) {
    next({ name: 'UserLogin' });
  } else {
    next();
  }
};

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/register',
    name: 'UserRegister',
    component: UserRegister,
  },
  {
    path: '/login',
    name: 'UserLogin',
    component: UserLogin,
    beforeEnter: (_to, _from, next) => {
      if (localStorage.getItem('authToken')) {
        next({ name: 'HomePage' });
      } else {
        next();
      }
    }
  },
  {
    path: '/organization',
    name: 'mclOrganization',
    component: Organization,
    beforeEnter: requireAuth,
  },
  {
    path: '/organizations/reg',
    name: 'RegisterOrganization',
    component: OrgRegister,
    beforeEnter: requireAuth,
  },
  {
    path: '/organizations/ov',
    name: 'OrganizationOverview',
    component: Organization,
    beforeEnter: requireAuth,
  },
  {
    path: '/organizations/demo',
    name: 'DemoOrganization',
    component: DemoOrganization,
    beforeEnter: requireAuth,
  },
  {
    path: '/team/create',
    name: 'mclTeam',
    component: TeamCreate,
    beforeEnter: requireAuth,
  },
  {
    path: '/teams',
    name: 'mclTeams',
    component: Teams,
    beforeEnter: requireAuth,
  },
  {
    path: '/teams/:team_id',
    name: 'TeamDetail',
    component: TeamDetail,
    beforeEnter: requireAuth,
  },
  {
    path: '/medias',
    name: 'mclMedia',
    component: Media,
    beforeEnter: requireAuth,
  },
  {
    path: '/medias/:medias_id',
    name: 'MediaDetail',
    component: MediaDetail,
    beforeEnter: requireAuth,
  },
  {
    path: '/labels',
    name: 'mclLabels',
    component: Labels,
    beforeEnter: requireAuth,
  },
];
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;