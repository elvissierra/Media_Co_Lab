<template>
    <div class="/home">
      <h1>Welcome to Media Co lab!</h1>
      <p>Start to MCL!</p>
    </div>
  </template>
  
  <script>
  export default {
    name: "Home",
    data() {
            return {
                message: "Home is a work in progress as we all are!",
            };
        },
    
  };
  </script>
  
    
    <style scoped>
    .home {
      text-align: center;
      margin-top: 50px;
    }
    
    h1 {
      font-size: 2.5em;
      color: #42b983;
    }
    
    p {
      font-size: 1.2em;
    }
    </style>
    