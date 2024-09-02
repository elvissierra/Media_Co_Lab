<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-center">{{ media.title }}</h1>
          <p>{{ media.description }}</p>
  
          <div v-if="media.content">
            <v-img v-if="isImage(media.content)" :src="media.content" :alt="media.title" class="mb-4"></v-img>
            <v-responsive v-else aspect-ratio="16/9" class="mb-4">
              <video controls :src="media.content" style="width: 100%;"></video>
            </v-responsive>
          </div>
  
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'MediaDetail',
    data() {
      return {
        media: null,
      }
    },
    async created() {
      const mediaId = this.$route.params.uuid
      try {
        const response = await this.$axios.get(`/medias/${mediaId}/`)
        this.media = response.data
      } catch (error) {
        console.error('Error fetching media details:', error)
      }
    },
    methods: {
      isImage(filePath) {
        return /\.(jpeg|jpg|gif|png)$/.test(filePath);
      },
    },
  }
  </script>
  
  <style scoped>
  .v-container {
    margin-top: 20px;
  }
  
  .v-img, .v-responsive {
    max-width: 100%;
  }
  </style>
  