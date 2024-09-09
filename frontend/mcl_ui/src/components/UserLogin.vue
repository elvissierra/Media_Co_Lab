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
    <router-link to="/home">Go to Homepage</router-link>
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
      isAuthenticated: !!localStorage.getItem('authToken'),
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

        localStorage.setItem('authToken', token);

        this.isAuthenticated = true;

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
  max-width: 400px;
  margin: 0 auto;
  padding: 1em;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: #f9f9f9;
}

.login h2 {
  text-align: center;
}

.login form div {
  margin-bottom: 1em;
}

.login form label {
  display: block;
  margin-bottom: 0.5em;
}

.login form input {
  width: 100%;
  padding: 0.5em;
  box-sizing: border-box;
}

.login button {
  width: 100%;
  padding: 0.75em;
  background: #007bff;
  border: none;
  border-radius: 4px;
  color: white;
  font-size: 1em;
}

.error {
  color: red;
  text-align: center;
}
</style>
