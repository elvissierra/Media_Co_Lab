<template>
    <div>
      <h1>Create Demo Organization</h1>
      <h3>Continue with the demo: So you can explore the platform quicker. After you create your organization, 
        a demo team will also be initialized and youll be able to upload media and tinker with the platform.
      </h3>
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
    name: 'DemoOrganization',
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
          this.demoTitle = '';
        } catch (error) {
          console.error(error);
          this.message = 'Failed to create demo organization. Please try again.';
        }
      },
    },
  };
  </script>
  