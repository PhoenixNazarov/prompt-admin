<script lang="ts">
import {defineComponent} from 'vue'
import {Prompt, usePromptStore} from "../../../stores/prompt.store.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {useSettingsStore} from "../../../stores/config/settings.store.ts";
import PromptUnitTestStatus from "./PromptUnitTestStatus.vue";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import TemplateMenuView from "./TemplateMenuView.vue";
import {hashCode} from "../../Utils.ts";


export default defineComponent({
  name: "WorkplaceMenuView",
  components: {TemplateMenuView, PromptUnitTestStatus, FontAwesomeIcon},
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
    isDisable(mapping: Mapping, prompt: Prompt) {
      return this.mappingEntityStore.entity.find(
          el =>
              el.connection_name == mapping.connection_name &&
              el.table == mapping.table &&
              el.field == mapping.field &&
              el.name == prompt.name &&
              el.entity == 'disable'
      )
    },
    toggleFold() {
      this.settingsStore.menu_fold = !this.settingsStore.menu_fold
      this.$emit('toggleFold')
    }
  }
})
</script>

<template>
  <div>
    <div style="display: flex;color: var(--color-5); margin-top: 1rem;justify-content: flex-end; margin-right: 1rem">
      <VBtn variant="text" density="comfortable" style="min-width: 0" @click.prevent="toggleFold">
        <FontAwesomeIcon icon="caret-right" :rotation="!settingsStore.menu_fold ? 180: undefined"/>
      </VBtn>
    </div>
    <VList
        bg-color="var(--color-4)"
        density="compact"
        v-model:opened="opened"
        :style="{
          'display': settingsStore.menu_fold ? 'none' : 'block'
        }"
    >
      <VListGroup :value="connection" v-for="[connection, mappingsTable] in mappingStore.getConnections">
        <template v-slot:activator="{ props }">
          <VListItem
              v-bind="props"
          >
            <FontAwesomeIcon icon="diagram-project"/>
            {{ connection }}
          </VListItem>
        </template>

        <TemplateMenuView :project="connection" @selectPrompt="p => $emit('selectPrompt', p)"/>

        <VListGroup :value="connection + mappingTable" v-for="[mappingTable, mappings] in mappingsTable">
          <template v-slot:activator="{ props }">
            <VListItem
                v-bind="props"
            >
              <FontAwesomeIcon icon="table"/>
              {{ mappingTable }}
            </VListItem>
          </template>
          <VListGroup :value="connection + mapping.field + mapping.id" v-for="mapping in mappings">
            <template v-slot:activator="{ props }">
              <VListItem
                  v-bind="props"
              >
                {{ mapping.field }}
              </VListItem>
            </template>

            <VListGroup :value="connection + mapping.field + mapping.id + 'disable'">
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
                </div>

              </VListItem>
            </VListGroup>

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
              </div>
            </VListItem>

            <VSkeletonLoader
                color="transparent"
                type="list-item"
                v-if="promptStore.loadings.loadAll"
            ></VSkeletonLoader>
          </VListGroup>
        </VListGroup>
      </VListGroup>

      <VSkeletonLoader
          color="transparent"
          type="list-item"
          v-if="mappingStore.loadings.loadAll"
      ></VSkeletonLoader>
    </VList>
  </div>
</template>

<style scoped>

.hide {
  opacity: 0;
}

.v-list-item--density-compact.v-list-item--one-line {
  min-height: unset;
}
</style>