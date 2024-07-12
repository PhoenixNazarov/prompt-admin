<script lang="ts">
import {defineComponent} from 'vue'
import {usePromptStore} from "../../../stores/prompt.store.ts";
import {useMappingStore} from "../../../stores/config/mapping.store.ts";
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {useSettingsStore} from "../../../stores/config/settings.store.ts";

export default defineComponent({
  name: "WorkplaceMenuView",
  components: {FontAwesomeIcon},
  setup() {
    const promptStore = usePromptStore()
    const mappingStore = useMappingStore()
    const settingsStore = useSettingsStore()
    return {
      promptStore,
      mappingStore,
      settingsStore
    }
  },
  data() {
    const settingsStore = useSettingsStore()
    return {
      opened: settingsStore.menuOpenedItems
    }
  },
  watch: {
    opened(newVal) {
      this.settingsStore.menuOpenedItems = newVal
    }
  }
})
</script>

<template>
  <VList
      bg-color="var(--color-4)"
      density="compact"
      v-model:opened="opened"
  >
    <VSkeletonLoader
        color="transparent"
        type="list-item"
        v-if="mappingStore.loadings.getAll"
    ></VSkeletonLoader>
    <VListGroup :value="connection" v-for="[connection, mappingsTable] in mappingStore.getConnections">
      <template v-slot:activator="{ props }">
        <VListItem
            v-bind="props"
        >
          <FontAwesomeIcon icon="diagram-project"/>
          {{ connection }}
        </VListItem>
      </template>
      <VListGroup :value="mappingTable" v-for="[mappingTable, mappings] in mappingsTable">
        <template v-slot:activator="{ props }">
          <VListItem
              v-bind="props"
          >
            <FontAwesomeIcon icon="table"/>
            {{ mappingTable }}
          </VListItem>
        </template>
        <VListGroup :value="mapping.field + mapping.id" v-for="mapping in mappings">
          <template v-slot:activator="{ props }">
            <VListItem
                v-bind="props"
            >
              {{ mapping.field }}
            </VListItem>
          </template>
          <VSkeletonLoader
              color="transparent"
              type="list-item"
              v-if="promptStore.loadings.loadAll"
          ></VSkeletonLoader>
          <VListItem
              v-for="prompt in promptStore.promptsByMapping(mapping.id)"
              @click.prevent="$emit('selectPrompt', prompt)"
          >
            {{ prompt.name }}
          </VListItem>
        </VListGroup>
      </VListGroup>
    </VListGroup>
  </VList>
</template>

<style scoped>

.v-list-item--density-compact.v-list-item--one-line {
  min-height: unset;
}
</style>