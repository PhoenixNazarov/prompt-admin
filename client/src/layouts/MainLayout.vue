<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "MainLayout"
})
</script>

<template>
  <div>
    <div class="header">
      <div class="name">Prompt Admin</div>
    </div>
    <div class="inner">
      <slot/>
    </div>
  </div>
</template>

<style scoped>
.header {
  height: 3rem;
  background-color: var(--color-5);
}

.name {
  color: var(--color-3);
  font-size: 1.5rem;
  text-transform: uppercase;
  font-weight: 600;
  padding: 0.35rem;
}

.inner {
  height: calc(100vh - 3rem);
  background-color: var(--color-3);
}

</style>