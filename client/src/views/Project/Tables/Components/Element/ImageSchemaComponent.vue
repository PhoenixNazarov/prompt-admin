<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {ImageSchema} from "../../types";
import DataElementSchemaMixin from "../Mixins/DataElementSchemaMixin.ts";

export default defineComponent({
  name: "ImageSchemaComponent",
  mixins: [DataElementSchemaMixin],
  data() {
    return {
      fileModel: undefined
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
        const bytes = reader?.result?.split(',')[1]
        this.doWrite(bytes)
      }
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
      v-if="model"
      :src="'data:image/png;base64,'+ model"
      :height="componentSchema.size ? CONST_SCHEMA_COMPONENT.image_size[componentSchema.size] : CONST_SCHEMA_COMPONENT.image_size_default"
  />
</template>

<style scoped>

</style>