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
      <h2>About Us</h2>
      <p>We are committed to bringing the best products and services to our users.</p>
    </section>

    <!-- Featured Section -->
    <section class="featured">
      <h2>Featured</h2>
      <div class="featured-items">
        <div v-for="item in featuredItems" :key="item.id" class="featured-item">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <button @click="learnMore(item)">Learn More</button>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section class="testimonials">
      <h2>What Our Users Say</h2>
      <div class="testimonial" v-for="testimonial in testimonials" :key="testimonial.id">
        <p>{{ testimonial.text }}</p>
        <small>— {{ testimonial.author }}</small>
      </div>
    </section>

    <!-- Call-to-Action Section -->
    <section class="cta-section">
      <h2>Ready to Join?</h2>
      <button @click="joinNow">Sign Up Now</button>
    </section>

    <!-- Footer -->
    <footer>
      <p>&copy; 2024 Our Platform. All Rights Reserved.</p>
      <div class="social-links">
        <a href="#" aria-label="Twitter">Twitter</a>
        <a href="#" aria-label="Facebook">Facebook</a>
        <a href="#" aria-label="LinkedIn">LinkedIn</a>
      </div>
    </footer>
  </div>
</template>


<script>
export default {
  name: "HomePage",
  data() {
    return {
      featuredItems: [
        { id: 1, title: "Item One", description: "Description of item one." },
        { id: 2, title: "Item Two", description: "Description of item two." },
      ],
      testimonials: [
        { id: 1, text: "This platform is amazing!", author: "John Doe" },
        { id: 2, text: "I had a wonderful experience.", author: "Jane Smith" },
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

.about, .featured, .testimonials, .cta-section {
  padding: 2rem;
  text-align: center;
}

.featured-items {
  display: flex;
  justify-content: space-around;
}

.featured-item {
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.testimonial {
  background-color: #fff;
  padding: 1rem;
  border: 1px solid #ddd;
  margin-bottom: 1rem;
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
