<template>
  <v-container class="pa-4">
    <v-row justify="center">
      <v-col cols="12" md="8" class="text-center">
        <h1 class="mb-5">Teams</h1>
      </v-col>
    </v-row>
    
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-alert v-if="error" type="error" dismissible>
          {{ error }}
        </v-alert>
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
        <v-card 
          class="mb-4"
          @click="viewTeam(team.id)"
          outlined
          hover
          elevation="2"
        >
          <v-img
            :src="team.image || 'https://via.placeholder.com/150'"
            height="150px"
          ></v-img>
          <v-card-title>
            <div>
              <h3 class="headline mb-1">{{ team.title }}</h3>
              <p class="grey--text">{{ team.description.length > 100 ? team.description.substring(0, 100) + '...' : team.description }}</p>
            </div>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-chip-group column>
              <v-chip
                v-for="user in team.users"
                :key="user.id"
                class="ma-1"
                outlined
                color="primary"
              >
                {{ user.first_name }}
              </v-chip>
            </v-chip-group>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'mclTeams',
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
  methods: {
    viewTeam(teamId) {
      this.$router.push({ name: 'TeamDetail', params: { team_id: teamId } });
    }
  }
};
</script>

<style>
.v-card {
  cursor: pointer;
}
</style>
