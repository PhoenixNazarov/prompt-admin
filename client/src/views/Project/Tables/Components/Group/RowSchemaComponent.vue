<script lang="ts">
import {defineAsyncComponent, defineComponent, PropType} from 'vue'
import {RowSchema} from "../../types";
import GroupSchemaMixin from "../Mixins/GroupSchemaMixin.ts";

export default defineComponent({
  name: "RowSchemaComponent",
  mixins: [GroupSchemaMixin],
  components: {
    GroupBuilder: defineAsyncComponent(() => import("../Group/GroupBuilder.vue") as any),
  },
  props: {
    componentSchema: {
      type: Object as PropType<RowSchema>,
      required: true
    }
  }
})
</script>

<template>
  <VRow>
    <VCol v-if="componentSchema.wrapInColumn">
      <GroupBuilder
          v-for="component in componentSchema.components"
          :component-schema="component"
          :component-context="componentContext"
          :input-schema="inputSchema"
          @event-schema="doEmitEventSchema"
      />
    </VCol>
    <GroupBuilder
        v-else
        v-for="component in componentSchema.components"
        :component-schema="component"
        :component-context="componentContext"
        :input-schema="inputSchema"
        @event-schema="doEmitEventSchema"
    />
  </VRow>
</template>

<style scoped>

</style>