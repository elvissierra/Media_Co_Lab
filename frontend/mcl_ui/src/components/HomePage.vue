<template>
  <div id="home">
    <v-container class="py-12">
      <!-- Hero Section -->
      <v-row class="align-center mb-12">
        <v-col cols="12" md="6">
          <div>
            <h1 class="text-h3 font-weight-bold mb-4">Media Co Lab</h1>
            <p class="text-h6 mb-6">
              Foster creativity and discussion on topics worldwide. Form teams, separate concerns, and evolve ideas together.
            </p>
            <v-btn
              @click="ctaAction"
              size="large"
              color="primary"
              variant="elevated"
            >
              Learn More
            </v-btn>
          </div>
        </v-col>
        <v-col cols="12" md="6">
          <v-img
            src="@/assets/giphy.gif"
            aspect-ratio="16/9"
            cover
            class="rounded-lg"
          ></v-img>
        </v-col>
      </v-row>

      <!-- About Section -->
      <v-row class="mb-12" ref="about_env">
        <v-col cols="12">
          <v-card elevation="0" class="bg-surface">
            <v-card-item>
              <div class="text-h4 font-weight-bold mb-4">About The Environment</div>
              <p class="text-body1 mb-0">
                We provide organizations and users the chance and tools to collaborate in a fluid, conscious environment.
                Users can bring up ideas, share thoughts on media subjects, and explore new perspectives. Media can be any
                type of file—images, videos, articles, voice notes, and more.
              </p>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>

      <!-- Features Section -->
      <v-row class="mb-12">
        <v-col cols="12">
          <h2 class="text-h4 font-weight-bold mb-8 text-center">Features</h2>
        </v-col>
        <v-col
          v-for="item in featuredItems"
          :key="item.id"
          cols="12"
          sm="6"
          md="3"
        >
          <v-card elevation="2" class="h-100 d-flex flex-column cursor-pointer hover-card">
            <v-card-item>
              <div class="text-h6 font-weight-bold mb-2">{{ item.title }}</div>
              <p class="text-body2 mb-4 flex-grow-1">{{ item.description }}</p>
              <v-btn
                @click="seeMore(item)"
                size="small"
                color="primary"
                variant="tonal"
              >
                View Feature
              </v-btn>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Feature Detail Modal -->
    <v-dialog v-model="showFeatureModal" max-width="600">
      <v-card v-if="selectedItem">
        <v-card-item>
          <div class="text-h5 font-weight-bold">{{ selectedItem.title }}</div>
        </v-card-item>
        <v-card-text>
          <v-img :src="selectedGif" alt="Feature GIF" aspect-ratio="16/9"></v-img>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            @click="closeGif"
            color="primary"
            variant="text"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- CTA Section -->
    <v-container class="py-12 bg-primary text-white">
      <v-row>
        <v-col cols="12" class="text-center">
          <h2 class="text-h4 font-weight-bold mb-6">Ready to Join?</h2>
          <v-btn
            @click="joinNow"
            size="large"
            color="white"
            variant="elevated"
          >
            Join Now
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>


<script>
export default {
  name: "HomePage",
  data() {
    return {
      selectedItem: null,
      selectedGif: null,
      showFeatureModal: false,
      featuredItems: [
        { id: 1, title: "Organizational layout", description: "Structured to provide a clean and clear pattern for anyone to start collaborating.", gifUrl: "/gifs/orgoverview.gif"},
        { id: 2, title: "Media discussions", description: "Have team discussions around media to help separate concerns and explore topics.", gifUrl: "/gifs/media.gif"},
        { id: 3, title: "Labeling & tagging", description: "Choose from preset types or create custom ones. Tags indicate priority and can be customized.", gifUrl: "/gifs/labels.gif"},
        { id: 4, title: "Team management", description: "Organize teams to separate discussions, brainstorm, and collaborate effectively.", gifUrl: "/gifs/teams.gif"},
      ],
    };
  },
  methods: {
    ctaAction() {
      this.$refs.about_env.$el.scrollIntoView({ behavior: 'smooth' });
    },
    seeMore(item) {
      this.selectedItem = item;
      this.selectedGif = item.gifUrl;
      this.showFeatureModal = true;
    },
    closeGif() {
      this.showFeatureModal = false;
      this.selectedItem = null;
      this.selectedGif = null;
    },
    joinNow() {
      this.$router.push({ name: 'UserRegister' });
    },
  },
};
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.cursor-pointer:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12) !important;
}

.hover-card {
  transition: all 0.3s ease;
}

.rounded-lg {
  border-radius: 12px;
}

#home {
  background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
}
</style>
