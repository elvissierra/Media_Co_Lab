<template>
  <div v-if="!isAuthenticated" class="login">
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
  <div v-else>
    <p>You are already logged in.</p>
    <router-link to="/">Go to Homepage</router-link>
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
      isAuthenticated: !!localStorage.getItem('authToken'),  // Check if the user is authenticated
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await this.$axios.post('auth/login/', {
          username: this.email,
          password: this.password,
        });
        const token = response.data.token;

        // Store the token in localStorage (temporary)
        localStorage.setItem('authToken', token);

        // Update the authentication status
        this.isAuthenticated = true;

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
