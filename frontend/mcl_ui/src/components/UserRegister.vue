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
  
            <v-text-field
              v-model="user.organization_id"
              label="Organization ID (optional)"
            ></v-text-field>
  
            <v-btn :disabled="!valid" @click="registerUser">
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
  export default {
    data() {
      return {
        valid: false,
        user: {
          first_name: '',
          last_name: '',
          email: '',
          password: '',
          organization_id: '', // Optional field
        },
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
    methods: {
        async registerUser() {
          try {
            this.error = null;
            await this.$axios.post('/register/', this.user); // No need to assign to a variable
            this.$router.push({ name: 'Login' });
          } catch (error) {
            this.error = error.response.data.detail || 'Registration failed. Please try again.';
          }
        }
    },
  };
  </script>
  