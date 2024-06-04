<script lang="ts">
import {defineComponent} from 'vue'
import {usePromptStore} from "../../../stores/prompt.store.ts";
import MenuGroup from "./MenuGroup.vue";
import {useMappingStore} from "../../../stores/config/mapping.store.ts";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

export default defineComponent({
  name: "WorkplaceMenuView",
  components: {MenuGroup, FontAwesomeIcon},
  setup() {
    const promptStore = usePromptStore()
    const mappingStore = useMappingStore()
    return {
      promptStore,
      mappingStore
    }
  }
})
</script>

<template>
  <div class="menu">
    <MenuGroup icon="diagram-project" :bold="true" :name="connection" v-for="[connection, mappingsTable] in mappingStore.getConnections">
      <MenuGroup icon="table" :name="mappingTable" v-for="[mappingTable, mappings] in mappingsTable"
                 style="margin-left: 1rem">
        <MenuGroup :start-open="false" :name="mapping.field" v-for="mapping in mappings"
                   style="margin-left: 1rem">
          <ol style="margin: 0">
            <li class="pointer" v-for="prompt in promptStore.promptsByMapping(mapping.id)"
                @click.prevent="$emit('selectPrompt', prompt)">
              {{ prompt.name }}
            </li>
          </ol>
        </MenuGroup>
      </MenuGroup>
    </MenuGroup>
  </div>
</template>

<style scoped>
.menu {
  color: var(--color-5);
  padding-top: 1rem;
}
</style>