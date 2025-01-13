<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">{{ media.title }}</h1>
        <p>{{ media.description }}</p>

        <div class="media-box">
          <div v-if="media.content">
            <v-img v-if="isImage(media.content)" :src="media.content" :alt="media.title" class="media-view"></v-img>
            <v-responsive v-else class="media-view">
              <video controls :src="media.content" class="video-view"></video>
            </v-responsive>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Comment Section TBD -->
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
      comments: [],
    };
  },
  async created() {
    const mediaId = this.$route.params.medias_id;
    try {
      const response = await this.$axios.get(`/medias/${mediaId}/`);
      this.media = response.data;

      const commentsResponse = await this.$axios.get(`/medias/${mediaId}/comments/`);
      this.comments = commentsResponse.data;
    } catch (error) {
      console.error('Error fetching comments:', error);
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
      };
      return userColors[user.username] || 'grey lighten-3';
    },
  },
};
</script>

<style scoped>
.media-box {
  border: 2px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.media-view {
  width: 100%;
  height: auto;
  object-fit: contain;
}

.video-view {
  max-width: 100%;
  height: auto; 
}

.comment-box {
  padding: 10px;
  border-radius: 8px;
}
</style>
