<script lang="ts">
import {defineComponent} from 'vue'
import {usePromptStore} from "../../../../stores/prompt.store.ts";

export default defineComponent({
  name: "SelectConnection",
  props: ['modelValue'],
  emits: ['update:modelValue'],
  setup() {
    const promptStore = usePromptStore()
    return {
      promptStore
    }
  },
  mounted() {
    this.promptStore.connectionsLoadAll()
  },
  computed: {
    value: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    }
  }
})
</script>

<template>
  <VSelect density="compact" label="Connection" v-model="value" variant="outlined"
           hint="Project database" persistent-hint
           :items="promptStore.connections"/>
</template>

<style scoped>

</style>