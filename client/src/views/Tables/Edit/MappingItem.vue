<script lang="ts">
import {defineComponent} from 'vue'
import {useMappingStore} from "../../../stores/config/mapping.store.ts";
import SelectConnection from "./Components/SelectConnection.vue";
import OutputList from "./OutputList.vue";
import MappingEntityList from "./MappingEntityList.vue";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {RouterService} from "../../../plugins/router.ts";
import RemoveButton from "./Components/RemoveButton.vue";

export default defineComponent({
  name: "MappingItem",
  components: {RemoveButton, MappingEntityList, OutputList, SelectConnection},
  setup() {
    const mappingStore = useMappingStore()
    const mappingEntityStore = useMappingEntityStore()
    return {
      mappingStore,
      mappingEntityStore
    }
  },
  props: {
    id: {
      type: Number
    }
  },
  data() {
    const mappingStore = useMappingStore()
    const mapping = mappingStore.getById(this.id)
    return {
      table: mapping?.table,
      field: mapping?.field,
      description: mapping?.description,
      field_name: mapping?.field_name,
      connection_name: mapping?.connection_name,
      field_order: mapping?.field_order,
      desc: mapping?.desc,

      loadingSave: false
    }
  },
  methods: {
    async save() {
      if (!this.table || !this.field || !this.description || !this.field_name || !this.connection_name) return
      this.loadingSave = true
      const result = await this.mappingStore.save({
        id: this.id,
        table: this.table,
        field: this.field,
        description: this.description,
        field_name: this.field_name,
        connection_name: this.connection_name,
        field_order: this.field_order,
        desc: this.desc
      })
      await RouterService.goToTableItem('mapping', result.id)
      this.loadingSave = false
    }
  }
})
</script>

<template>
  <VCard density="compact">
    <VCardTitle>
      MAPPING
    </VCardTitle>
    <VCardText>
      <VRow>
        <VCol>
          <SelectConnection v-model="connection_name"/>
        </VCol>
        <VCol>
          <VTextField density="compact" label="Table" v-model="table" variant="outlined"
                      hint="Table in database" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VTextField density="compact" label="Field" v-model="field" variant="outlined"
                      hint="Field of table in database" persistent-hint/>
        </VCol>
        <VCol>
          <VTextField density="compact" label="Field Name" v-model="field_name" variant="outlined"
                      hint="Display name for prompt row" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VTextarea density="compact" label="Description" v-model="description" variant="outlined"
                     hint="Description of the remote product" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VTextField density="compact" label="Order Field" v-model="field_order" variant="outlined"
                      hint="Field for sort" persistent-hint/>
        </VCol>
        <VCol>
          <VSwitch v-model="desc" label="Descending" density="compact"/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VBtn :loading="loadingSave" class="mr-2" color="success" text="Save" @click.prevent="save"/>
          <RemoveButton v-if="id" :remove="() => mappingStore.remove(id)" :title="`Mapping #${id}`"
                        list-name="mapping"/>
        </VCol>
      </VRow>
      <VRow>
        <MappingEntityList
            :mappings-entity="mappingEntityStore.getMappingEntityByMapping(connection_name, table, field)"/>
      </VRow>
    </VCardText>
  </VCard>
</template>

<style scoped>

</style>