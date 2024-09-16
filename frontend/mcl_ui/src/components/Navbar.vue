<template>
  <nav class="navbar">
    <ul class="navbar-list">
      <li><a href="/home">Home</a></li>
      <li><a href="/teams">Teams</a></li>
      <li><a href="/medias">Media</a></li>
    </ul>
  </nav>
</template>

  
  <script>
  export default {
    name: "Nav_bar",
  };
  </script>
  
  <style scoped>
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
  