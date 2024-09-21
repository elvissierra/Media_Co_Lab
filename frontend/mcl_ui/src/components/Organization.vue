<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center"> Organization Overview: {{ organization?.title }} </h1>
      </v-col>
    </v-row>

    <!-- Teams Section -->
    <v-row>
      <v-col cols="12">
        <h2 class="text-center">Teams</h2>
      </v-col>
      <v-col
        v-for="team in organization?.teams"
        :key="team.title"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card class="mb-4" outlined hover>
          <v-card-title>{{ team.title }}</v-card-title>
          <v-card-text>
            {{ team.description }}
            <v-divider class="my-2"></v-divider>
            <h4>Users</h4>
            <v-list dense v-if="team.users.length">
              <v-list-item v-for="user in team.users" :key="user.first_name">
                <v-list-item-content>{{ user.first_name }}</v-list-item-content>
              </v-list-item>
            </v-list>
            <p v-else>No users in this team</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- TBD Medias Section -->
    <v-row v-if="organization?.medias && organization.medias.length">
      <v-col cols="12">
        <h2 class="text-center">Medias</h2>
      </v-col>
      <v-col
        v-for="media in organization.medias"
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

    <!-- TBD Labels Section -->
    <v-row v-if="organization?.labels && organization.labels.length">
      <v-col cols="12">
        <h2 class="text-center">Labels</h2>
      </v-col>
      <v-col
        v-for="label in organization.labels"
        :key="label.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-chip>{{ label.name }}</v-chip>
      </v-col>
    </v-row>
  </v-container>
</template>




<script>
export default {
  name: 'OrganizationOverview',
  data() {
    return {
      organization: null,
    };
  },
  async created() {
    try {
      const response = await this.$axios.get('/organizations/ov/');
      this.organization = response.data;
    } catch (error) {
      console.error('Error fetching organizational information:', error);
    }
  }
};
</script>

<style>
.v-card {
  cursor: pointer;
}
</style>
  