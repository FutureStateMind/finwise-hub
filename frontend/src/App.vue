<template>
  <div id="app">
    <Navigation v-if="showNavigation" />
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Navigation from './components/Navigation.vue';

export default {
  name: 'App',
  components: {
    Navigation
  },
  setup() {
    const route = useRoute();
    
    const showNavigation = computed(() => {
      return route.name !== 'Login' && route.name !== 'Register';
    });
    
    return {
      showNavigation
    };
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: #f5f7fa;
}

#app {
  min-height: 100vh;
}

main {
  min-height: calc(100vh - 70px);
}

h1, h2, h3, h4, h5, h6 {
  margin: 0;
}

p {
  margin: 0;
}
</style>
