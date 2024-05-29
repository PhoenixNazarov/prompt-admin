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

export default defineComponent({
  name: "WorkplaceView",
  components: {HintView, WorkplaceMenuView, EditorView, MainLayout},
  setup() {
    const promptStore = usePromptStore()
    const mappingStore = useMappingStore()
    const macroStore = useMacroStore()
    const mappingEntityStore = useMappingEntityStore()
    const outputStore = useOutputStore()
    const inputStore = useInputStore()
    return {
      promptStore,
      mappingStore,
      macroStore,
      mappingEntityStore,
      outputStore,
      inputStore
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
    }
  },
  mounted() {
    this.promptStore.loadAll()
    this.mappingStore.getAll()
    this.macroStore.getAll()
    this.mappingEntityStore.getAll()
    this.outputStore.getAll()
    this.inputStore.getAll()
  },
})
</script>

<template>
  <MainLayout>
    <div class="workplace">
      <div class="menu outer-y">
        <WorkplaceMenuView @selectPrompt="selectPrompt"/>
      </div>
      <div class="editor">
        <EditorView :prompt='prompt' v-if="prompt"/>
        <div style="color: var(--color-5); padding: 1rem" v-else>
          Select need prompt...
        </div>
      </div>
      <div class="hint outer-y">
        <HintView :prompt="prompt" v-if="prompt" @preview="selectPrompt"/>
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