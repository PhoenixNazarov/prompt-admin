<script lang="ts">
import {defineComponent} from 'vue'
import MappingEntityList from "./MappingEntityList.vue";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {useMacroStore} from "../../../stores/config/macro.store.ts";
import {RouterService} from "../../../plugins/router.ts";
import RemoveButton from "./Components/RemoveButton.vue";

export default defineComponent({
  name: "MacroItem",
  components: {RemoveButton, MappingEntityList},
  props: {
    id: {
      type: Number
    }
  },
  setup() {
    const mappingEntityStore = useMappingEntityStore()
    const macroStore = useMacroStore()
    return {
      macroStore,
      mappingEntityStore
    }
  },
  data() {
    const macroStore = useMacroStore()
    const macro = macroStore.getById(this.id)
    return {
      macro: macro?.macro,
      macro_value: macro?.macro_value,
      description: macro?.description,

      loadingSave: false
    }
  },
  methods: {
    async save() {
      if (!this.macro || !this.macro_value || !this.description) return
      this.loadingSave = true
      const result = await this.macroStore.save({
        id: this.id,
        macro: this.macro,
        macro_value: this.macro_value,
        description: this.description,
      })
      await RouterService.goToTableItem('macro', result.id)
      this.loadingSave = false
    }
  }
})
</script>

<template>
  <VCard density="compact">
    <VCardTitle>
      MACRO
    </VCardTitle>
    <VCardText>
      <VRow>
        <VCol>
          <VTextField density="compact" label="Macro" v-model="macro" variant="outlined"
                      hint="Macro" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VTextarea density="compact" label="Macro value" v-model="macro_value" variant="outlined"
                     hint="Macro value" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VTextarea density="compact" label="Description" v-model="description" variant="outlined"
                     hint="Description" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VBtn :loading="loadingSave" class="mr-2" color="success" text="Save" @click.prevent="save"/>
          <RemoveButton v-if="id" :remove="() => macroStore.remove(id)" :title="`Macro #${id}`"
                        list-name="mapping-entity"/>
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