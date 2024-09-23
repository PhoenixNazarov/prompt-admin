<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {TextAreaSchema} from "../../types";
import DataElementSchemaMixin from "../Mixins/DataElementSchemaMixin.ts";

export default defineComponent({
  name: "TextAreaSchemaComponent",
  mixins: [DataElementSchemaMixin],
  props: {
    componentSchema: {
      type: Object as PropType<TextAreaSchema>,
      required: true
    }
  }
})
</script>

<template>
  {{componentSchema.persistentHint}}
  <VTextarea
      v-model="model"
      :label="doRenderContextText(componentSchema.label)"
      :hint="doRenderContextText(componentSchema.hint)"
      :rows="componentSchema.rows"
      :persistent-hint="componentSchema.persistentHint"
      :disabled="componentSchema.disabled"
      :hide-details="componentSchema.hideDetails"
      :color="changeColor()"
      :base-color="changeColor()"
      density="compact"
      variant="outlined"
      @update:model-value="doWrite"
  />
</template>

<style scoped>

</style>