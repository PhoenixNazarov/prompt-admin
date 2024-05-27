<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "PaButton",
  props: {
    text: String
  }
})
</script>

<template>
  <button>{{text}}</button>
</template>

<style scoped>

</style>