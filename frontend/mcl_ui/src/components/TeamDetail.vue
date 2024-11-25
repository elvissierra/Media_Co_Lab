<template>
  <v-container>
    <v-row v-if="team">
      <v-col cols="12">
        <h1 class="text-center">{{ team.title }}</h1>
        <p>{{ team.description }}</p>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <h2 class="text-center">Related Media</h2>

        <v-alert v-if="error" type="warning">
          {{ error }}
        </v-alert>

        <v-row v-if="relatedMedia.length > 0">
          <v-col
            v-for="media in relatedMedia"
            :key="media.id"
            cols="12"
            sm="6"
            md="4"
          >
          <v-card
              class="mb-4"
              @click="viewMedia(media.id)"
              outlined
              hover
              elevation="3"
            >
              <v-img
                v-if="isImage(media.content)"
                :src="getFullImageUrl(media.content)"
                :alt="media.title"
                height="200"
                class="media-image"
                cover
              ></v-img>
              <v-responsive v-else aspect-ratio="16/9">
                <video
                  controls
                  :src="getFullImageUrl(media.content)"
                  class="video-content"
                  style="width: 100%; height: 200px; object-fit: cover;"
                ></video>
              </v-responsive>
              <v-card-title class="text-h6 text-center mt-2">
                {{ media.title }}
              </v-card-title>
            </v-card>
          </v-col>
        </v-row>
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
      relatedMedia: [],
      error: null,
    };
  },
  async created() {
    const teamId = this.$route.params.team_id;
    try {
      const teamResponse = await this.$axios.get(`/teams/${teamId}/`);
      this.team = teamResponse.data;
      this.relatedMedia = this.team.medias
      if (this.relatedMedia.length === 0) {
        this.error = 'No related media found for this team.';
      }
    } catch (error) {
      console.error('Error fetching team or media details:', error);
      this.error = 'Unable to fetch team or media details. Please try again later.';
    }
  },
  methods: {
    isImage(filePath) {
      return /\.(jpeg|jpg|gif|png)$/.test(filePath);
    },
    getFullImageUrl(relativeUrl) {
      return `${process.env.VUE_APP_BASE_URL}${relativeUrl}`;
    },
    viewMedia(mediaId) {
      this.$router.push({ name: 'MediaDetail', params: { medias_id: mediaId } });
    },
  },
};
</script>


<style scoped>
.media-thumbnail {
  position: relative;
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.media-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.text-center {
  text-align: center;
}
</style>
