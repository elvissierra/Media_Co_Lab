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
        :key="media.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card 
          class="mb-4"
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
              <v-img v-if="isImage(media.content)" :src="media.content" :alt="media.title"></v-img>
              <v-responsive v-else aspect-ratio="16/9">
                <video controls :src="media.content" style="width: 100%;"></video>
              </v-responsive>
            </div>
            <v-divider></v-divider>
            <p>Team: {{ media.team.name }}</p>
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
      medias: [], // Array to store fetched media data
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
  },
};
</script>

<style scoped>
.v-card {
  cursor: pointer;
}
</style>
