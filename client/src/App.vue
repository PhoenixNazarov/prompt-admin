<script lang="ts">
import {defineComponent} from 'vue'
import {RouterView} from 'vue-router'
import NotificationView from "./views/Notifications/NotificationView.vue";

export default defineComponent({
  name: "App",
  components: {NotificationView, RouterView}
})
</script>

<template>
  <RouterView/>
  <NotificationView/>
</template>

<style scoped>

</style>