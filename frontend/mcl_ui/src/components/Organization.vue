<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center"> Organization Overview </h1>
      </v-col>
    </v-row>

    <!-- Teams Section -->
    <v-row>
      <v-col cols="12">
        <h2 class="text-center">Teams</h2>
      </v-col>
      <v-col
        v-for="team in user_organization.teams"
        :key="team.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card class="mb-4" outlined hover>
          <v-card-title>{{ team.title }}</v-card-title>
          <v-card-text>{{ team.description }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Users Section -->
    <v-row>
      <v-col cols="12">
        <h2 class="text-center">Users</h2>
      </v-col>
      <v-col
        v-for="team in user_organization.teams"
        :key="team.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-col
          v-for="user in team.users"
          :key="user.id"
          cols="12"
          sm="6"
          md="4"
        >
          <v-card class="mb-4" outlined hover>
            <v-card-title> {{ user.first_name }}</v-card-title>
          </v-card>
          </v-col>
        </v-col>
    </v-row>

    <!-- Medias Section -->
    <v-row>
      <v-col cols="12">
        <h2 class="text-center">Medias</h2>
      </v-col>
      <v-col
        v-for="media in user_organization.medias"
        :key="media.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card class="mb-4" outlined hover>
          <v-card-title>{{ media.title }}</v-card-title>
          <v-card-text>{{ media.description }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>



<script>
export default {
  name: 'mclOrganization',
  data() {
    return {
      user_organization: {},
    };
  },
  async created() {
    try {
      const response = await this.$axios.get('/organizations/to/');      
      this.user_organization = response.data;
    } catch (error) {
      console.error('Error fetching organization:', error);
    }
  },
  methods: {
    vieworganization(organizationId) {
      this.$router.push({ name: 'mclOrganizationDetail', params: { uuid: organizationId } });
    }
  }
};

</script>

<style>
.v-card {
  cursor: pointer;
}
</style>
  