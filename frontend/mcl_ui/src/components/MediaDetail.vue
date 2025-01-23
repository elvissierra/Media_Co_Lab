<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center" v-if="media">{{ media.title }}</h1>
        <p v-if="media">{{ media.description }}</p>
        <v-progress-circular v-else indeterminate color="primary" class="mx-auto"></v-progress-circular>

        <div v-if="media && media.content" class="media-box">
          <div v-if="isImage(media.content)">
            <v-img :src="media.content" :alt="media.title" class="media-view"></v-img>
          </div>
          <v-responsive v-else class="media-view">
            <video controls :src="media.content" class="video-view"></video>
          </v-responsive>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <h2 class="text-center">Comments</h2>

        <v-progress-circular v-if="loadingComments" indeterminate color="primary" class="mx-auto"></v-progress-circular>

        <p v-if="!comments.length && !loadingComments" class="text-center">No comments yet</p>

        <div v-else class="comments-container">
          <v-card v-for="comment in comments" :key="comment.id" :class="getUserColor(comment.owner)" class="comment-box mb-3">
            <v-card-title>
              {{ comment.owner }}
            </v-card-title>
            <v-card-text>
              {{ comment.content }}
            </v-card-text>
          </v-card>
        </div>

        <v-btn v-if="nextPageUrl" @click="loadMoreComments" color="primary">Load More Comments</v-btn>

        <v-form v-if="media" @submit.prevent="submitComment">
          <v-textarea v-model="newComment" label="Add a comment" outlined rows="3" required></v-textarea>
          <v-btn type="submit" color="primary" :disabled="isSubmitting">Post Comment</v-btn>
        </v-form>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar.visible" :timeout="snackbar.timeout" :color="snackbar.color">
      {{ snackbar.message }}
      <v-btn color="white" text @click="snackbar.visible = false">Close</v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
export default {
  name: 'MediaDetail',
  data() {
    return {
      media: null,
      comments: [],
      newComment: '',
      isSubmitting: false,
      loadingComments: true,
      nextPageUrl: null,
      snackbar: {
        visible: false,
        message: '',
        color: 'success',
        timeout: 3000,
      },
    };
  },
  async created() {
    const mediaId = this.$route.params.medias_id;
    try {
      const response = await this.$axios.get(`/medias/${mediaId}/`);
      this.media = response.data;

      await this.loadComments();
    } catch (error) {
      console.error('Error fetching media or comments:', error);
      this.snackbar.message = 'Failed to fetch media or comments, please try again.';
      this.snackbar.color = 'error';
      this.snackbar.visible = true;
    } finally {
      this.loadingComments = false;
    }
  },
  methods: {
    isImage(filePath) {
      return /\.(jpeg|jpg|gif|png)$/.test(filePath);
    },
    getUserColor(user) {
      const hash = Array.from(user.username).reduce((acc, char) => acc + char.charCodeAt(0), 0);
      const colorIndex = hash % 4;
      const colors = ['green lighten-3', 'blue lighten-3', 'purple lighten-3', 'orange lighten-3'];
      return colors[colorIndex] || 'grey lighten-3';
    },
    async loadComments() {
      this.loadingComments = true;
      const mediaId = this.$route.params.medias_id;
      try {
        const response = await this.$axios.get(`/medias/${mediaId}/comments/`);
        this.comments = response.data.results;
        this.nextPageUrl = response.data.next;
      } catch (error) {
        console.error('Error fetching comments:', error);
        this.snackbar.message = 'Failed to load comments.';
        this.snackbar.color = 'error';
        this.snackbar.visible = true;
      } finally {
        this.loadingComments = false;
      }
    },
    async loadMoreComments() {
      if (this.nextPageUrl) {
        this.loadingComments = true;
        try {
          const response = await this.$axios.get(this.nextPageUrl);
          this.comments.push(...response.data.results);
          this.nextPageUrl = response.data.next;
        } catch (error) {
          console.error('Error loading more comments:', error);
          this.snackbar.message = 'Failed to load more comments.';
          this.snackbar.color = 'error';
          this.snackbar.visible = true;
        } finally {
          this.loadingComments = false;
        }
      }
    },
    async submitComment() {
      if (this.newComment.trim()) {
        this.isSubmitting = true;
        const mediaId = this.$route.params.medias_id;
        try {
          const response = await this.$axios.post(`/medias/${mediaId}/comments/`, {
            text: this.newComment,
          });
          this.comments.push(response.data);
          this.newComment = '';
        } catch (error) {
          console.error('Error posting comment:', error);
          this.snackbar.message = 'Failed to post your comment, please try again.';
          this.snackbar.color = 'error';
          this.snackbar.visible = true;
        } finally {
          this.isSubmitting = false;
        }
      } else {
        alert('Please enter a comment before submitting.');
      }
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

.comments-container {
  margin-top: 20px;
}

.comment-form {
  margin-top: 20px;
}
</style>
