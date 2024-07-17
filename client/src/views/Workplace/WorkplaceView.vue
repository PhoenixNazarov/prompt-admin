<script lang="ts">
import {defineComponent} from 'vue'
import MainLayout from "../../layouts/MainLayout.vue";
import EditorView from "./Editor/EditorView.vue";
import {Prompt, usePromptStore} from "../../stores/prompt.store.ts";
import WorkplaceMenuView from "./Menu/WorkplaceMenuView.vue";
import {useMappingStore} from "../../stores/config/mapping.store.ts";
import HintView from "./Hint/HintView.vue";
import {useMacroStore} from "../../stores/config/macro.store.ts";
import {useMappingEntityStore} from "../../stores/config/mappingEntity.store.ts";
import {useOutputStore} from "../../stores/config/output.store.ts";
import {useInputStore} from "../../stores/config/input.store.ts";
import {usePromptAuditStore} from "../../stores/config/promptAudit.store.ts";
import {useAccountStore} from "../../stores/user.store.ts";
import CompareView from "./Editor/CompareView.vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

export default defineComponent({
  name: "WorkplaceView",
  components: {FontAwesomeIcon, CompareView, HintView, WorkplaceMenuView, EditorView, MainLayout},
  setup() {
    const promptStore = usePromptStore()
    const mappingStore = useMappingStore()
    const macroStore = useMacroStore()
    const mappingEntityStore = useMappingEntityStore()
    const outputStore = useOutputStore()
    const inputStore = useInputStore()
    const promptAuditStore = usePromptAuditStore()
    const accountStore = useAccountStore()
    return {
      promptStore,
      mappingStore,
      macroStore,
      mappingEntityStore,
      outputStore,
      inputStore,
      promptAuditStore,
      accountStore
    }
  },
  data() {
    return {
      openPrompts: [] as Prompt[],
      selectedPrompt: null as Prompt | null,
    }
  },
  methods: {
    selectPrompt(prompt: Prompt) {
      if (!this.openPrompts.includes(prompt)) this.openPrompts.push(prompt)
      this.selectedPrompt = prompt
    },
    closePrompt(prompt: Prompt) {
      const index = this.openPrompts.indexOf(prompt)
      if (index > -1) {
        this.openPrompts.splice(index, 1)
      }
      if (this.selectedPrompt == prompt) {
        setTimeout(() => this.selectedPrompt = this.openPrompts[index - 1], 10)
      } else {
        const needSelect = this.selectedPrompt
        setTimeout(() => this.selectedPrompt = needSelect, 10)
      }
    },
    name(prompt: Prompt) {
      if (prompt.preview) return `PREVIEW: ${prompt.name}`
      if (prompt.auditData) return `COMPARE: ${prompt.name}`
      return prompt.name
    }
  },
  mounted() {
    this.promptStore.loadAll()
    this.mappingStore.loadAll()
    this.macroStore.loadAll()
    this.mappingEntityStore.loadAll()
    this.outputStore.loadAll()
    this.inputStore.loadAll()
    this.accountStore.loadAll()
  },
})
</script>

<template>
  <div class="workplace">
    <div class="menu outer-y">
      <WorkplaceMenuView @selectPrompt="selectPrompt"/>
    </div>
    <div class="editor">

      <VTabs
          bg-color="var(--color-5)"
          slider-color="var(--color-4)"
          v-model="selectedPrompt"
          show-arrows
      >
        <VTab
            v-for="i in openPrompts"
            :key="i.id"
            :value="i"
        >
          {{ name(i) }}
          <FontAwesomeIcon icon="fa-xmark" style="margin-left: 1rem" @click.prevent="closePrompt(i)"/>
        </VTab>
      </VTabs>
      <CompareView :prompt='selectedPrompt' v-if="selectedPrompt && selectedPrompt.auditData"/>
      <EditorView :prompt='selectedPrompt' v-else-if="selectedPrompt && !selectedPrompt.auditData"/>
      <div style="color: var(--color-5); padding: 1rem" v-else>
        Select need prompt...
      </div>
    </div>
    <div class="hint outer-y">
      <HintView v-if="selectedPrompt" :prompt="selectedPrompt" @preview="selectPrompt"/>
    </div>
  </div>
</template>

<style scoped>
.workplace {
  display: flex;
  height: 100%;
}

.menu {
  width: 20rem;
  background-color: var(--color-4);
  overflow-x: hidden;
}

.editor {
  width: calc(100vw - 45rem)
}

.hint {
  width: 25rem;
  background-color: var(--color-4);
  overflow-x: hidden;
}

</style>