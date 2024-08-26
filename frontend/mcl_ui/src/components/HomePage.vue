<template>
  <div class="home-page">
    <h1>Welcome to Media Co lab!</h1>
    <p>Start to MCL!</p>
    <button @click="logoutUser">Logout</button> <!-- Logout Button -->
  </div>
</template>

<script>
export default {
  name: "HomePage",
  methods: {
    async logoutUser() {
      try {
        await this.$axios.post('auth/logout/', {}, {
          headers: {
            'Authorization': `Token ${localStorage.getItem('authToken')}`,
          },
        });
        localStorage.removeItem('authToken');
        this.$router.push({ name: 'UserLogin' });
      } catch (error) {
        console.error('Error on logout:', error);
      }
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
  