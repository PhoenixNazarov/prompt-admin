<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {ChangeContextEvent, ImageSchema} from "../../types";
import DataElementSchemaMixin from "../Mixins/DataElementSchemaMixin.ts";

export default defineComponent({
  name: "ImageSchemaComponent",
  mixins: [DataElementSchemaMixin],
  data() {
    return {
      fileModel: undefined,
      format: undefined as undefined | string
    }
  },
  props: {
    componentSchema: {
      type: Object as PropType<ImageSchema>,
      required: true
    }
  },
  methods: {
    doWriteFile(file: File | undefined) {
      if (!file) return this.doWrite(undefined)
      const reader = new FileReader();
      reader.readAsDataURL(file)
      reader.onload = () => {
        const result = reader?.result
        if (result) {
          if (this.componentSchema.formatReference) {
            const format = result.split(';')[0].replace(/^(data:)/,"")
            const event: ChangeContextEvent = {
              eventType: 'change-context',
              contextKey: this.componentSchema.formatReference,
              value: format
            }
            this.doEmitEventSchema(event)
          }
          const bytes = result.split(',')[1]
          this.doWrite({type: 'bytes', value: bytes})
        }
      }
    },
    getFormat() {
      if (this.format) return this.format
      return 'image/png'
    }
  },
  mounted() {
    if (this.componentSchema.formatReference)
      this.format = this.doRenderContextText(this.componentSchema.formatReference)
  },
  watch: {
    componentContext: {
      handler() {
        if (this.componentSchema.formatReference)
          this.format = this.doRenderContextText(this.componentSchema.formatReference)
      },
      deep: true
    }
  }
})
</script>

<template>
  <VFileInput
      accept="image/*"
      v-model="fileModel"
      @update:model-value="doWriteFile"
  />
  <img
      v-if="(model as any)?.value"
      :src="`data:${getFormat()};base64,`+ (model as any).value"
      :height="componentSchema.size ? CONST_SCHEMA_COMPONENT.image_size[componentSchema.size] : CONST_SCHEMA_COMPONENT.image_size_default"
  />
  <img
      v-else-if="model"
      :src="`data:${getFormat()};base64,`+ model"
      :height="componentSchema.size ? CONST_SCHEMA_COMPONENT.image_size[componentSchema.size] : CONST_SCHEMA_COMPONENT.image_size_default"
  />
</template>

<style scoped>

</style>