<template>
  <div>
    <h1>Media</h1>
    <!-- Display media-related content -->
    <div v-if="mediaItems.length">
      <div v-for="media in mediaItems" :key="media.id" class="media-item">
        <h3>{{ media.title }}</h3>
        <p>{{ media.description }}</p>
        <div v-if="media.media_type === 'image'">
          <img :src="media.file_url" :alt="media.title" />
        </div>
        <div v-if="media.media_type === 'video'">
          <video controls :src="media.file_url"></video>
        </div>
        <!-- Add more media types as needed -->
      </div>
    </div>
    <div v-else>
      <p>No media items available.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'mclMedia',
  data() {
    return {
      mediaItems: [], // Array to store fetched media data
    };
  },
  async created() {
    try {
      const response = await this.$axios.get('/medias/');
      this.mediaItems = response.data;
    } catch (error) {
      console.error('Error fetching media items:', error);
    }
  },
};
</script>

<style scoped>
.media-item {
  margin-bottom: 20px;
}

.media-item img,
.media-item video {
  max-width: 100%;
  height: auto;
  display: block;
}
</style>
