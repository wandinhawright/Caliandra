<template>
  <div id="app">
    <Header v-if="!hideHeader" />
    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import Header from './components/Header.vue'

const route = useRoute()

// Hide header on login, register, and verification pages
const hideHeader = computed(() => {
  return route.meta.hideHeader === true
})
</script>

<style>
#app {
  min-height: 100vh;
  background: #fffedf;
}

main {
  flex: 1;
}
</style>
