<template>
    <v-container>
      <v-row>
        <v-col cols="12" md="6" offset-md="3">
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="organization.title"
              :rules="rules.required"
              label="Organization Title"
              required
            ></v-text-field>
    
            <v-btn :loading="loading" :disabled="loading" @click="registerOrg">
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
    name: 'RegisterOrganization',
    data() {
      return {
        valid: false,
        loading: false,
        organization: {
          title: '',
        },
        error: null,
        rules: {
            required: [(v) => !!v || 'This field is required'],
            minLength: (v) => v.length >= 3 || 'Min 3 characters',
        }
      };
    },
    methods: {
      async registerOrg() {
        console.log(this.$refs.form.validate());
        if (!this.$refs.form.validate()) {
          console.log('Form is invalid');
          return;
        }
        try {
          this.error = null;
          await axiosPublic.post('/organizations/register/', this.organization);
          this.$router.push({ name: 'HomePage' });
        } catch (error) {
          this.error = error.response?.data?.detail || 'Registration failed. Please try again.';
        } finally {
            this.loading = false;
        }
      },
    },
  };
  </script>
  