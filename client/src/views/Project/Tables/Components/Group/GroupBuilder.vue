<script lang="ts">
import {defineAsyncComponent, defineComponent} from 'vue'
import ElementBuilder from "../Element/ElementBuilder.vue";
import GroupSchemaMixin from "../Mixins/GroupSchemaMixin.ts";

export default defineComponent({
  name: "GroupBuilder",
  mixins: [GroupSchemaMixin],
  components: {
    ElementBuilder,
    CardSchemaComponent: defineAsyncComponent(() => import("../Group/CardSchemaComponent.vue")),
    ListSchemaComponent: defineAsyncComponent(() => import("../Group/ListSchemaComponent.vue")),
    RowSchemaComponent: defineAsyncComponent(() => import("../Group/RowSchemaComponent.vue")),
    ColumnSchemaComponent: defineAsyncComponent(() => import("../Group/ColumnSchemaComponent.vue")),
  }
})
</script>

<template>
  <CardSchemaComponent
      v-if="componentSchema.type =='card'"
      :component-schema="componentSchema"
      :component-context="componentContext"
      :input-schema="inputSchema"
      @event-schema="doEmitEventSchema"
  />
  <ListSchemaComponent
      v-else-if="componentSchema.type =='list'"
      :component-schema="componentSchema"
      :component-context="componentContext"
      :input-schema="inputSchema"
      @event-schema="doEmitEventSchema"
  />
  <RowSchemaComponent
      v-else-if="componentSchema.type =='row'"
      :component-schema="componentSchema"
      :component-context="componentContext"
      :input-schema="inputSchema"
      @event-schema="doEmitEventSchema"
  />
  <ColumnSchemaComponent
      v-else-if="componentSchema.type =='column'"
      :component-schema="componentSchema"
      :component-context="componentContext"
      :input-schema="inputSchema"
      @event-schema="doEmitEventSchema"
  />
  <ElementBuilder
      v-else
      :component-schema="componentSchema"
      :component-context="componentContext"
      @event-schema="doEmitEventSchema"
  />
</template>

<style scoped>

</style>