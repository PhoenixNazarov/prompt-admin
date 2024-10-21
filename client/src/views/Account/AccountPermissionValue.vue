<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AccountPermissionValue",
  props: {
    label: {
      type: String,
      required: true
    },
    value: {
      type: Number
    },
    hint: {
      type: String
    }
  },
  data() {
    return {
      value_: this.value
    }
  }
})
</script>

<template>
  <VSelect
      :label="label"
      density="compact"
      :items="[0, 1, 2]"
      :model-value="value_"
      :hint="hint"
      :persistent-hint="true"
      class="mb-1"
      @update:model-value="el => {value_ = el; $emit('updateModel', el)}"
  ></VSelect>
</template>

<style scoped>

</style>