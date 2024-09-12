<template>
  <div id="home">

    <!-- About Section -->
    <section class="about">
      <h2>What we do here:</h2>
      <p>Welcome to Media_co_Lab, where we foster creativity and discussion on topics world wide.
        Form teams and seperate topics to more clearly identify interests, and evolve ideas!
      </p>
    </section>

    <!-- Hero Section -->
    <section class="hero">
      <button @click="ctaAction">Learn More</button>
    </section>

    <!-- About Section -->
    <section ref="about_env" class="target-section">
      <h2>About The Environment:</h2>
      <p>To provide organizations and regular users the chance and tools to collaborate in a fluid
         and conscious environment. Users can bring up ideas, share thoughts on media subjects, 
         and explore new views on present-day media. Media can be any type of file—images, videos,
          articles, voice notes, etc.</p>
    </section>

    <!-- Features Section -->
    <section class="features">
      <h2>Features</h2>
      <div class="feature-items">
        <div v-for="item in featuredItems" :key="item.id" class="featured-item">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <button @click="seeMore(item)"> View Feature </button>
        </div>
      </div>

        <!-- Section to display the GIF -->
      <div v-if="selectedItem" class="gif-display">
        <h3>{{ selectedItem.title }}</h3>
        <img :src="selectedGif" alt="Feature GIF">
        <button @click="closeGif">Close</button>
      </div>

    </section>

    <!-- Call-to-Action Section -->
    <section class="cta-section">
      <h2>Ready to Join?</h2>
      <button @click="joinNow">Join Now</button>
    </section>

    <!-- Footer -->
    <footer>

    </footer>
  </div>
</template>


<script>
export default {
  name: "HomePage",
  data() {
    return {
      selectedItem: null, // Will hold the selected feature item
      selectedGif: null,  // Will hold the URL of the GIF
      featuredItems: [
        { id: 1, title: "Organizational layout", description: "Structured to provide a clean and clear pattern for anyone to start co_lab-ing." },
        { id: 2, title: "Media discussions", description: "Have team discussions around media to help seperate concerns." },
        { id: 3, title: "Labeling type", description: "Type can be chosen from a preset list or create a new type to fit your needs." },
        { id: 4, title: "Labeling tag", description: "Tags are designed to indicate a level of priority." },
      ],
    };
  },
  methods: {
    ctaAction() {
      this.$refs.about_env.scrollIntoView({behavior: 'smooth'}); /* tbc scroll down to ATE */
    },
    seeMore(item) {
      this.seletedItem = item;
      this.selectedGif = item.gifUrl;
    },
    closeGif() {
      this.selectedItem = null;
      this.selectedGif = null;
    },
    joinNow() {
      alert("Signing you up...");
    },
  },
};
</script>

<style scoped>
/* Styling for the homepage sections */

.navbar {
  background: #333;
  color: white;
  padding: 1rem;
}

.navbar ul {
  display: flex;
  list-style: none;
  justify-content: space-around;
}

.navbar a {
  color: white;
  text-decoration: none;
}

.hero {
  background: url("@/assets/giphy.gif") no-repeat center center;
  background-size: cover;
  height: 60vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  padding: 2rem; /* Add some padding to the hero section */
}

.hero button {
  background-color: #ff5722;
  color: white;
  padding: 1rem 2rem;
  border: none;
  cursor: pointer;
  font-size: 1.25rem;
  border-radius: 30px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease, transform 0.3s ease;
  margin-top: auto;
}

.about, .features, .cta-section {
  padding: 2rem;
  text-align: center;
}

.feature-items {
  display: flex;
  justify-content: space-around;
  align-items: stretch;
  gap: 1rem;
  flex-wrap: wrap;
}

.featured-item {
  flex: 1 1 45%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1rem;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #f9f9f9;
}

.gif-display {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.gif-display img {
  max-width: 100%;
  height: auto;
}

.gif-display button {
  margin-top: 10px;
  background-color: #ff5722;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  cursor: pointer;
}

@media (max-width: 768px) {
  .featured-item {
    flex: 1 1 100%;
  }
}


.cta-section {
  background-color: #4caf50;
  color: white;
}

.cta-section button {
  background-color: #ff5722;
  color: white;
  padding: 1rem 2rem;
  border: none;
  cursor: pointer;
  font-size: 1.25rem;
  border-radius: 30px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease, transform 0.3s ease;
  margin-top: auto;
}

footer {
  background-color: #333;
  color: white;
  padding: 1rem;
  text-align: center;
}

.social-links a {
  margin: 0 10px;
  color: white;
  text-decoration: none;
}
</style>
