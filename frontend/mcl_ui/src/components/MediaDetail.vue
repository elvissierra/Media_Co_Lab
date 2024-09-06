<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">{{ media.title }}</h1>
        <p>{{ media.description }}</p>

        <div v-if="media.content">
          <v-img v-if="isImage(media.content)" :src="media.content" :alt="media.title" class="media-view mb-4"></v-img>
          <v-responsive v-else aspect-ratio="16/9" class="media-view mb-4">
            <video controls :src="media.content" class="video-view"></video>
          </v-responsive>
        </div>
      </v-col>
    </v-row>

    <!-- Comment Section -->
    <v-row>
      <v-col cols="12">
        <h2 class="text-center">Comments</h2>
        <div class="comments-container">
          <v-card
            v-for="comment in comments"
            :key="comment.id"
            :class="getUserColor(comment.user)"
            class="comment-box mb-3"
          >
            <v-card-title>
              {{ comment.user.username }}
            </v-card-title>
            <v-card-text>
              {{ comment.text }}
            </v-card-text>
          </v-card>
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
      comments: [], // Placeholder for fetched comments
    };
  },
  async created() {
    const mediaId = this.$route.params.uuid;
    try {
      const response = await this.$axios.get(`/medias/${mediaId}/`);
      this.media = response.data;

      const commentsResponse = await this.$axios.get(`/medias/${mediaId}/comments/`);
      this.comments = commentsResponse.data;
    } catch (error) {
      console.error('Error fetching media or comments:', error);
    }
  },
  methods: {
    isImage(filePath) {
      return /\.(jpeg|jpg|gif|png)$/.test(filePath);
    },
    getUserColor(user) {
      const userColors = {
        user1: 'green lighten-3',
        user2: 'blue lighten-3',
        user3: 'purple lighten-3',
        user4: 'orange lighten-3',
        // Add more user-specific colors as needed
      };
      return userColors[user.username] || 'grey lighten-3'; // Default color if no specific color
    },
  },
};
</script>

<style scoped>
.media-view {
  max-width: 800px;
  margin: 0 auto;
}

.video-view {
  max-width: 800px;
  height: auto;
}

.comments-container {
  display: flex;
  flex-direction: column;
}

.comment-box {
  padding: 10px;
  border-radius: 8px;
}

.text-center {
  text-align: center;
}
</style>
