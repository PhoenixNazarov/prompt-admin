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
import Breadcrumb from 'primevue/breadcrumb';
import {useSyncDataStore} from "../../stores/config/syncData.store.ts";
import PreviewView from "./Editor/PreviewView.vue";
import UnitTestView from "./Editor/UnitTestView.vue";
import {useUnitTestStore} from "../../stores/config/unitTest.store.ts";
import MainHintView from "./Hint/MainHintView.vue";

export default defineComponent({
  name: "WorkplaceView",
  components: {
    MainHintView,
    UnitTestView,
    PreviewView,
    FontAwesomeIcon, CompareView, HintView, WorkplaceMenuView, EditorView, MainLayout, Breadcrumb
  },
  setup() {
    const promptStore = usePromptStore()
    const mappingStore = useMappingStore()
    const macroStore = useMacroStore()
    const mappingEntityStore = useMappingEntityStore()
    const outputStore = useOutputStore()
    const inputStore = useInputStore()
    const promptAuditStore = usePromptAuditStore()
    const accountStore = useAccountStore()
    const syncDataStore = useSyncDataStore()
    const unitTestStore = useUnitTestStore()
    return {
      promptStore,
      mappingStore,
      macroStore,
      mappingEntityStore,
      outputStore,
      inputStore,
      promptAuditStore,
      accountStore,
      syncDataStore,
      unitTestStore
    }
  },
  data() {
    return {
      openPrompts: [] as Prompt[],
      selectedPrompt: null as Prompt | null,

      validate: {
        interval: null as object | null,
        needUpdate: false,
        iteration: false
      }
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
      if (prompt.previewData) return `PREVIEW: ${prompt.name}`
      if (prompt.auditData) return `COMPARE: ${prompt.name}`
      if (prompt.unitTestData) return `TEST: ${prompt.name}`
      if (prompt.templateData) return `TEMPLATE: ${prompt.templateData.key}`
      return prompt.name
    },
    breadcrumbItems() {
      const mapping = this.mappingStore.getById(this.selectedPrompt?.mapping_id)
      if (!mapping) return []
      return [
        {label: mapping.connection_name, icon: 'fa fa-diagram-project'},
        {label: mapping.table, icon: 'fa fa-table'},
        {label: mapping.field},
        {label: this.selectedPrompt?.name}
      ]
    },
    async validateIteration() {
      if (!this.validate.needUpdate || this.validate.iteration) return
      this.validate.iteration = true
      this.validate.needUpdate = false
      try {
        if (this.selectedPrompt) await this.promptStore.validate(this.selectedPrompt)
      } catch (e) {

      }
      this.validate.iteration = false
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
    this.syncDataStore.loadAll()
    this.unitTestStore.loadAll()

    this.validate.interval = setInterval(this.validateIteration, 200)
  },
  unmounted() {
    if (this.validate.interval) clearInterval(this.validate.interval as unknown as string)
  },
  watch: {
    'selectedPrompt.value'() {
      this.validate.needUpdate = true
    }
  }
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
      <div>
        <CompareView :prompt='selectedPrompt' v-if="selectedPrompt && selectedPrompt.auditData"/>
        <PreviewView :prompt='selectedPrompt' v-else-if="selectedPrompt && selectedPrompt.previewData"/>
        <UnitTestView :prompt="selectedPrompt" v-else-if="selectedPrompt && selectedPrompt.unitTestData"/>
        <EditorView :prompt='selectedPrompt' v-else-if="selectedPrompt"/>
        <div style="color: var(--color-5); padding: 1rem" v-else>
          Select need prompt...
        </div>
        <Breadcrumb v-if="breadcrumbItems().length > 0" :model="breadcrumbItems()"
                    class="breadcrumb"
                    style="background-color: white; padding: 0.2rem 1rem; height: 2rem"/>
      </div>
    </div>
    <div class="hint outer-y">
      <MainHintView
          :prompt="selectedPrompt"
          @preview="selectPrompt"
          @closePrompt="closePrompt"
      />
    </div>
  </div>
</template>

<style scoped>
.workplace {
  display: flex;
  height: 100%;
}

.menu {
  width: 25rem;
  background-color: var(--color-4);
  overflow-x: hidden;
}

.editor {
  width: calc(100vw - 50rem)
}

.hint {
  width: 25rem;
  background-color: var(--color-4);
  overflow-x: hidden;
}

</style>