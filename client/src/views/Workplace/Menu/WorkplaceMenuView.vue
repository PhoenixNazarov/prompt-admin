<script lang="ts">
import {defineComponent} from 'vue'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {useSettingsStore} from "../../../stores/config/settings.store.ts";
import PromptUnitTestStatus from "./PromptUnitTestStatus.vue";
import TemplateMenuView from "./TemplateMenuView.vue";
import MenuPromptList from "./MenuPromptList.vue";


export default defineComponent({
  name: "WorkplaceMenuView",
  components: {MenuPromptList, TemplateMenuView, PromptUnitTestStatus, FontAwesomeIcon},
  setup() {
    const settingsStore = useSettingsStore()
    return {
      settingsStore,
    }
  },
  data() {
    const settingsStore = useSettingsStore()
    return {
      opened: settingsStore.menuOpenedItems,
      filter: settingsStore.menu_search,
    }
  },
  watch: {
    opened(newVal) {
      this.settingsStore.menuOpenedItems = newVal
    },
    filter(newVal) {
      this.settingsStore.menu_search = newVal
    }
  },
  methods: {
    toggleFold() {
      this.settingsStore.menu_fold = !this.settingsStore.menu_fold
      this.$emit('toggleFold')
    }
  }
})
</script>

<template>
  <div>
    <div class="menu-header border-bottom-component">
      <VTextField v-if="!settingsStore.menu_fold"
                  v-model="filter"
                  placeholder="Search"
                  prepend-inner-icon="mdi-magnify"
                  density="compact"
                  variant="outlined"
                  style="margin-left: 1rem" hide-details/>
      <VBtn variant="text" density="comfortable" style="min-width: 0" @click.prevent="toggleFold">
        <FontAwesomeIcon icon="caret-right" :rotation="!settingsStore.menu_fold ? 180: undefined"/>
      </VBtn>
    </div>
    <MenuPromptList
        :filter="filter" @selectPrompt="prompt => $emit('selectPrompt', prompt)"

    />
  </div>
</template>

<style scoped>
.menu-header {
  display: flex;
  color: var(--color-5);
  margin-top: 1rem;
  justify-content: flex-end;
  padding-right: 1rem;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}
</style>