<script lang="ts">
import {defineComponent} from 'vue'
import {useOutputStore} from "../../../stores/config/output.store.ts";
import MappingEntityList from "./MappingEntityList.vue";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {RouterService} from "../../../plugins/router.ts";
import RemoveButton from "./Components/RemoveButton.vue";

export default defineComponent({
  name: "OutputItem",
  components: {RemoveButton, MappingEntityList},
  props: {
    id: {
      type: Number
    }
  },
  setup() {
    const mappingEntityStore = useMappingEntityStore()
    const outputStore = useOutputStore()
    return {
      mappingEntityStore,
      outputStore
    }
  },
  data() {
    const outputStore = useOutputStore()
    const output = outputStore.getById(this.id)
    return {
      output: output?.output,

      loadingSave: false
    }
  },
  methods: {
    async save() {
      if (!this.output) return
      this.loadingSave = true
      const result = await this.outputStore.save({id: this.id, output: this.output})
      await RouterService.goToTableItem('output', result.id)
      this.loadingSave = false
    }
  }
})
</script>

<template>
  <VCard density="compact">
    <VCardTitle>
      OUTPUT
    </VCardTitle>
    <VCardText>
      <VRow>
        <VCol>
          <VTextarea density="compact" label="Output" v-model="output" variant="outlined"
                     hint="Output format for prompts" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VBtn :loading="loadingSave" class="mr-2" color="success" text="Save" @click.prevent="save"/>
          <RemoveButton v-if="id" :remove="() => outputStore.remove(id)" :title="`Output #${id}`" :text="output"
                        list-name="output"/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <MappingEntityList :create="false" table-name="BOUND MAPPING ENTITIES"
                             :mappings-entity="mappingEntityStore.getMappingEntityByEntity('output', id)"/>
        </VCol>
      </VRow>
    </VCardText>
  </VCard>
</template>

<style scoped>

</style>