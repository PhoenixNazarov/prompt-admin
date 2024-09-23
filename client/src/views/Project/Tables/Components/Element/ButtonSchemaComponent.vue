<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {ButtonSchema} from "../../types/button.ts";
import ComponentSchemaMixin from "../Mixins/ComponentSchemaMixin.ts";


export default defineComponent({
  name: "ButtonSchemaComponent",
  mixins: [ComponentSchemaMixin],
  props: {
    componentSchema: {
      type: Object as PropType<ButtonSchema>,
      required: true
    }
  },
  methods: {
    doClick() {
      this.doEmitEventSchema(JSON.parse(JSON.stringify(this.componentSchema.event)))
    }
  }
})
</script>

<template>
  <VBtn
      :text="componentSchema.text"
      :disabled="componentSchema.disabled"
      :color="componentSchema.color"
      @click.prevent="doClick"
  />
</template>

<style scoped>

</style>