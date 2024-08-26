<script lang="ts">
import {defineComponent} from 'vue'
import {useSettingsStore} from "../../stores/config/settings.store.ts";

export default defineComponent({
  name: "SettingsEditView",
  setup() {
    const settingsStore = useSettingsStore()
    return {
      settingsStore
    }
  }
})
</script>

<template>
  <VCard title="Settings" variant="tonal">
    <VCardText>
      <VCheckbox density="compact" hide-details v-model="settingsStore.changelog_folding" label="Changelog folding"/>
      <VCheckbox density="compact" hide-details v-model="settingsStore.changelog_different_current"
                 label="Changelog different current"/>
      <VRadioGroup inline density="compact" hide-details
                   v-model="settingsStore.changelog_mode">
        <VRadio value="split" label="Split"/>
        <VRadio value="unified" label="Unified"/>
      </VRadioGroup>
      <VCheckbox density="compact" hide-details v-model="settingsStore.editor_line_wrapping"
                 label="Line wrapping for editor"/>
    </VCardText>
  </VCard>
</template>

<style scoped>

</style>