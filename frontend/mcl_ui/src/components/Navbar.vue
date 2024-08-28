<template>
    <nav class="navbar">
      <ul>
        <li><a href="/home-page/">Home</a></li>
        <li><a href="/teams/">Teams</a></li>
        <li><a href="/media/">Media</a></li>
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
  
  .navbar ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    display: flex;
    justify-content: space-around;
  }
  
  .navbar ul li {
    display: inline;
  }
  
  .navbar ul li a {
    color: white;
    text-decoration: none;
    font-size: 1.2em;
  }
  
  .navbar ul li a:hover {
    text-decoration: underline;
  }
  </style>
  