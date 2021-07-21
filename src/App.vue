<template>
  <div id="app">
    <leitura/>
  </div>
</template>


<script>
import Leitura from "@/components/leitura";

export default {
  name: 'App',
  components: { Leitura },

  mounted() {
    this.$mqtt.subscribe('laura/#')
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
