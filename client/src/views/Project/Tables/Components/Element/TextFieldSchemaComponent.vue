<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {TextFieldSchema} from "../../types";
import ElementSchemaMixins from "../Mixins/DataElementSchemaMixin.ts";
import PopupElementSchema from "../Mixins/PopupElementSchema.ts";
import ListSchemaComponent from "../Group/ListSchemaComponent.vue";

export default defineComponent({
  name: "TextFieldSchemaComponent",
  components: {ListSchemaComponent},
  mixins: [ElementSchemaMixins, PopupElementSchema],
  props: {
    componentSchema: {
      type: Object as PropType<TextFieldSchema>,
      required: true
    }
  }
})
</script>

<template>
  <VTextField
      v-model="model"
      :label="doRenderContextText(componentSchema.label)"
      :hint="doRenderContextText(componentSchema.hint)"
      :type="componentSchema.format"
      :persistent-hint="componentSchema.persistentHint"
      :disabled="componentSchema.disabled"
      :hide-details="componentSchema.hideDetails"
      :color="changeColor()"
      :base-color="changeColor()"
      density="compact"
      variant="outlined"
      @update:model-value="doWrite"

      :append-icon="componentSchema.popup ? 'mdi-eye' : ''"
      @click:append="doPopup"
  />
  <VDialog v-model="popupShow" v-if="componentSchema.popup?.listSchema">
    <ListSchemaComponent
        :component-schema="componentSchema.popup?.listSchema"
        :component-context="componentContext"
        :input-schema="popupInputSchema"
        @event-schema="doPopupEvent"
    />
  </VDialog>
</template>

<style scoped>

</style>