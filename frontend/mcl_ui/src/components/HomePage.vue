<template>
  <div id="home">

    <!-- Hero Section -->
    <section class="hero">
      <h1>Welcome to Our Amazing Platform</h1>
      <p>Your journey to excellence starts here.</p>
      <button @click="ctaAction">Get Started</button>
    </section>

    <!-- About Section -->
    <section class="about">
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
          <button @click="learnMore(item)">Learn More</button>
        </div>
      </div>
    </section>

    <!-- Call-to-Action Section -->
    <section class="cta-section">
      <h2>Ready to Join?</h2>
      <button @click="joinNow">Sign Up Now</button>
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
      featuredItems: [
        { id: 1, title: "Labeling type", description: "Type can be chosen from a preset list or create a new type to fit your needs." },
        { id: 2, title: "Labeling tag", description: "Tags are designed to indicate a level of priority." },
      ],
    };
  },
  methods: {
    ctaAction() {
      alert("Navigating to get started!");
    },
    learnMore(item) {
      alert(`Learn more about ${item.title}`);
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
  background: url() no-repeat center center;
  background-size: cover;
  height: 60vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
}

.hero button {
  background-color: #ff5722;
  color: white;
  padding: 1rem 2rem;
  border: none;
  cursor: pointer;
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
}

.featured-item {
  flex: 1 1 45%;
  padding: 1rem;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #f9f9f9;
}

@media (max-width: 768px) {
  .featured-item {
    flex: 1 1 100%;
  }
}


.cta-section {
  background-color: #4caf50;
  color: white;
  padding: 2rem;
}

.cta-section button {
  background-color: #ff5722;
  color: white;
  padding: 1rem 2rem;
  border: none;
  cursor: pointer;
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
