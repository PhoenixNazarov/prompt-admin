<script lang="ts">
import {defineAsyncComponent, defineComponent, PropType} from 'vue'
import {ElementSchema} from "../../types";
import ComponentSchemaMixin from "../Mixins/ComponentSchemaMixin.ts";

export default defineComponent({
  name: "ElementBuilder",
  mixins: [ComponentSchemaMixin],
  props: {
    componentSchema: {
      type: Object as PropType<ElementSchema>,
      required: true
    }
  },
  components: {
    ButtonSchemaComponent: defineAsyncComponent(() => import("../Element/ButtonSchemaComponent.vue")),
    TextSchemaComponent: defineAsyncComponent(() => import("../Element/TextSchemaComponent.vue")),
    TextFieldSchemaComponent: defineAsyncComponent(() => import("./TextFieldSchemaComponent.vue")),
    TextAreaSchemaComponent: defineAsyncComponent(() => import("./TextAreaSchemaComponent.vue")),
    CheckboxSchemaComponent: defineAsyncComponent(() => import("./CheckboxSchemaComponent.vue")),
    // PopupSchemaComponent: defineAsyncComponent(() => import("./PopupSchemaComponent.vue")),
    // ItemRowSchemaComponent: defineAsyncComponent(() => import("./ItemRowSchemaComponent.vue")),
    SelectSchemaComponent: defineAsyncComponent(() => import("./SelectSchemaComponent.vue")),
    ImageSchemaComponent: defineAsyncComponent(() => import("./ImageSchemaComponent.vue")),
    DateSchemaComponent: defineAsyncComponent(() => import("./DateSchemaComponent.vue")),
  }
})
</script>

<template>
  <ButtonSchemaComponent
      v-if="componentSchema.type == 'button'"
      :component-schema="componentSchema"
      :component-context="componentContext"
      @event-schema="doEmitEventSchema"
  />
  <TextSchemaComponent
      v-if="componentSchema.type == 'text'"
      :component-schema="componentSchema"
      :component-context="componentContext"
      @event-schema="doEmitEventSchema"
  />
  <TextFieldSchemaComponent
      v-if="componentSchema.type == 'textField'"
      :component-schema="componentSchema"
      :component-context="componentContext"
      @event-schema="doEmitEventSchema"
  />
  <TextAreaSchemaComponent
      v-if="componentSchema.type == 'textArea'"
      :component-schema="componentSchema"
      :component-context="componentContext"
      @event-schema="doEmitEventSchema"
  />
  <CheckboxSchemaComponent
      v-if="componentSchema.type == 'checkbox'"
      :component-schema="componentSchema"
      :component-context="componentContext"
      @event-schema="doEmitEventSchema"
  />
  <!--  <PopupSchemaComponent-->
  <!--      v-if="componentSchema.type == 'popup'"-->
  <!--      :component-schema="componentSchema"-->
  <!--      :component-context="componentContext"-->
  <!--      @event-schema="onEventSchema"-->
  <!--  />-->
<!--  <ItemRowSchemaComponent-->
<!--      v-if="componentSchema.type == 'item-row'"-->
<!--      :component-schema="componentSchema"-->
<!--      :component-context="componentContext"-->
<!--      @event-schema="doEmitEventSchema"-->
<!--  />-->
  <SelectSchemaComponent
      v-if="componentSchema.type == 'select'"
      :component-schema="componentSchema"
      :component-context="componentContext"
      @event-schema="doEmitEventSchema"
  />
  <ImageSchemaComponent
      v-if="componentSchema.type == 'image'"
      :component-schema="componentSchema"
      :component-context="componentContext"
      @event-schema="doEmitEventSchema"
  />
  <DateSchemaComponent
      v-if="componentSchema.type == 'date'"
      :component-schema="componentSchema"
      :component-context="componentContext"
      @event-schema="doEmitEventSchema"
  />
</template>

<style scoped>

</style>