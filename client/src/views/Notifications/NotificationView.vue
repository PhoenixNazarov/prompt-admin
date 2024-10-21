<script lang="ts">
import {defineComponent} from 'vue'
import {notifications} from "./NotificationService.ts";

export default defineComponent({
  name: "NotificationView",
  data() {
    return {
      queue: notifications,

      snackbar: true,
      text: 'test',
      timeout: 2000 as number | undefined
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
  >
    {{ text }}

    <template v-slot:actions>
      <v-btn
          color="pink"
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