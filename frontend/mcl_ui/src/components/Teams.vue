<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">Teams</h1>
      </v-col>
    </v-row>
    
    <v-row>
      <v-col
        v-for="team in teams"
        :key="team.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card class="mb-4">
          <v-card-title>
            {{ team.title }}
          </v-card-title>
          <v-card-text>
            {{ team.description }}
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary">View Team</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'mclTeam',
  data() {
    return {
      teams: [],
    };
  },
  async created() {
    try {
      const response = await this.$axios.get('/teams/');
      this.teams = response.data;
    } catch (error) {
      console.error('Error fetching teams:', error);
    }
  },
};
</script>

