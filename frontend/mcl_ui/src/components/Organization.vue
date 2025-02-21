<template>
  <v-container class="pa-4">
    <v-row justify="center">
      <v-col cols="12" md="8" class="text-center">
        <h1 class="headline mb-5">Organization Overview: {{ organization?.title }}</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" class="mb-4">
        <h2 class="text-center mb-4">Teams</h2>
      </v-col>
      <v-col
        v-for="team in organization?.teams"
        :key="team.title"
        cols="12"
        sm="6"
        md="4"
        class="mb-4"
      >
        <v-card outlined elevation="3" class="pa-3 team-card">
          <v-card-title class="text-uppercase font-weight-bold d-flex align-center justify-center">
            <v-icon left class="mr-2">mdi-account-group</v-icon>
            {{ team.title }}
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pt-3">
            <v-img
              v-if="team.image"
              :src="team.image"
              height="150px"
              class="mb-3"
              contain
            ></v-img>
            <p>{{ team.description }}</p>
            <v-divider class="my-2"></v-divider>
            
            <h4 class="subtitle-2 mb-3">Users</h4>
            <v-chip-group
              column
              class="d-flex flex-wrap"
            >
              <v-chip
                v-for="user in team.users"
                :key="user.id"
                class="ma-1 d-flex align-center user-chip"
                outlined
                color="primary"
                ripple="false"
                size="large"
              >
                <v-avatar left size="32" class="mr-2 ml-n2">
                  <v-img
                    :src="getFullImageUrl(user.avatar)"
                    alt="user avatar"
                    height="40"
                    width="40"
                    aspect-ratio="1"
                    class="rounded-circle"
                  />
                </v-avatar>
                {{ user.first_name }}
              </v-chip>
            </v-chip-group>
            <p v-if="!team.users.length" class="text-grey">No users in this team</p>

            <v-divider class="my-4"></v-divider>
            
            <h4 class="subtitle-2 mb-3">Media Collage</h4>
            <v-row>
              <v-col
                v-for="media in team.medias"
                :key="media.uuid"
                cols="6"
                sm="4"
                md="3"
                class="mb-3"
              >
                <v-hover v-slot:default="{ props }">
                  <v-card
                    v-bind="props"
                    @click="viewMedia(media.uuid)"
                    class="media-thumbnail"
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
            <p v-if="!team.medias.length" class="text-grey">No media in this team</p>

            <v-card-actions class="justify-center mt-4">
              <v-btn color="blue darken-2" class="white---text" @click="viewTeam(team.id)">View Team</v-btn>
            </v-card-actions>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="organization?.labels && organization.labels.length">
      <v-col cols="12" class="mb-4">
        <h2 class="text-center mb-4">Labels</h2>
      </v-col>
      <v-col
        v-for="label in organization.labels"
        :key="label.id"
        cols="12"
        sm="6"
        md="4"
        class="mb-4"
      >
        <v-card outlined class="pa-3" :color="label.color || 'grey lighten-4'">
          <v-card-title class="font-weight-medium">
            <v-chip color="primary" text-color="white">{{ label.name }}</v-chip>
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
    viewTeam(teamId) {
      this.$router.push({ name: 'TeamDetail', params: { team_id: teamId } });
    },
    isImage(filePath) {
      return /\.(jpeg|jpg|gif|png)$/.test(filePath);
    },
    getFullImageUrl(relativeUrl) {
      return `${process.env.VUE_APP_BASE_URL}${relativeUrl}`;
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

.team-card {
  border: 2px solid #1976D2;
  border-radius: 8px;
  pointer-events: none;
}

.team-card .v-card-actions,
.team-card .v-btn {
  pointer-events: auto;
}

h1, h2, h4 {
  color: #1976D2;
}

.mb-4 {
  margin-bottom: 20px;
}

.mb-5 {
  margin-bottom: 40px;
}
.media-thumbnail {
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.media-thumbnail:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15)
}

.text-grey {
  color: #9e9e9e
}

.hover-effect {
  transition: transform 0.3s ease-in-out;
}
.hover-effect:hover {
  transform: scale(1.05);
}
</style>