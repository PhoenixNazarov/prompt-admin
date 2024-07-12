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
  <h1>{{ title }}</h1>
  <div class="program-general program-error" v-if="error">
    {{ error }}
  </div>
  <div class="program-general program" v-if="code">{{ code }}</div>
</template>

<style scoped>
@import '/src/styles/hint.css';
.program-general {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-left: 1rem;
  margin-right: 1rem;
  white-space: break-spaces;
}
.program-error {
  margin-bottom: 1rem;
}
</style>