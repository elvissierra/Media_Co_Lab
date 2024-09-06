<template>
  <div class="home-page">
    <h1>Welcome to Media Co lab!</h1>
    <p>Start to MCL!</p>

    <button v-if="!isLoggedIn" @click="goToRegister">Register</button>

    <button v-if="isLoggedIn" @click="logoutUser">Logout</button>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      isLoggedIn: false,
    };
  },
  created() {
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
      this.isLoggedIn = !!localStorage.getItem('authToken');
    },
    async logoutUser() {
      try {
        await this.$axios.post('auth/logout/', {}, {
          headers: {
            'Authorization': `Token ${localStorage.getItem('authToken')}`,
          },
        });
        localStorage.removeItem('authToken');
        this.isLoggedIn = false; // Update login status
        this.$router.push({ name: 'UserLogin' });
      } catch (error) {
        console.error('Error on logout:', error);
      }
    },
    goToRegister() {
      this.$router.push({ name: 'UserRegister' });
    },
  },
};
</script>

  
  <style scoped>
  .home-page {
    text-align: center;
    margin-top: 50px;
  }
  
  h1 {
    font-size: 2.5em;
    color: #42b983;
  }
  
  p {
    font-size: 1.2em;
  }
  </style>
  