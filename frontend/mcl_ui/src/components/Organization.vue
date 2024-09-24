<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center mb-5">Organization Overview: {{ organization?.title }}</h1>
      </v-col>
    </v-row>

    <!-- Teams Section -->
    <v-row>
      <v-col cols="12">
        <h2 class="text-center mb-4">Teams</h2>
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
            <p>{{ team.description }}</p>
            <v-divider class="my-2"></v-divider>
            <h4>Users</h4>
            <v-list dense v-if="team.users.length">
              <v-list-item v-for="user in team.users" :key="user.first_name">
                <v-list-item-content>{{ user.first_name }}</v-list-item-content>
              </v-list-item>
            </v-list>
            <p v-else>No users in this team</p>

            <h4>Media Collage</h4>
            <v-row>
              <v-col
                v-for="media in team.medias"
                :key="media.uuid"
                cols="6"
                sm="4"
              >
                <v-hover v-slot:default="{ props }">
                  <v-card
                    v-bind="props"
                    @click="viewMedia(media.uuid)"
                    class="media-thumbnail"
                    elevation="2"
                    tile
                  >
                    <v-img v-if="isImage(media.content)" :src="getFullImageUrl(media.content)" :alt="media.title" aspect-ratio="1" />
                  </v-card>
                </v-hover>
              </v-col>
            </v-row>
            <p v-if="!team.medias.length">No media in this team</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- TBD Labels Section -->
    <v-row v-if="organization?.labels && organization.labels.length">
      <v-col cols="12">
        <h2 class="text-center mb-4">Labels</h2>
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
  },
  methods: {
    viewMedia(mediaId) {
      this.$router.push({ name: 'MediaDetail', params: { uuid: mediaId } });
    },
    isImage(filePath) {
      return /\.(jpeg|jpg|gif|png)$/.test(filePath);
    },
    getFullImageUrl(relativeUrl) {
      return `${this.$axios.defaults.baseURL}${relativeUrl}`;
  },
}
};
</script>

<style>
.v-card {
  transition: transform 0.3s;
}

.v-card:hover {
  transform: scale(1.05);
}

h1, h2, h4 {
  color: #1976D2; /* Primary color */
}

.mb-4 {
  margin-bottom: 20px;
}

.mb-5 {
  margin-bottom: 40px;
}
.media-thumbnail {
  cursor: pointer;
  transition: transform 0.3s;
}

.media-thumbnail:hover {
  transform: scale(1.05);
}
</style>