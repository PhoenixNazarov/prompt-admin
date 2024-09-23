<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {CheckboxSchema} from "../../types";
import DataElementSchemaMixin from "../Mixins/DataElementSchemaMixin.ts";

export default defineComponent({
  name: "CheckboxSchemaComponent",
  mixins: [DataElementSchemaMixin],
  props: {
    componentSchema: {
      type: Object as PropType<CheckboxSchema>,
      required: true
    }
  },
})
</script>

<template>
  <VCheckbox
      v-model="model"
      :label="doRenderContextText(componentSchema.label)"
      :hint="doRenderContextText(componentSchema.hint)"
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