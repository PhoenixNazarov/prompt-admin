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

export default defineComponent({
  name: "WorkplaceView",
  components: {CompareView, HintView, WorkplaceMenuView, EditorView, MainLayout},
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
      prompt: null as Prompt | null,
    }
  },
  methods: {
    selectPrompt(prompt: Prompt) {
      this.prompt = prompt
      this.promptAuditStore.loadForPrompt(this.prompt)
    }
  },
  mounted() {
    this.promptStore.loadAll()
    this.mappingStore.getAll()
    this.macroStore.getAll()
    this.mappingEntityStore.getAll()
    this.outputStore.getAll()
    this.inputStore.getAll()
    this.accountStore.getAll()
  },
})
</script>

<template>
  <MainLayout @setView="$emit">
    <div class="workplace">
      <div class="menu outer-y">
        <WorkplaceMenuView @selectPrompt="selectPrompt"/>
      </div>
      <div class="editor">
        <CompareView :prompt='prompt' v-if="prompt && prompt.auditData"/>
        <EditorView :prompt='prompt' v-else-if="prompt && !prompt.auditData"/>
        <div style="color: var(--color-5); padding: 1rem" v-else>
          Select need prompt...
        </div>
      </div>
      <div class="hint outer-y">
        <HintView :prompt="prompt" @preview="selectPrompt"/>
      </div>
    </div>
  </MainLayout>
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