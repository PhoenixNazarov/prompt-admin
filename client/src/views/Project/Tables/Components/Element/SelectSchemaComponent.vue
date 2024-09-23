<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {SelectSchema} from "../../types";
import DataElementSchemaMixin from "../Mixins/DataElementSchemaMixin.ts";

export default defineComponent({
  name: "SelectSchemaComponent",
  mixins: [DataElementSchemaMixin],
  props: {
    componentSchema: {
      type: Object as PropType<SelectSchema>,
      required: true
    }
  }
})
</script>

<template>
  <VSelect
      v-model="model"
      :items="componentSchema.items"
      :label="doRenderContextText(componentSchema.label)"
      :hint="doRenderContextText(componentSchema.hint)"
      :persistent-hint="componentSchema.persistentHint"
      :disabled="componentSchema.disabled"
      :hide-details="componentSchema.hideDetails"
      :color="changeColor()"
      :base-color="changeColor()"
      density="compact"
      variant="outlined"
      @update:model-value="(el) => doWrite(el as string)"
  />
</template>

<style scoped>

</style>