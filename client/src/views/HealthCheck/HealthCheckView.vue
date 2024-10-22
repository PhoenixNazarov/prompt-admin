<script lang="ts">
import {defineComponent} from 'vue'
import {useHealthCheckStore} from "../../stores/healthcheck.store.ts";
import HealthTargetView from "./HealthTargetView.vue";

export default defineComponent({
  name: "HealthCheckView",
  components: {HealthTargetView},
  setup() {
    const healthCheckStore = useHealthCheckStore()
    return {
      healthCheckStore
    }
  },
  async mounted() {
    await this.healthCheckStore.loadTargets()
  }
})
</script>

<template>
  <VContainer>
    <VCard>
      <VCardTitle>Health Monitor</VCardTitle>
      <VCardText>
        <VSkeletonLoader type="card" v-if="healthCheckStore.loadings.targets"/>

        <HealthTargetView v-else :health-target="target" v-for="target in healthCheckStore.targets"/>
      </VCardText>
    </VCard>
  </VContainer>
</template>

<style scoped>

</style>