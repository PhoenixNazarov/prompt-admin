<script lang="ts">
import {defineComponent} from 'vue'
import {RouterView} from 'vue-router'
import SchemaJsonView from "./views/SchemaJsonView.vue";
import NotificationView from "./views/Notifications/NotificationView.vue";

export default defineComponent({
  name: "App",
  components: {NotificationView, SchemaJsonView, RouterView}
})
</script>

<template>
  <RouterView/>
  <NotificationView/>
</template>

<style scoped>

</style>