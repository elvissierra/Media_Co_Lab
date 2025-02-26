<template>
  <v-container>
    <!-- Media Area -->
    <v-row>
      <v-col cols="12">
        <div class="media-details">
          <h1 class="text-center" v-if="media">{{ media.title }}</h1>
          <p class="text-center" v-if="media">{{ media.description }}</p>
          <div v-if="media && media.content" class="media-box">
            <div v-if="isImage(media.content)">
              <v-img :src="media.content" :alt="media.title" class="media-view"></v-img>
            </div>
            <v-responsive v-else class="media-view">
              <video controls :src="media.content" class="video-view"></video>
            </v-responsive>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Chat Area -->
    <v-row>
      <v-col cols="12">
        <div class="chat-area">
          <h2 class="text-center">Chat</h2>
          <v-progress-circular
            v-if="loadingMedia"
            indeterminate
            color="primary"
            class="mx-auto"
          ></v-progress-circular>

          <p v-if="!chats.length && !loadingMedia" class="text-center">
            No comments yet
          </p>
          <p v-if="media && media.chat_count" class="text-center">
            {{ media.chat_count }} Chats
          </p>

          <div ref="chatContainer" v-if="chats.length" class="chats-container">
            <v-card
              v-for="chat in chats"
              :key="chat.id"
              class="chat-card mb-3"
            >
              <v-card-title class="chat-header">
                <v-avatar size="32" class="mr-2">
                  <v-img 
                    :src="chat.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(chat.owner_full_name)}`"
                    alt="user avatar"
                    height="32"
                    width="32"
                    aspect-ratio="1"
                    class="rounded-circle"
                  />
                </v-avatar>
                <span class="chat-owner">{{ chat.owner_full_name }}</span>
              </v-card-title>
              <v-card-text class="chat-content">
                {{ chat.content }}
              </v-card-text>
            </v-card>
          </div>

          <v-form v-if="media" @submit.prevent="submitChat" class="chat-form">
            <v-textarea
              v-model="newChat"
              label="Add a chat"
              outlined
              rows="2"
              required
              class="mb-2"
            ></v-textarea>
            <v-btn type="submit" color="primary" :disabled="isSubmitting">
              Post Chat
            </v-btn>
          </v-form>
        </div>
      </v-col>
    </v-row>

    <v-snackbar
      v-model="snackbar.visible"
      :timeout="snackbar.timeout"
      :color="snackbar.color"
    >
      {{ snackbar.message }}
      <v-btn color="white" text @click="snackbar.visible = false">
        Close
      </v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
export default {
  name: "MediaDetail",
  data() {
    return {
      media: null,
      chats: [],
      newChat: "",
      isSubmitting: false,
      loadingMedia: true,
      snackbar: {
        visible: false,
        message: "",
        color: "success",
        timeout: 3000,
      },
    };
  },
  async created() {
    await this.fetchMedia();
  },
  methods: {
    isImage(filePath) {
      return /\.(jpeg|jpg|gif|png)$/.test(filePath);
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.chatContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
    async fetchMedia() {
      const mediaId = this.$route.params.medias_id;
      try {
        const response = await this.$axios.get(`/medias/${mediaId}/chats/`);
        console.log("Media Response:", response.data);
        this.media = response.data;
        this.chats = response.data.chats || [];
      } catch (error) {
        console.error("Error fetching media:", error);
        this.snackbar.message = "Failed to fetch media, please try again.";
        this.snackbar.color = "error";
        this.snackbar.visible = true;
      } finally {
        this.loadingMedia = false;
      }
    },
    async submitChat() {
      if (this.newChat.trim()) {
        this.isSubmitting = true;
        const mediaId = this.$route.params.medias_id;
        try {
          const response = await this.$axios.post(`/medias/${mediaId}/chats/`, {
            content: this.newChat,
          });
          this.chats.push(response.data);
          if (this.media.chat_count !== undefined) {
            this.media.chat_count++;
          }
          this.newChat = "";
          this.scrollToBottom();
        } catch (error) {
          console.error("Error posting chat:", error);
          this.snackbar.message =
            "Failed to post your chat, please try again.";
          this.snackbar.color = "error";
          this.snackbar.visible = true;
        } finally {
          this.isSubmitting = false;
        }
      } else {
        alert("Please enter a chat before submitting.");
      }
    },
  },
  watch: {
    chats() {
      this.scrollToBottom();
    },
  },
};
</script>

<style scoped>

.media-details {
  margin-bottom: 2rem;
}

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

.chat-area {
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem;
}

.chats-container {
  margin-top: 1rem;
  max-height: 400px;
  overflow-y: auto;
  padding: 0.5rem;
  background: #f9f9f9;
  border-radius: 8px;
}

.chat-card {
  border-radius: 8px;
  padding: 0;
  width: 100%;
  max-width: 600px;
  margin: .5rem auto;
  display: block;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s;
}

.chat-card:hover {
  transform: scale(1.03);
  transform-origin: center;
}

.chat-header {
  display: flex;
  align-items: center;
  background-color: #eeeeee;
  padding: 0.5rem 1rem;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.chat-owner {
  font-size: 0.9rem;
  font-weight: 500;
  color: #333;
}

.chat-content {
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  line-height: 1.3;
  word-break: break-word;
}

.chat-form {
  margin-top: 1rem;
}
</style>
