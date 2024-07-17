<script lang="ts">
import {defineComponent} from 'vue'
import {RouterView} from 'vue-router'
import {useAccountStore} from "./stores/user.store.ts";

export default defineComponent({
  name: "App",
  components: {RouterView},
  setup() {
    const accountStore = useAccountStore()
    return {
      accountStore
    }
  },
  data() {
    return {
      loading: true,
      view: 'table'
    }
  },
  async mounted() {
    this.loading = true
    try {
      await this.accountStore.loadMe()
    } catch (e) {
    }
    this.loading = false

  },
})
</script>

<template>
  <RouterView/>
</template>

<style scoped>

</style>