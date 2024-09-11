<template>
  <div class="header">
    <h1>Welcome to Media Co lab!</h1>

    <button v-if="!isLoggedIn" @click="goToRegister">Register</button>

    <button v-if="isLoggedIn" @click="logoutUser">Logout</button>
  </div>
</template>

<script>
export default {
  name: "TopPage",
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
  .top_page {
    text-align: center;
    margin-top: 50px;
  }
  
  h1 {
    font-size: 2.5em;
    color: #4caf50;
  }
  
  p {
    font-size: 1.2em;
  }

  .header {
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Pushes content to the top and bottom */
  padding: 0;
  margin: 0;
  position: relative;
  }

  .header button {
    align-self: flex-end; /* Moves button to the right */
    margin-top: auto; /* Pushes the button to the bottom */
    background-color: #ff5722;
    color: white;
    padding: 1rem 2rem;
    border: none;
    cursor: pointer;
    border-radius: 8px 8px 0 0;
    top: 10px;
  }

  .header button:hover {
    background-color: #e64a19;
  }

  </style>
  