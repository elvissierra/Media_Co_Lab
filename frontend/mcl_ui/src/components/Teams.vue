<template>
  <div>
    <h1>Teams</h1>
    <ul>
      <li v-for="team in teams" :key="team.id">
        <h2>{{ team.title }}</h2>
        <p>{{ team.description }}</p>
        <ul>
          <li v-for="user in team.users" :key="user.id">
            {{ user.first_name }}
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
      const response = await this.$axios.get('/teams/');  // Use this.$axios
      this.teams = response.data;
    } catch (error) {
      console.error('Error fetching teams:', error);
    }
  }
};
</script>
