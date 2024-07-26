<script lang="ts">
import {defineComponent} from 'vue'
import JsonEditorVue from 'json-editor-vue'

export default defineComponent({
  name: "SchemaJsonView",
  components: {
    JsonEditorVue
  },
  data() {
    return {
      schema: {"user_context": {"user": {"name": "YNmrXhHeRyJYkUYPRZKg", "ha": "RhJYwfweVpzfZZbQqSTU", "test": "RhJYwfweVpzfZZbQqSTUtest"}, "coach": {"name": "vtnNvSNuqVcltRMDBPZG"}}, "user_context2": {"user": {"name": "YNmrXhHeRyJYkUYPRZKg", "ha": "RhJYwfweVpzfZZbQqSTU", "test": "RhJYwfweVpzfZZbQqSTUtest"}, "coach": {"name": "vtnNvSNuqVcltRMDBPZG"}}}
      ,
    }
  }
})
</script>

<template>
  <JsonEditorVue v-model="schema"/>
</template>

<style scoped>
</style>