import { createStore } from 'vuex';
import axios from '@/axios';

const store = createStore({
  state: {
    user: null,
    authToken: localStorage.getItem('authToken') || null,
  },
  getters: {
    isLoggedIn: state => !!state.authToken,
    userHasOrganization: state => !!state.user?.organization,
    isOrgAdmin: state => !!state.user?.is_org_admin,
    isPlatformAdmin: state => !!state.user?.is_staff,
    isPendingApproval: state => state.user?.org_status === 'pending',
    isDenied: state => state.user?.org_status === 'denied',
    orgIsApproved: state => !!state.user?.organization?.is_approved,
  },
  actions: {
    async fetchUser({ commit }, userId) {
      try {
        const response = await axios.get(`/api/users/${userId}/`);
        commit('setUser', response.data);
        return response.data;
      } catch (error) {
        console.error('Error fetching user:', error);
      }
    },
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setUserOrganization(state, organization) {
      if (state.user) {
        state.user.organization = organization;
      }
    },
    setAuthToken(state, token) {
      state.authToken = token;
      if (token) {
        localStorage.setItem('authToken', token);
      } else {
        localStorage.removeItem('authToken');
      }
    },
  },
});

export default store;
