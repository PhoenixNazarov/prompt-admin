<script lang="ts">
import {defineAsyncComponent, defineComponent} from 'vue'
import {ComponentContextSchema, EventSchema} from "../../types";
import EventDispatcher from "../../EventDispatcher.ts";
import ComponentSchemaMixin from "../Mixins/ComponentSchemaMixin.ts";


export default defineComponent({
  name: "NavigationBuilder",
  mixins: [ComponentSchemaMixin],
  components: {
    ReferenceGroupSchemaComponent: defineAsyncComponent(() => import("./ReferenceGroupSchemaComponent.vue")),
  },
  data() {
    return {
      selfComponentContext: this.componentContext as ComponentContextSchema
    }
  },
  methods: {
    onEventSchema(event: EventSchema) {
      if (!EventDispatcher.onContextEvent(event, this.selfComponentContext)) {
        this.$emit('event-schema', event)
      }
    }
  }
})
</script>

<template>
  <ReferenceGroupSchemaComponent
      v-if="componentSchema.type == 'reference-window'"
      :component-schema="componentSchema"
      :component-context="selfComponentContext"
      @event-schema="onEventSchema"
  />
</template>

<style scoped>

</style>