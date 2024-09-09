<template>
  <div id="app">
    <HomePage />
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Page from './components/Page.vue'
import Navbar from './components/Navbar.vue'

export default {
  name: 'App',
  components: {
    HomePage,
    Navbar,
  }
}
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
</style>
