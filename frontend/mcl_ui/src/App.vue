<template>
  <div class="header">
    <h1>Welcome to Media Co lab!</h1>

    <div v-if="!isLoggedIn">
      <button class="combined-button">
        <span @click="goToRegister">Register</span> /
        <span @click="loginUser">Login</span>
      </button>
    </div>
    <button v-if="isLoggedIn" @click="logoutUser">Logout</button>
  </div>

  <nav class="navbar">
    <ul class="navbar-list">
      <li><a href="/home">Home</a></li>
      <li><a href="/organizations/ov">Organization</a></li>
      <li><a href="/teams">Teams</a></li>
      <li><a href="/medias">Media</a></li>
    </ul>
  </nav>  
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: false,
    };
  },
  created() {
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
      this.isLoggedIn = !!localStorage.getItem('authToken');
    },
    async logoutUser() {
      try {
        await this.$axios.post('auth/logout/', {}, {
          headers: {
            'Authorization': `Token ${localStorage.getItem('authToken')}`,
          },
        });
        localStorage.removeItem('authToken');
        this.isLoggedIn = false; 
        this.$router.push({ name: 'UserLogin' });
      } catch (error) {
        console.error('Error on logout:', error);
      }
    },
    goToRegister() {
      this.$router.push({ name: 'UserRegister' });
    },
    loginUser() {
      this.$router.push({ name: 'UserLogin' });
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.top_page {
  text-align: center;
  margin-top: 50px;
}


.header {
  display: flex;
  flex-direction: column;
  justify-content: space-between; 
  align-items: center;
  padding: 0;
  margin: 0;
  position: relative;
}


.header button,
.combined-button {
  align-self: flex-end; 
  margin-top: auto; 
  background-color: #ff5722;
  color: white;
  padding: 1rem 2rem;
  border: none;
  cursor: pointer;
  border-radius: 8px 8px 0 0;
  font-weight: bold;
  display: inline-flex;
}

.combined-button {
  position: absolute;
  bottom: 0px; 
  right: 1px; 
}

.header button:hover,
.combined-button:hover {
  background-color: #e64a19; 
}


.combined-button span {
  cursor: pointer;
  text-decoration: underline; 
}

.combined-button span:hover {
  color: #fff;
}


h1 {
  text-align: center;
  font-size: 2.5em;
  color: #4caf50;
  margin-bottom: auto;
}


p {
  font-size: 1.2em;
}

.navbar {
    background-color: #333;
    padding: 10px;
    
  }
  
  .navbar {
  position: relative;
  background-color: #333;
  height: 60px; /* Set a specific height */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 2rem;
  color: white;
  margin: 0; /* Ensure no default margins */
  }

  .navbar-list {
  display: flex; /* Turns the list into a flex container */
  list-style: none; /* Removes bullet points */
  justify-content: space-between;
  width: 100%; /* Makes the list take the full width of the navbar */
  padding: 0;
  margin: 0;
  }

  .navbar-list li {
    margin: 0 20px; /* Adds spacing between the items */
  }

  .navbar-list li a {
    color: white;
    text-decoration: none;
    font-size: 1.2em;
    padding: 10px 20px;
  }

  .navbar-list li a:hover {
    background-color: #555;
    border-radius: 5px;
  }
</style>
