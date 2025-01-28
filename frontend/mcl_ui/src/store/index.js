import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state: {
    user: null, // Stores user data
    authToken: localStorage.getItem('authToken') || null, // Persist token across sessions
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setAuthToken(state, token) {
      state.authToken = token;
      if (token) {
        localStorage.setItem('authToken', token);
      } else {
        localStorage.removeItem('authToken');
      }
    },
    clearAuth(state) {
      state.user = null;
      state.authToken = null;
      localStorage.removeItem('authToken');
    },
  },
  getters: {
    isAuthenticated: state => !!state.authToken, // Check if user is logged in
    userHasOrganization: state => !!state.user?.organization, // Check if user belongs to an organization
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('/api/auth/login/', credentials);
        commit('setAuthToken', response.data.token);
        await this.dispatch('fetchUser', response.data.userId); // Fetch user data
      } catch (error) {
        console.error('Error during login:', error);
        throw error; // Propagate error for handling in components
      }
    },
    async logout({ commit }) {
      try {
        await axios.post('/api/auth/logout/', {}, {
          headers: {
            Authorization: `Token ${this.state.authToken}`,
          },
        });
      } catch (error) {
        console.warn('Error during logout or already logged out:', error);
      } finally {
        commit('clearAuth');
      }
    },
    async fetchUser({ commit }, userId) {
      try {
        const response = await axios.get(`/api/users/${userId}`, {
          headers: {
            Authorization: `Token ${this.state.authToken}`,
          },
        });
        commit('setUser', response.data);
      } catch (error) {
        console.error('Error fetching user:', error);
      }
    },
  },
});

export default store;
