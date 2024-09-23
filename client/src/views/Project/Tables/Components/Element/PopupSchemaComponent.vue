<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {ChangeContextEvent, ComponentContextSchema, PopupSchema, RenderReferenceEvent} from "../../types";
import UtilSchema from "../UtilSchema.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

export default defineComponent({
  name: "PopupSchemaComponent",
  components: {
    FontAwesomeIcon,
  },
  props: {
    componentSchema: {
      type: Object as PropType<PopupSchema>,
      required: true
    },
    componentContext: {
      type: Object as PropType<ComponentContextSchema>,
    }
  },
  data() {
    return {
      model: UtilSchema.renderReference(this.componentSchema.reference, this.componentContext),
      show: false
    }
  },
  methods: {
    doWrite(newModel: string) {
      const event: ChangeContextEvent = {
        eventType: 'change-context',
        contextKey: this.componentSchema.reference,
        value: newModel
      }
      this.$emit('event-schema', event)
    },
    doPopup() {
      const event: RenderReferenceEvent = {
        eventType: 'render-reference',
        name: this.componentSchema.name,
        overlay: 'popup',
        inputSchema: {
          inputType: 'select',
          reference: this.componentSchema.reference,
          targetColumn: this.componentSchema.targetColumn
        }
      }
      this.$emit('event-schema', event)
    }
  },
  watch: {
    componentContext: {
      handler() {
        this.model = UtilSchema.renderReference(this.componentSchema.reference, this.componentContext)
      },
      deep: true
    }
  }
})
</script>

<template>
  <VTextField
      v-model="model"
      :label="componentSchema.label"
      :hint="componentSchema.hint"
      :type="componentSchema.format"
      :persistent-hint="componentSchema.persistentHint"
      :disabled="componentSchema.disabled"
      density="compact"
      variant="outlined"
      append-icon="mdi-eye"
      @update:model-value="doWrite"
      @click:append="doPopup"
  />
</template>

<style scoped>

</style>