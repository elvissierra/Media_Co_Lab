<template>
  <v-container class="d-flex align-center justify-center fill-height">
    <v-card v-if="!isAuthenticated" class="w-100" style="max-width: 450px" elevation="8">
      <v-card-item>
        <div class="text-h5 font-weight-bold mb-1">Welcome Back</div>
        <p class="text-subtitle2 text-medium-emphasis">Sign in to your account</p>
      </v-card-item>

      <v-divider></v-divider>

      <v-card-text class="py-6">
        <form @submit.prevent="loginUser" class="space-y-4">
          <v-text-field
            v-model="email"
            label="Email"
            type="email"
            placeholder="your.email@example.com"
            variant="outlined"
            required
            density="comfortable"
          ></v-text-field>

          <v-text-field
            v-model="password"
            label="Password"
            type="password"
            placeholder="Enter your password"
            variant="outlined"
            required
            density="comfortable"
          ></v-text-field>

          <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
            {{ error }}
          </v-alert>

          <v-btn
            type="submit"
            color="primary"
            size="large"
            block
            variant="elevated"
            :loading="loading"
          >
            Sign In
          </v-btn>
        </form>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="justify-center py-4">
        <span class="text-body2">Don't have an account?</span>
        <v-btn
          text
          color="primary"
          to="/register"
          class="text-capitalize"
        >
          Sign up here
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-card v-else class="w-100" style="max-width: 450px" elevation="8">
      <v-card-item>
        <div class="text-h5 font-weight-bold">Already Logged In</div>
      </v-card-item>
      <v-divider></v-divider>
      <v-card-text class="py-6">
        <p class="mb-4">You are already logged in.</p>
        <v-btn
          to="/"
          color="primary"
          block
          variant="elevated"
        >
          Go to Homepage
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';

export default {
  name: "UserLogin",
  data() {
    return {
      email: '',
      password: '',
      error: null,
      loading: false,
    };
  },
  computed: {
    ...mapGetters(['isLoggedIn']),
    isAuthenticated() {
      return this.isLoggedIn;
    }
  },
  methods: {
    ...mapMutations(['setAuthToken']),
    async loginUser() {
      try {
        this.loading = true;
        this.error = null;
        const response = await this.$axios.post('auth/login/', {
          email: this.email,
          password: this.password,
        });
        const token = response.data.token;

        this.setAuthToken(token);

        this.$router.push({ name: 'HomePage' });
      } catch (error) {
        this.error = 'Invalid email or password';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>


<style scoped>
.fill-height {
  min-height: 100vh;
}

.w-100 {
  width: 100%;
}

.space-y-4 > * + * {
  margin-top: 1rem;
}
</style>