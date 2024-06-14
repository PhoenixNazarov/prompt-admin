<script lang="ts">
import {defineComponent} from 'vue'
import WorkplaceView from "./views/Workplace/WorkplaceView.vue";
import {useAccountStore} from "./stores/user.store.ts";
import Authorization from "./views/Authorization.vue";
import FormatView from "./views/Format/FormatView.vue";

export default defineComponent({
  name: "App",
  components: {FormatView, Authorization, WorkplaceView},
  setup() {
    const accountStore = useAccountStore()
    return {
      accountStore
    }
  },
  data() {
    return {
      loading: true,
      view: 'workplace'
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
    <Authorization v-else-if="!accountStore.logged"/>
    <WorkplaceView v-else-if="view == 'workplace'" @setView="(v: string) => view=v"/>
    <FormatView v-else-if="view == 'format'" @setView="(v: string) => view=v"/>
  </div>
</template>

<style scoped>

</style>