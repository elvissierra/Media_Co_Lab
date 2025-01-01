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
  /* Container Styling */
  .info-container.compact {
    max-width: 600px; /* Limit the width */
    margin: 0 auto; /* Center the container */
    background-color: #f9f9f9; /* Light gray background */
    border: 1px solid #ddd; /* Subtle border */
    border-radius: 8px; /* Rounded corners */
    padding: 16px; /* Add space inside */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    text-align: left; /* Align text to the left */
  }
  
  /* Heading Styling */
  .info-container h3 {
    margin-bottom: 8px; /* Reduce space below heading */
    font-size: 1.25rem; /* Slightly smaller font size */
    color: #333; /* Dark text color */
  }
  
  /* Paragraph Styling */
  .info-container p {
    margin: 0 0 8px; /* Compact spacing */
    font-size: 0.95rem; /* Smaller font size */
    line-height: 1.4; /* Tighter line spacing */
  }
  
  /* List Styling */
  .info-container ul {
    list-style-type: disc; /* Bulleted list */
    margin: 0 0 8px 20px; /* Compact with slight indentation */
    padding: 0;
  }
  
  .info-container ul li {
    margin-bottom: 4px; /* Tighten space between items */
    font-size: 0.9rem; /* Smaller font for compactness */
  }

  .demo-form {
  margin-top: 16px; /* Space above the form */
}

/* Form Elements */


.demo-form input[type="text"] {
  width: 100%; /* Full width */
  max-width: 300px; /* Limit input size */
  padding: 5px; /* Minimal padding */
  margin-bottom: 8px; /* Space below input */
  border: 1px solid #ccc; /* Subtle border */
  border-radius: 4px; /* Soft corners */
}

.demo-form button {
  padding: 6px 12px; /* Compact button size */
  background-color: #007bff; /* Blue background */
  color: white; /* White text */
  border: none; /* No border */
  border-radius: 4px; /* Rounded corners */
  font-size: 0.9rem; /* Consistent with form size */
  cursor: pointer; /* Pointer cursor */
}
  </style>
  