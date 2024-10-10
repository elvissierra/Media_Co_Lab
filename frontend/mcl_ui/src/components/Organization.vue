<template>
  <v-container class="pa-4">
    <v-row justify="center">
      <v-col cols="12" md="8" class="text-center">
        <h1 class="mb-5">Organization Overview: {{ organization?.title }}</h1>
      </v-col>
    </v-row>

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
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header>
              <v-icon left>mdi-account-group</v-icon>
              {{ team.title }}
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-card-text>
                <v-img
                  v-if="team.image"
                  :src="team.image"
                  height="150px"
                  class="mb-3"
                ></v-img>
                <p>{{ team.description }}</p>
                <v-divider class="my-2"></v-divider>
                <h4>Users</h4>
                <v-chip-group>
                  <v-chip
                    v-for="user in team.users"
                    :key="user.id"
                    class="ma-1"
                    outlined
                    color="primary"
                    ripple="false"
                  >
                    <v-avatar left size="24">
                      <img :src="getFullImageUrl(user.avatar)" alt="user avatar" />
                    </v-avatar>
                    {{ user.first_name }}
                  </v-chip>
                </v-chip-group>
                <p v-if="!team.users.length">No users in this team</p>

                <h4>Media Collage</h4>
                <v-row>
                  <v-col
                    v-for="media in team.medias"
                    :key="media.uuid"
                    cols="6"
                    sm="4"
                    md="3"
                  >
                    <v-hover v-slot:default="{ props }">
                      <v-card
                        v-bind="props"
                        @click="viewMedia(media.uuid)"
                        class="media-thumbnail mb-2"
                        elevation="2"
                        tile
                      >
                        <v-img
                          v-if="isImage(media.content)"
                          :src="getFullImageUrl(media.content)"
                          :alt="media.title"
                          aspect-ratio="1"
                          class="hover-effect"
                        />
                      </v-card>
                    </v-hover>
                  </v-col>
                </v-row>
                <p v-if="!team.medias.length">No media in this team</p>

                <v-card-actions>
                  <v-btn color="primary" @click="viewTeamDetails(team.id)">View Team</v-btn>
                </v-card-actions>
              </v-card-text>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>

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
        <v-card outlined class="mb-3" :color="label.color || 'grey lighten-4'">
          <v-card-title>
            <v-chip>{{ label.name }}</v-chip>
          </v-card-title>
        </v-card>
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
      console.log(this.organization);
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
      return `${process.env.VUE_APP_MEDIA_BASE_URL}${relativeUrl}`;
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

.hover-effect {
  transition: transform 0.3s ease-in-out;
}
.hover-effect:hover {
  transform: scale(1.05);
}
</style>