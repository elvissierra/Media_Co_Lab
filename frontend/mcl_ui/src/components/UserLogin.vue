<template>
    <div class="login">
      <h2>Login</h2>
      <form @submit.prevent="loginUser">
        <div>
          <label for="email">Email:</label>
          <input type="email" v-model="email" required />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" v-model="password" required />
        </div>
        <button type="submit">Login</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: "UserLogin",
    data() {
      return {
        email: '',
        password: '',
        error: null,
      };
    },
    methods: {
      async loginUser() {
        try {
          const response = await this.$axios.post('auth/login/', {
            email: this.email,
            password: this.password,
          });
          const token = response.data.token;
  
          // Save the token to localStorage
          localStorage.setItem('authToken', token);

          // Redirect to the home page
          this.$router.push({ name: 'HomePage' });
        } catch (error) {
          this.error = 'Invalid email or password';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .login {
    max-width: 300px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .error {
    color: red;
    margin-top: 10px;
  }
  </style>
  