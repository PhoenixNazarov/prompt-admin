<script lang="ts">
import {defineComponent} from 'vue'
import {notifications} from "./NotificationService.ts";

export default defineComponent({
  name: "NotificationView",
  data() {
    return {
      queue: notifications,

      snackbar: false,
      text: '',
      timeout: 0 as number | undefined,
      level: ''
    }
  },
  methods: {
    popNotification() {
      if (this.snackbar || this.queue.length <= 0) {
        return
      }

      const notifications = this.queue.pop()
      if (!notifications) return;

      this.snackbar = true
      this.text = notifications.message
      this.timeout = notifications.timeout
      this.level = notifications.level
    }
  },
  watch: {
    queue: {
      handler() {
        this.popNotification()
      },
      deep: true
    },
    snackbar() {
      this.popNotification()
    }
  }
})
</script>

<template>
  <VSnackbar
      v-model="snackbar"
      :timeout="timeout"
      :color="level"
  >
    {{ text }}

    <template v-slot:actions>
      <v-btn
          variant="text"
          @click="snackbar = false"
      >
        Close
      </v-btn>
    </template>
  </VSnackbar>
</template>

<style scoped>

</style>