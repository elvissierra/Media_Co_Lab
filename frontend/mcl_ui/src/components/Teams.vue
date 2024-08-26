<template>
  <div>
    <h1>Teams</h1>
    <ul>
      <li v-for="team in teams" :key="team.id">
        <h2>{{ team.name }}</h2>
        <ul>
          <li v-for="member in team.members" :key="member.id">
            {{ member.name }}
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'mclTeams',
  data() {
    return {
      teams: [],  // Array to store the fetched teams
    };
  },
  async created() {
    try {
      const response = await this.$axios.get('/teams/');  // axios use
      this.teams = response.data;
    } catch (error) {
      console.error('Error fetching teams:', error);
    }
  }
};
</script>
