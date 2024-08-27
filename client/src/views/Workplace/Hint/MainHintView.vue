<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt} from "../../../stores/prompt.store.ts";
import HintView from "./HintView.vue";
import TemplateHintView from "./TemplateHintView.vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {useSettingsStore} from "../../../stores/config/settings.store.ts";

export default defineComponent({
  name: "MainHintView",
  components: {FontAwesomeIcon, TemplateHintView, HintView},
  props: {
    prompt: {
      type: Object as PropType<Prompt | null>
    }
  },
  setup() {
    const settingsStore = useSettingsStore()
    return {
      settingsStore
    }
  },
  methods: {
    toggleFold() {
      this.settingsStore.hint_fold = !this.settingsStore.hint_fold
      this.$emit('toggleFold')
    }
  }
})
</script>

<template>
  <div class="hint">
    <VBtn variant="text" class="mb-4" density="comfortable" style="min-width: 0" @click.prevent="toggleFold">
      <FontAwesomeIcon icon="caret-right" :rotation="!settingsStore.hint_fold ? undefined: 180"/>
    </VBtn>
    <div>
      <TemplateHintView :prompt="prompt" v-if="prompt?.templateData" @closePrompt="p => $emit('closePrompt', p)"/>
      <HintView :prompt="prompt" v-else-if="prompt" @preview="p => $emit('preview', p)"/>
    </div>
  </div>
</template>

<style scoped>

.hint {
  padding: 1rem;
  color: var(--color-5);
}
</style>