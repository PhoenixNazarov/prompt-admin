<script lang="ts">
import {defineComponent} from 'vue'
import {Prompt, usePromptStore} from "../../../stores/prompt.store.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {useSettingsStore} from "../../../stores/config/settings.store.ts";

export function hashCode(str: string | number | undefined): number {
  const newStr = String(str)
  let h: number = 0;
  for (let i = 0; i < newStr.length; i++) {
    h = 31 * h + newStr.charCodeAt(i);
  }
  return h & 0xFFFFFFFF
}

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
  },
  methods: {
    sortPrompts(mapping: Mapping, prompts: Prompt[]) {
      if (!mapping.field_order) {
        return prompts.sort((a, b) => {
          return hashCode(a.name) - hashCode(b.name)
        })
      }
      return prompts.sort((a, b) => {
        if (mapping.desc) {
          return hashCode(b.sort_value) - hashCode(a.sort_value)
        } else {
          return hashCode(a.sort_value) - hashCode(b.sort_value)
        }
      })
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
        v-if="mappingStore.loadings.loadAll"
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
              v-for="prompt in sortPrompts(mapping, promptStore.promptsByMapping(mapping.id))"
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