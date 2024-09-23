<script lang="ts">
import {defineComponent, PropType} from 'vue'
import ElementSchemaMixins from "../Mixins/DataElementSchemaMixin.ts";
import {DateSchema} from "../../types";
import DatePicker from "primevue/datepicker";
import FloatLabel from "primevue/floatlabel";

export default defineComponent({
  name: "DateSchemaComponent",
  mixins: [ElementSchemaMixins],
  components: {DatePicker, FloatLabel},
  props: {
    componentSchema: {
      type: Object as PropType<DateSchema>,
      required: true
    }
  },
  data() {
    return {
      on: false
    }
  },
  watch: {
    model(newVal) {
      this.doWrite(newVal)
    }
  }
})
</script>

<template>
  <FloatLabel>
    <label for="dateSchema" class="font-bold block mb-2"> {{ doRenderContextText(componentSchema.label) }}: </label>
    <DatePicker
        inputId="dateSchema"
        v-model="model"
        :disabled="componentSchema.disabled"
        :hide-details="componentSchema.hideDetails"
        :color="changeColor()"
        :base-color="changeColor()"
        density="compact"
        variant="outlined"
    />
  </FloatLabel>
</template>

<style scoped>

</style>