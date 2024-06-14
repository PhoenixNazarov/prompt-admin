<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

export default defineComponent({
  name: "ConsistentReportCase",
  components: {FontAwesomeIcon},
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: Object as PropType<boolean | null>
    }
  }
})
</script>

<template>
  <h2>
    <FontAwesomeIcon v-if="value != null && value" icon="check"/>
    <FontAwesomeIcon v-if="value != null && !value" icon="xmark" class="xmark"/>
    {{ title }}
  </h2>
</template>

<style scoped>
@import '/src/styles/hint.css';

.xmark {
  color: var(--color-2)
}

</style>