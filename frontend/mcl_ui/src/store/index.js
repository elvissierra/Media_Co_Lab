import { createStore } from 'vuex';

const store = createStore({
  state: {
    user: null,
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
  },
  getters: {
    userHasOrganization: state => !!state.user?.organization,
  },
  actions: {
    async fetchUser({ commit }) {
      try {
        const response = await axios.get('/api/users/${userId}');
        commit('setUser', response.data);
      } catch (error) {
        console.error('Error fetching user:', error);
      }
    },
  },
});

export default store;