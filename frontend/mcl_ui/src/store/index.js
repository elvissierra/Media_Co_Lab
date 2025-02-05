import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state: {
    user: null,
    authToken: localStorage.getItem('authToken') || null,
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
  getters: {
    userHasOrganization: state => !!state.user?.organization,
    isLoggedIn: state => !!state.authToken,
  },
  actions: {
    async fetchUser({ commit }, userId) {
      try {
        const response = await axios.get(`/api/users/${userId}`);
        commit('setUser', response.data);
      } catch (error) {
        console.error('Error fetching user:', error);
      }
    },
  },
});

export default store;
