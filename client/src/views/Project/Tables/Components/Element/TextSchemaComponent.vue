<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {TextSchema} from "../../types";
import ComponentSchemaMixin from "../Mixins/ComponentSchemaMixin.ts";

export default defineComponent({
  name: "TextSchemaComponentComponent",
  mixins: [ComponentSchemaMixin],
  props: {
    componentSchema: {
      type: Object as PropType<TextSchema>,
      required: true
    }
  }
})
</script>

<template>
  <div :class="[
      componentSchema.typography,
      componentSchema.textCenter ? 'text-center' : '',
      componentSchema.bold ? 'font-weight-bold' : ''
      ]">
    {{ doRenderContextText(componentSchema.text) }}
  </div>
</template>

<style scoped>

</style>