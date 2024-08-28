<template>
  <div>
    <h1>Media</h1>
    <!-- Media-related content goes here -->
    <div v-if="mediaItems.length">
      <div v-for="media in mediaItems" :key="media.id">
        <!-- Display media content -->
        <p>{{ media.title }}</p>
        <p>{{ media.description }}</p>
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
      // Optionally handle other error cases here
    }
  },
};
</script>
