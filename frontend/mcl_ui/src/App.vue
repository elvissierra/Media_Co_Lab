<template>
  <v-app>
    <v-app-bar elevation="4" color="primary">
      <v-app-bar-title class="font-weight-bold">Media Co Lab</v-app-bar-title>
      <v-spacer></v-spacer>

      <nav class="d-flex gap-2 align-center">
        <v-btn
          v-if="!isHomePage"
          text
          to="/"
          class="text-white"
        >
          Home
        </v-btn>
        <v-btn
          text
          to="/organizations/demo"
          class="text-white"
        >
          Demo
        </v-btn>
        <v-btn
          text
          to="/organizations/ov"
          class="text-white"
        >
          Organization
        </v-btn>
        <v-btn
          text
          to="/teams"
          class="text-white"
        >
          Teams
        </v-btn>
        <v-btn
          text
          to="/medias"
          class="text-white"
        >
          Media
        </v-btn>
      </nav>

      <v-divider vertical class="mx-3 opacity-30"></v-divider>

      <v-btn
        v-if="!isLoggedIn"
        text
        @click="loginUser"
        class="text-white"
      >
        Login
      </v-btn>
      <v-btn
        v-if="!isLoggedIn"
        variant="tonal"
        @click="goToRegister"
        class="mx-2"
      >
        Register
      </v-btn>
      <v-btn
        v-if="isLoggedIn"
        text
        @click="logoutUser"
        class="text-white"
      >
        Logout
      </v-btn>
    </v-app-bar>

    <v-main class="bg-background">
      <router-view />
    </v-main>
  </v-app>
</template>


<script>
import { mapGetters, mapMutations } from 'vuex';

export default {
  name: "App",
  computed: {
    ...mapGetters(['isLoggedIn']),
    isHomePage() {
      return this.$route.path === '/';
    }
  },
  methods: {
    ...mapMutations(['setAuthToken']),
    async logoutUser() {
      try {
        await this.$axios.post('auth/logout/', {}, {
          headers: {
            'Authorization': `Token ${this.$store.state.authToken}`,
          },
        });
        this.setAuthToken(null);
        this.$router.push({ name: 'UserLogin' });
      } catch (error) {
        console.error('Error on logout:', error);
      }
    },
    goToRegister() {
      this.$router.push({ name: 'UserRegister' });
    },
    loginUser() {
      this.$router.push({ name: 'UserLogin' });
    },
  },
  created() {
  },
};
</script>


<style scoped>
.gap-2 {
  gap: 0.5rem;
}
</style>