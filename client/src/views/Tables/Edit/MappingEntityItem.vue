<script lang="ts">
import {defineComponent} from 'vue'
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import SelectConnection from "./Components/SelectConnection.vue";
import OutputList from "./OutputList.vue";
import {useOutputStore} from "../../../stores/config/output.store.ts";
import PromptList from "./PromptList.vue";
import MacroList from "./MacroList.vue";
import InputList from "./InputList.vue";
import {useInputStore} from "../../../stores/config/input.store.ts";
import {useMacroStore} from "../../../stores/config/macro.store.ts";
import {RouterService} from "../../../plugins/router.ts";
import RemoveButton from "./Components/RemoveButton.vue";

export default defineComponent({
  name: "MappingEntityItem",
  components: {RemoveButton, InputList, MacroList, PromptList, OutputList, SelectConnection},
  setup() {
    const outputStore = useOutputStore()
    const inputStore = useInputStore()
    const macroStore = useMacroStore()
    const mappingEntityStore = useMappingEntityStore()
    return {
      outputStore,
      mappingEntityStore,
      inputStore,
      macroStore
    }
  },
  props: {
    id: {
      type: Number
    }
  },
  data() {
    const mappingEntityStore = useMappingEntityStore()
    const mappingEntity = mappingEntityStore.getById(this.id)
    return {
      connection_name: mappingEntity?.connection_name,
      table: mappingEntity?.table,
      field: mappingEntity?.field,
      name: mappingEntity?.name,
      mapping_id: mappingEntity?.mapping_id,
      entity: mappingEntity?.entity,
      entity_id: mappingEntity?.entity_id,

      loadingSave: false
    }
  },
  methods: {
    async save() {
      if (!this.entity || !this.entity_id) return
      this.loadingSave = true
      const result = await this.mappingEntityStore.save({
        connection_name: this.connection_name,
        table: this.table,
        field: this.field,
        name: this.name,
        mapping_id: this.mapping_id,
        entity: this.entity,
        entity_id: this.entity_id,
        id: this.id,
      })
      await RouterService.goToTableItem('output', result.id)
      this.loadingSave = false
    }
  }
})
</script>

<template>
  <VCard density="compact">
    <VCardTitle>
      MAPPING ENTITY
    </VCardTitle>
    <VCardText>
      <VRow>
        <VCol>
          <SelectConnection v-model="connection_name"/>
        </VCol>
        <VCol>
          <VTextField density="compact" clearable label="Table" v-model="table" variant="outlined"
                      hint="Linked table" persistent-hint/>
        </VCol>
        <VCol>
          <VTextField density="compact" clearable label="Mapping Id" v-model="mapping_id" variant="outlined"
                      hint="Linked prompt id" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VTextField density="compact" clearable label="Field" v-model="field" variant="outlined"
                      hint="Linked field" persistent-hint/>
        </VCol>
        <VCol>
          <VTextField density="compact" clearable label="Name" v-model="name" variant="outlined"
                      hint="Linked name" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VSelect density="compact" label="Type" v-model="entity" variant="outlined"
                   hint="Type mapping for prompts" persistent-hint
                   :items="['output', 'input', 'macro']"/>
        </VCol>
        <VCol>
          <VTextField density="compact" label="Mapping Entity Id" v-model="entity_id" variant="outlined"
                      hint="Linked mapping entity id" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VBtn :loading="loadingSave" class="mr-2" color="success" text="Save" @click.prevent="save"/>
          <RemoveButton v-if="id" :remove="() => mappingEntityStore.remove(id)" :title="`Mapping Entity #${id}`"
                        list-name="mapping-entity"/>
        </VCol>
      </VRow>
      <VRow v-if="entity_id">
        <VCol>
          <OutputList v-if="entity=='output'"
                      table-name="RELATED OUTPUT"
                      :create="false"
                      :outputs="outputStore.getByIds([entity_id])"
          />
          <MacroList v-if="entity=='macro'"
                     table-name="RELATED MACRO"
                     :create="false"
                     :macros="macroStore.getByIds([entity_id])"
          />
          <InputList v-if="entity=='input'"
                     table-name="RELATED INPUT"
                     :create="false"
                     :inputs="inputStore.getByIds([entity_id])"
          />
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <PromptList table-name="RELATED PROMPTS"
                      v-if="entity && entity_id"
                      :prompts="mappingEntityStore.getPromptsByMappingEntity({
                      connection_name,
                      table,
                      field,
                      name,
                      mapping_id,
                      entity,
                      entity_id,
                      })"/>
        </VCol>
      </VRow>


    </VCardText>
  </VCard>
</template>

<style scoped>

</style>