<template>
    <v-container>
      <v-row>
        <v-col cols="12" md="6" offset-md="3">
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="teamData.title"
              :rules="rules.required"
              label="Title"
              required
            ></v-text-field>
  
            <v-text-field
              v-model="teamData.description"
              :rules="rules.required"
              label="Description"
              required
            ></v-text-field>
  
            <v-btn @click.prevent="createTeam" :disabled="!valid">
              Launch Team
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
        teamData: {
          title: '',
          description: '',
        },
        error: null,
        rules: {
          required: [(v) => !!v || "This field is required"],
        },
      };
    },
    methods: {
      async createTeam() {
        if (!this.$refs.form.validate()) {
          console.log('Form is invalid');
          return;
        }
  
        try {
          this.error = null;
          const response = await this.$axios.post('/teams/', this.teamData);    
          await this.$router.push({ name: 'TeamDetail', params: { id: response.data.id } });
        } catch (error) {
          this.error = error.response?.data?.detail || 'Creation failed. Please try again.';
        }
      },  
    },
  };
  </script>
  