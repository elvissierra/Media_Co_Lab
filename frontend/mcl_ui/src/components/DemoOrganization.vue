<template>
  <div>
    <h1>Create Demo Organization</h1>

    <!-- Informational Container -->
    <div class="info-container compact">
      <h3>Continue with the demo:</h3>
      <p>
        So you can explore the platform. After you create your organization,
        a demo team will also be initialized, and you can tinker with features of:
      </p>
      <ul>
        <li><strong>Teams:</strong> Separation between concerns</li>
        <li><strong>Upload Content:</strong> Media, documents</li>
        <li><strong>Collaborate:</strong> Message with team members</li>
      </ul>
    </div>

    <form class="demo-form" @submit.prevent="createDemoOrganization">
      <label for="org-title">Demo Organization Title: </label>
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
  
  <style scoped>
  
  .info-container.compact {
    max-width: 600px; 
    margin: 0 auto; 
    background-color: #f9f9f9; 
    border: 1px solid #ddd; 
    border-radius: 8px; 
    padding: 16px; 
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); 
    text-align: left; 
  }
  
  .info-container h3 {
    margin-bottom: 8px; 
    font-size: 1.25rem; 
    color: #333; 
  }
  
  .info-container p {
    margin: 0 0 8px; 
    font-size: 0.95rem; 
    line-height: 1.4; 
  }
  
  .info-container ul {
    list-style-type: disc; 
    margin: 0 0 8px 20px; 
    padding: 0;
  }
  
  .info-container ul li {
    margin-bottom: 4px; 
    font-size: 0.9rem; 
  }

  .demo-form {
  margin-top: 16px; 
}

.demo-form input[type="text"] {
  width: 100%; 
  max-width: 300px; 
  padding: 5px; 
  margin-bottom: 8px; 
  border: 1px solid #ccc; 
  border-radius: 4px; 
}

.demo-form button {
  padding: 6px 12px; 
  background-color: #007bff; 
  color: white; 
  border: none; 
  border-radius: 4px; 
  font-size: 0.9rem; 
  cursor: pointer; 
}
  </style>
  