<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6" offset-md="3">
        <v-form ref="form" v-model="valid">
          <v-text-field
            v-model="user.first_name"
            :rules="rules.required"
            label="First Name"
            required
          ></v-text-field>

          <v-text-field
            v-model="user.last_name"
            :rules="rules.required"
            label="Last Name"
            required
          ></v-text-field>

          <v-text-field
            v-model="user.email"
            :rules="[rules.required, rules.email]"
            label="Email"
            required
          ></v-text-field>

          <v-text-field
            v-model="user.password"
            :rules="rules.required"
            label="Password"
            type="password"
            required
          ></v-text-field>

          <v-select
            v-model="user.organization"
            :items="organizations"
            item-text="title"
            item-value="id"
            :rules="rules.required"
            label="Select Organization"
            required
          ></v-select>

          <v-btn @click="registerUser">
            Register
          </v-btn>

          <v-alert v-if="error" type="error">
            {{ error }}
          </v-alert>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axiosPublic from '@/axiosPublic';

export default {
  data() {
    return {
      valid: false,
      user: {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        orgnization: null,
      },
      organizations: [],
      error: null,
      rules: {
        required: (value) => !!value || 'Required.',
        email: (value) => {
          const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          return pattern.test(value) || 'Invalid email.';
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
        this.error = 'Issue fetching Organization.';
      }
    },
    async registerUser() {
      console.log(this.$refs.form.validate());
      if (!this.$refs.form.validate()) {
        console.log('Form is invalid');
        return;
      }
      try {
        this.error = null;
        await axiosPublic.post('/users/create/', this.user);
        this.$router.push({ name: 'UserLogin' });
      } catch (error) {
        this.error = error.response?.data?.detail || 'Registration failed. Please try again.';
      }
    },
  },
};
</script>
