<script lang="ts">
import {defineComponent} from 'vue'
import WorkplaceView from "./views/Workplace/WorkplaceView.vue";
import {useAccountStore} from "./stores/user.store.ts";
import Authorization from "./views/Authorization.vue";

export default defineComponent({
  name: "App",
  components: {Authorization, WorkplaceView},
  setup() {
    const accountStore = useAccountStore()
    return {
      accountStore
    }
  },
  data() {
    return {
      loading: true
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
  <div>
    <div v-if="loading">
      Loading...
    </div>
    <Authorization v-if="!accountStore.logged"/>
    <WorkplaceView v-else/>
  </div>
</template>

<style scoped>

</style>