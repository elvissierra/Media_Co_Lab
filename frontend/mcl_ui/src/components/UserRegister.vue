<template>
  <v-container class="d-flex align-center justify-center fill-height">
    <v-card class="w-100" style="max-width: 500px" elevation="8">
      <v-card-item>
        <div class="text-h5 font-weight-bold mb-1">Create Account</div>
        <p class="text-subtitle2 text-medium-emphasis">Join us and start collaborating</p>
      </v-card-item>

      <v-divider></v-divider>

      <v-card-text class="py-6">
        <v-form ref="form" v-model="valid">
          <v-text-field
            v-model="user.first_name"
            :rules="rules.required"
            label="First Name"
            variant="outlined"
            placeholder="John"
            density="comfortable"
            required
            class="mb-4"
          ></v-text-field>

          <v-text-field
            v-model="user.last_name"
            :rules="rules.required"
            label="Last Name"
            variant="outlined"
            placeholder="Doe"
            density="comfortable"
            required
            class="mb-4"
          ></v-text-field>

          <v-text-field
            v-model="user.email"
            :rules="[rules.required, rules.email]"
            label="Email"
            type="email"
            variant="outlined"
            placeholder="john.doe@example.com"
            density="comfortable"
            required
            class="mb-4"
          ></v-text-field>

          <v-text-field
            v-model="user.password"
            :rules="rules.required"
            label="Password"
            type="password"
            variant="outlined"
            placeholder="Enter a strong password"
            density="comfortable"
            required
            class="mb-4"
          ></v-text-field>

          <v-select
            v-model="user.organization"
            :items="organizations"
            item-title="title"
            item-value="id"
            :rules="rules.required"
            label="Select Organization"
            variant="outlined"
            density="comfortable"
            required
            class="mb-6"
          ></v-select>

          <v-alert v-if="error" type="error" variant="tonal" class="mb-6">
            {{ error }}
          </v-alert>

          <v-btn
            @click="registerUser"
            color="primary"
            size="large"
            block
            variant="elevated"
            :loading="loading"
          >
            Create Account
          </v-btn>
        </v-form>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="justify-center py-4">
        <span class="text-body2">Already have an account?</span>
        <v-btn
          text
          color="primary"
          to="/login"
          class="text-capitalize"
        >
          Sign in instead
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import axiosPublic from '@/axiosPublic';

export default {
  data() {
    return {
      valid: false,
      loading: false,
      user: {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        organization: null,
      },
      organizations: [],
      error: null,
      rules: {
        required: (value) => !!value || 'This field is required.',
        email: (value) => {
          const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          return pattern.test(value) || 'Please enter a valid email address.';
        },
      },
    };
  },
  async created() {
    await this.fetchOrganizations();
  },
  methods: {
    async fetchOrganizations(){
      try {
        const response = await axiosPublic.get('/organizations/');
        this.organizations = response.data;
      } catch (error) {
        this.error = 'Unable to load organizations. Please try again later.';
      }
    },
    async registerUser() {
      if (!this.$refs.form.validate()) {
        return;
      }
      try {
        this.loading = true;
        this.error = null;
        await axiosPublic.post('/users/create/', this.user);
        this.$router.push({ name: 'UserLogin' });
      } catch (error) {
        this.error = error.response?.data?.detail || 'Registration failed. Please try again.';
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

.mb-4 {
  margin-bottom: 1rem;
}

.mb-6 {
  margin-bottom: 1.5rem;
}
</style>