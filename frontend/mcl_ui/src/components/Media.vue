<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">Media</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col
        v-for="media in medias"
        :key="media.uuid"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card 
          class="mb-4"
          @click="viewMedia(media.uuid)"
          outlined
          hover
        >
          <v-card-title>
            {{ media.title }}
          </v-card-title>
          <v-card-text>
            <p>{{ media.description }}</p>
            <v-divider></v-divider>
            <div v-if="media.content">
              <v-img v-if="isImage(media.content)" :src="getFullImageUrl(media.content)" :alt="media.title"></v-img>
              <v-responsive v-else aspect-ratio="16/9">
                <video controls :src="media.content" style="width: 100%;"></video>
              </v-responsive>
            </div>
            <v-divider></v-divider>
            <p>Team: {{ media.team_title }}</p>
            <v-row v-if="media.labels && media.labels.length > 0">
              <v-col
                v-for="label in media.labels"
                :key="label.title"
                cols="auto"
              >
                <v-chip
                  :color="label.preset_tag"
                  class="ma-1"
                  small
                  outlined
                >
                  {{ label.title }}
                </v-chip>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'mclMedia',
  data() {
    return {
      medias: [],
    };
  },
  async created() {
    try {
      const response = await this.$axios.get('/medias/');
      this.medias = response.data;
    } catch (error) {
      console.error('Error fetching media items:', error);
    }
  },
  methods: {
    isImage(filePath) {
      return /\.(jpeg|jpg|gif|png)$/.test(filePath);
    },
    viewMedia(mediaId) {
      this.$router.push({ name: 'MediaDetail', params: { uuid: mediaId } });
    },
    getFullImageUrl(relativeUrl) {
  return `http://localhost:8000${relativeUrl}`;

  },
}
};
</script>

<style scoped>
.v-card {
  cursor: pointer;
}

</style>
