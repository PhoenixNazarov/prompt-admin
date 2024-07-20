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
    },
    connection_name: {
      type: String
    },
    entity: {
      type: String
    },
    entity_id: {
      type: Number
    },
    table: {
      type: String
    },
    field: {
      type: String
    },
    name: {
      type: String
    }
  },
  data() {
    const mappingEntityStore = useMappingEntityStore()
    const mappingEntity = mappingEntityStore.getById(this.id)
    return {
      connection_name_: mappingEntity?.connection_name ? mappingEntity?.connection_name : this.connection_name,
      table_: mappingEntity?.table ? mappingEntity?.table : this.table,
      field_: mappingEntity?.field ? mappingEntity?.field : this.field,
      name_: mappingEntity?.name ? mappingEntity?.name : this.name,
      mapping_id: mappingEntity?.mapping_id,
      entity_: mappingEntity?.entity ? mappingEntity?.entity : this.entity,
      entity_id_: mappingEntity?.entity_id ? mappingEntity?.entity_id : this.entity_id,

      loadingSave: false
    }
  },
  methods: {
    async save() {
      if (!this.entity_ || !this.entity_id_) return
      this.loadingSave = true
      const result = await this.mappingEntityStore.save({
        connection_name: this.connection_name_,
        table: this.table_,
        field: this.field_,
        name: this.name_,
        mapping_id: this.mapping_id,
        entity: this.entity_,
        entity_id: this.entity_id_,
        id: this.id,
      })
      await RouterService.goToTableItem('mapping-entity', result.id)
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
          <SelectConnection v-model="connection_name_"/>
        </VCol>
        <VCol>
          <VTextField density="compact" clearable label="Table" v-model="table_" variant="outlined"
                      hint="Linked table" persistent-hint/>
        </VCol>
        <VCol>
          <VTextField density="compact" clearable label="Mapping Id" v-model="mapping_id" variant="outlined"
                      hint="Linked prompt id" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VTextField density="compact" clearable label="Field" v-model="field_" variant="outlined"
                      hint="Linked field" persistent-hint/>
        </VCol>
        <VCol>
          <VTextField density="compact" clearable label="Name" v-model="name_" variant="outlined"
                      hint="Linked name" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VSelect density="compact" label="Type" v-model="entity_" variant="outlined"
                   hint="Type mapping for prompts" persistent-hint
                   :items="['output', 'input', 'macro']"/>
        </VCol>
        <VCol>
          <VTextField density="compact" label="Mapping Entity Id" v-model="entity_id_" variant="outlined"
                      hint="Linked mapping entity id" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VBtn :loading="loadingSave" class="mr-2" color="success" :text="id ? 'Save' : 'Create'"
                @click.prevent="save"/>
          <RemoveButton v-if="id" :remove="() => mappingEntityStore.remove(id)" :title="`Mapping Entity #${id}`"
                        list-name="mapping-entity"/>
        </VCol>
      </VRow>
      <VRow v-if="entity_id_">
        <VCol>
          <OutputList v-if="entity_=='output'"
                      table-name="RELATED OUTPUT"
                      :create="false"
                      :outputs="outputStore.getByIds([entity_id_])"
          />
          <MacroList v-if="entity_=='macro'"
                     table-name="RELATED MACRO"
                     :create="false"
                     :macros="macroStore.getByIds([entity_id_])"
          />
          <InputList v-if="entity_=='input'"
                     table-name="RELATED INPUT"
                     :create="false"
                     :inputs="inputStore.getByIds([entity_id_])"
          />
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <PromptList table-name="RELATED PROMPTS"
                      v-if="entity_ && entity_id_"
                      :prompts="mappingEntityStore.getPromptsByMappingEntity({
                      connection_name : connection_name_,
                      table: table_,
                      field: field_,
                      name: name_,
                      mapping_id,
                      entity: entity_,
                      entity_id: entity_id_,
                      })"/>
        </VCol>
      </VRow>


    </VCardText>
  </VCard>
</template>

<style scoped>

</style>