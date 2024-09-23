<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {ComponentContextSchema, EventSchema, GroupElementSchema, InputSchema} from "../../types";
import ElementBuilder from "../Element/ElementBuilder.vue";

export default defineComponent({
  name: "GroupElementSchemaComponent",
  components: {ElementBuilder},
  props: {
    componentSchema: {
      type: Object as PropType<GroupElementSchema>,
      required: true
    },
    componentContext: {
      type: Object as PropType<ComponentContextSchema>,
    },
    inputSchema: {
      type: Object as PropType<InputSchema>
    }
  },
  methods: {
    onEventSchema(event: EventSchema) {
      this.$emit('event-schema', event)
    }
  }
})
</script>

<template>
  <ElementBuilder
      :component-schema="componentSchema.element"
      :component-context="componentContext"
      @event-schema="onEventSchema"
  />
</template>

<style scoped>

</style>