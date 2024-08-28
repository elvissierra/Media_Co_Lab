<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">{{ team.title }}</h1>
        <p>{{ team.description }}</p>
        <!-- Add more team details as needed -->
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'TeamDetail',
  data() {
    return {
      team: null,
    }
  },
  async created() {
    const teamId = this.$route.params.id
    try {
      const response = await this.$axios.get(`/teams/${teamId}/`)
      this.team = response.data
    } catch (error) {
      console.error('Error fetching team details:', error)
    }
  },
}
</script>
