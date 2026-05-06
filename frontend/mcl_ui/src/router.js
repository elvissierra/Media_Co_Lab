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
import PendingApproval from './components/PendingApproval.vue'
import PlatformAdmin from './components/PlatformAdmin.vue'

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
  {
    path: '/pending',
    name: 'PendingApproval',
    component: PendingApproval,
    beforeEnter: requireAuth,
  },
  {
    path: '/platform-admin',
    name: 'PlatformAdmin',
    component: PlatformAdmin,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('authToken');
      if (!token) return next('/login');
      next(); // server will 403 if not staff; component handles it
    },
  },
  {
    path: '/denied',
    name: 'DeniedAccess',
    component: {
      template: `
        <v-container class="fill-height d-flex align-center justify-center">
          <v-card max-width="480" class="pa-8 text-center">
            <v-icon size="64" color="error" class="mb-4">mdi-account-cancel</v-icon>
            <v-card-title class="text-h5 mb-2">Access Denied</v-card-title>
            <v-card-text>Your membership request was denied. Contact the organization admin for more information.</v-card-text>
            <v-btn variant="outlined" color="primary" @click="$router.push('/login')">Back to Login</v-btn>
          </v-card>
        </v-container>
      `,
    },
    beforeEnter: requireAuth,
  },
];
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;