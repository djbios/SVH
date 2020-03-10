<template>
  <div id="app">
<!--    <img alt="Vue logo" src="./assets/logo.png">-->
    <SvhApp/>
  </div>
</template>

<script>
import SvhApp from './components/SvhApp'

export default {
  name: 'app',
  components: {
    SvhApp
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
