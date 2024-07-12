<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt} from "../../../stores/prompt.store.ts";
import {Diff} from "vue-diff";
import {useSettingsStore} from "../../../stores/config/settings.store.ts";

export default defineComponent({
  name: "CompareView",
  components: {Diff},
  setup() {
    const settingsStore = useSettingsStore()
    return {
      settingsStore
    }
  },
  props: {
    prompt: {
      type: Object as PropType<Prompt>,
      required: true
    }
  },
  data() {
    return {
      height: (window.innerHeight - 6 * parseFloat(getComputedStyle(document.documentElement).fontSize))
    }
  }
})
</script>

<template>
  <div>
    <Diff
        :mode="settingsStore.changelog_mode"
        theme="light"
        language="xml"
        :prev="!settingsStore.changelog_different_current ?
        prompt.auditData?.prevAudit?.value :
        prompt.auditData!!.audit!!.value"
        :current="!settingsStore.changelog_different_current ?
        prompt.auditData?.audit.value :
        prompt.value"
        :folding="settingsStore.changelog_folding"
        :virtual-scroll="{ height: height }"
        style="    font-size: 0.5rem;"
    />
  </div>
</template>

<style scoped>
</style>