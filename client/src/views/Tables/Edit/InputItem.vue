<script lang="ts">
import {defineComponent} from 'vue'
import MappingEntityList from "./MappingEntityList.vue";
import {useInputStore} from "../../../stores/config/input.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {RouterService} from "../../../plugins/router.ts";
import RemoveButton from "./Components/RemoveButton.vue";

export default defineComponent({
  name: "InputItem",
  components: {RemoveButton, MappingEntityList},
  props: {
    id: {
      type: Number
    }
  },
  setup() {
    const mappingEntityStore = useMappingEntityStore()
    const inputStore = useInputStore()
    return {
      mappingEntityStore,
      inputStore
    }
  },
  data() {
    const inputStore = useInputStore()
    const input = inputStore.getById(this.id)
    return {
      macro: input?.macro,
      macro_value: input?.macro_value,
      description: input?.description,
      default_type: input?.default_type,
      default_: input?.default,

      loadingSave: false
    }
  },
  methods: {
    async save() {
      if (!this.macro || !this.macro_value || !this.description || !this.default_type || !this.default_) return
      this.loadingSave = true
      const result = await this.inputStore.save({
        id: this.id,
        macro: this.macro,
        macro_value: this.macro_value,
        description: this.description,
        default_type: this.default_type,
        default: this.default_,
      })
      await RouterService.goToTableItem('input', result.id)
      this.loadingSave = false
    }
  }
})
</script>

<template>
  <VCard density="compact">
    <VCardTitle>
      INPUT
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
          <VTextField density="compact" label="Macro value" v-model="macro_value" variant="outlined"
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
          <VSelect density="compact" label="Default type" v-model="default_type" variant="outlined"
                   hint="Type of default value" persistent-hint
                   :items="['str', 'int', 'bool', 'json']"/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VTextarea density="compact" label="Default value" v-model="default_" variant="outlined"
                     hint="Value for preview paste" persistent-hint/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <VBtn :loading="loadingSave" class="mr-2" color="success" text="Save" @click.prevent="save"/>
          <RemoveButton v-if="id" :remove="() => inputStore.remove(id)" :title="`Input #${id}`"
                        list-name="mapping-entity"/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <MappingEntityList :create="false" table-name="BOUND MAPPING ENTITIES"
                             :mappings-entity="mappingEntityStore.getMappingEntityByEntity('input', id)"/>
        </VCol>
      </VRow>
    </VCardText>
  </VCard>
</template>

<style scoped>

</style>