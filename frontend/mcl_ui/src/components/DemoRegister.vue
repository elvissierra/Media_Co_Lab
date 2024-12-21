<template>
    <div>
      <h1>Create Demo Organization</h1>
      <form @submit.prevent="createDemoOrganization">
        <label for="org-title">Demo Organization Title:</label>
        <input type="text" id="org-title" v-model="demoTitle" />
        <button type="submit">Create Demo</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axiosPublic from '@/axiosPublic';

  export default {
    name: 'OrganizationDemo',
    data() {
      return {
        demoTitle: '',
        message: '',
      };
    },
    methods: {
      async createDemoOrganization() {
        try {
          const response = await axiosPublic.post('/organizations/demo/', {
            title: this.demoTitle,
          });
          this.message = `Demo organization "${response.data.title}" created successfully!`;
          this.demoTitle = ''; // Reset the form
        } catch (error) {
          console.error(error);
          this.message = 'Failed to create demo organization. Please try again.';
        }
      },
    },
  };
  </script>
  