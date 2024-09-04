<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">{{ team.title }}</h1>
        <p>{{ team.description }}</p>
        <!-- Add more team details as needed -->
      </v-col>
    </v-row>

    <!-- Media Thumbnails -->
    <v-row>
      <v-col cols="12">
        <h2 class="text-center">Related Media</h2>
        <v-row>
          <v-col
            v-for="media in relatedMedia"
            :key="media.id"
            cols="12"
            sm="6"
            md="4"
          >
            <div class="media-thumbnail">
              <!-- Media Content (Image or Video Thumbnail) -->
              <v-img
                v-if="isImage(media.content)"
                :src="media.content"
                :alt="media.title"
                class="media-image"
              ></v-img>
              <v-responsive v-else class="media-image">
                <video :src="media.content" muted></video>
              </v-responsive>

              <!-- Sticky Tabs for Labels -->
              <div class="sticky-tabs">
                <div
                  v-for="label in media.labels"
                  :key="label.id"
                  :style="{ backgroundColor: label.preset_tag }"
                  class="sticky-tab"
                ></div>
              </div>
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
      relatedMedia: [], // Related media objects for the team
    };
  },
  async created() {
    const teamId = this.$route.params.uuid;
    try {
      // Fetch team details
      const response = await this.$axios.get(`/teams/${teamId}/`);
      this.team = response.data;

      // Fetch related media for the team
      const mediaResponse = await this.$axios.get(`/teams/${teamId}/medias/`);
      this.relatedMedia = mediaResponse.data;
    } catch (error) {
      console.error('Error fetching team or media details:', error);
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

.sticky-tabs {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.sticky-tab {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Styling for title, description, etc. */
.text-center {
  text-align: center;
}
</style>
