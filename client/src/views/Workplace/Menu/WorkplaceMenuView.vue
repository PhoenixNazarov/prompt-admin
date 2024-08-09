<script lang="ts">
import {defineComponent} from 'vue'
import {Prompt, usePromptStore} from "../../../stores/prompt.store.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {useSettingsStore} from "../../../stores/config/settings.store.ts";
import PromptUnitTestStatus from "./PromptUnitTestStatus.vue";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";

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
  components: {PromptUnitTestStatus, FontAwesomeIcon},
  setup() {
    const promptStore = usePromptStore()
    const mappingStore = useMappingStore()
    const settingsStore = useSettingsStore()
    const mappingEntityStore = useMappingEntityStore()
    return {
      promptStore,
      mappingStore,
      settingsStore,
      mappingEntityStore
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
    },
    doDisable(connectionName: string, table: string, field: string, name: string) {
      this.mappingEntityStore.save({
        connection_name: connectionName,
        table: table,
        field: field,
        name: name,
        entity: 'disable',
        entity_id: 1
      })
    },
    doUnDisable(mapping: Mapping, prompt: Prompt) {
      const mappingEntity = this.isDisable(mapping, prompt)
      if (mappingEntity) this.mappingEntityStore.remove(mappingEntity.id)
    },
    isDisable(mapping: Mapping, prompt: Prompt) {
      return this.mappingEntityStore.entity.find(
          el =>
              el.connection_name == mapping.connection_name &&
              el.table == mapping.table &&
              el.field == mapping.field &&
              el.name == prompt.name &&
              el.entity == 'disable'
      )
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

          <VListGroup :value="mapping.field + mapping.id + 'disable'">
            <template v-slot:activator="{ props }">
              <VListItem
                  v-bind="props"
              >
                <FontAwesomeIcon icon="eye-slash"/>
                Disabled
              </VListItem>
            </template>
            <VListItem
                v-if="mapping.id"
                v-for="prompt in sortPrompts(mapping, promptStore.promptsByMapping(mapping.id)).filter(p => isDisable(mapping, p))"
                @click.prevent="$emit('selectPrompt', prompt)"
            >
              <div style="display: flex;justify-content: space-between;align-items: center;">
                <div>
                  {{ prompt.name }}
                </div>
                <FontAwesomeIcon
                    icon="eye"
                    style="opacity: 0.5"
                    v-if="prompt.name"
                    @click.prevent="doUnDisable(mapping, prompt)"
                />
              </div>

            </VListItem>
          </VListGroup>

          <VSkeletonLoader
              color="transparent"
              type="list-item"
              v-if="promptStore.loadings.loadAll"
          ></VSkeletonLoader>

          <VListItem
              v-if="mapping.id"
              v-for="prompt in sortPrompts(mapping, promptStore.promptsByMapping(mapping.id)).filter(p => !isDisable(mapping, p))"
              @click.prevent="$emit('selectPrompt', prompt)"
          >
            <div style="display: flex;justify-content: space-between;align-items: center;">
              <div>
                <PromptUnitTestStatus :prompt="prompt" @selectPrompt="p => $emit('selectPrompt', p)"/>
                {{ prompt.name }}
              </div>
              <FontAwesomeIcon
                  icon="eye-slash"
                  style="opacity: 0.5"
                  v-if="prompt.name"
                  @click.prevent="doDisable(mapping.connection_name, mapping.table, mapping.field, prompt.name)"
              />
            </div>

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