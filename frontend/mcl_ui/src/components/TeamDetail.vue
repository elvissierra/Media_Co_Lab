<template>
  <v-container>
    <v-row>
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
            <div class="media-thumbnail">
              <h3>{{ media.title }}</h3>
              <v-img
                v-if="isImage(media.content)"
                :src="media.content"
                :alt="media.title"
                class="media-image"
              ></v-img>
              <v-responsive v-else class="media-image">
                <video :src="media.content" controls muted></video>
              </v-responsive>
            </div>
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
    const teamId = this.$route.params.uuid;
    try {
    
      const teamResponse = await this.$axios.get(`/teams/${teamId}/`);
      this.team = teamResponse.data;

    
      const mediaResponse = await this.$axios.get(`/teams/${teamId}/medias/`);
      this.relatedMedia = mediaResponse.data;

    
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
