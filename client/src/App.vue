<script lang="ts">
import {defineComponent} from 'vue'
import {RouterView} from 'vue-router'
import SchemaJsonView from "./views/SchemaJsonView.vue";

export default defineComponent({
  name: "App",
  components: {SchemaJsonView, RouterView}
})
</script>

<template>
  <RouterView/>
</template>

<style scoped>

</style>