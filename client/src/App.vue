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
  mounted() {
    this.accountStore.loadMe()
  },
})
</script>

<template>
  <div>
    <Authorization v-if="!accountStore.logged"/>
    <WorkplaceView v-else/>
  </div>
</template>

<style scoped>

</style>