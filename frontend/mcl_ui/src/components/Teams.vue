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
        <v-card 
          class="mb-4"
          @click="viewTeam(team.id)"
          outlined
          hover
        >
          <v-card-title>
            {{ team.title }}
          </v-card-title>
          <v-card-text>
            <p>{{ team.description }}</p>
            <v-divider></v-divider>
            <v-list dense>
              <v-list-item
                v-for="user in team.users"
                :key="user.id"
              >
                <v-list-item-content>
                  {{ user.first_name }}
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
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
  methods: {
    viewTeam(teamId) {
      this.$router.push({ name: 'TeamDetail', params: { id: teamId } });
    }
  }
};
</script>

<style>
.v-card {
  cursor: pointer;
}
</style>
