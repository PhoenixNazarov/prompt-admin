<script lang="ts">
import {defineAsyncComponent, defineComponent, PropType} from 'vue'
import {ColumnSchema} from "../../types";
import GroupSchemaMixin from "../Mixins/GroupSchemaMixin.ts";

export default defineComponent({
  name: "ColumnSchemaComponent",
  mixins: [GroupSchemaMixin],
  components: {
    GroupBuilder: defineAsyncComponent(() => import("../Group/GroupBuilder.vue") as any),
  },
  props: {
    componentSchema: {
      type: Object as PropType<ColumnSchema>,
      required: true
    }
  }
})
</script>

<template>
  <VCol
      :class="{
          'row-reverse': componentSchema.rowReverse
        }"
  >
    <GroupBuilder
        v-for="component in componentSchema.components"
        :component-schema="component"
        :component-context="componentContext"
        :input-schema="inputSchema"
        @event-schema="doEmitEventSchema"
    />
  </VCol>
</template>

<style scoped>
.row-reverse {
  display: flex;
  flex-direction: row-reverse;
}
</style>