<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "CodeText",
  props: {
    title: {
      type: String
    },
    code: {
      type: String
    },
    error: {
      type: String
    }
  }
})
</script>

<template>
  <VCard :title="title" variant="text">
    <VCardText>
      <div class="program-general" :class="{'program-error': code != undefined}" v-if="error">
        {{ error }}
      </div>
      <div class="program-general program" v-if="code">{{ code }}</div>
    </VCardText>
  </VCard>
</template>

<style scoped>
@import '/src/styles/hint.css';

.program-general {
  padding: 1rem;
  border-radius: 0.5rem;
  white-space: break-spaces;
}

.program-error {
  margin-bottom: 1rem;
}

.v-card-text {
  padding: 0;
}
</style>