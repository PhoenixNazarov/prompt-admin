<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt, usePromptStore} from "../../../stores/prompt.store.ts";
import MappingItem from "./MappingItem.vue";

export default defineComponent({
  name: "PromptList",
  components: {MappingItem},
  setup() {
    const promptStore = usePromptStore()
    return {
      promptStore
    }
  },
  props: {
    prompts: {
      type: Object as PropType<Prompt[]>
    },
    tableName: {
      type: String,
      default: 'PROMPTS'
    },
  },
  data() {
    return {
      headers: [
        {title: 'Mapping Id', key: 'mapping_id'},
        {title: 'Table', key: 'table'},
        {title: 'Field', key: 'field'},
        {title: 'Name', key: 'name'}
      ]
    }
  }
})
</script>

<template>
  <VDataTable
      :headers="headers"
      :items="prompts ? prompts : promptStore.prompts"
      density="compact"
      variant="outlined"
      :loading="promptStore.loadings.loadAll"
  >
    <template v-slot:top>
      <VToolbar
          flat
          color="transparent"
          density="compact"
      >
        <VToolbarTitle>{{ tableName }}</VToolbarTitle>
      </VToolbar>
    </template>
    <template v-slot:loading>
      <VSkeletonLoader type="table-row@5"></VSkeletonLoader>
    </template>
  </VDataTable>
</template>

<style scoped>

</style>