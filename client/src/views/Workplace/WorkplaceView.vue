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
import PreviewView from "./Editor/Preview/PreviewView.vue";
import UnitTestView from "./Editor/UnitTestView.vue";
import {useUnitTestStore} from "../../stores/config/unitTest.store.ts";
import MainHintView from "./Hint/MainHintView.vue";
import {useSettingsStore} from "../../stores/config/settings.store.ts";

export default defineComponent({
  name: "WorkplaceView",
  components: {
    MainHintView,
    UnitTestView,
    PreviewView,
    FontAwesomeIcon,
    CompareView,
    HintView,
    WorkplaceMenuView,
    EditorView,
    MainLayout,
    Breadcrumb
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
    const settingsStore = useSettingsStore()
    return {
      openPrompts: [] as Prompt[],
      selectedPrompt: null as Prompt | null,

      validate: {
        interval: null as object | null,
        needUpdate: false,
        iteration: false
      },

      widthMenu: settingsStore.menu_fold ? '4rem' : '25rem',
      widthHint: settingsStore.hint_fold ? '4rem' : '25rem',
    }
  },
  methods: {
    selectPrompt(prompt: Prompt) {
      if (prompt.templateData) {
        if (this.openPrompts.findIndex(el => el.templateData?.key == prompt.templateData?.key) == -1) this.openPrompts.push(prompt)
      } else if (prompt.unitTestData) {
        if (this.openPrompts.findIndex(el => el.unitTestData?.unitTest.id == prompt.unitTestData?.unitTest.id) == -1) this.openPrompts.push(prompt)
      } else if (!this.openPrompts.includes(prompt)) this.openPrompts.push(prompt)
      this.selectedPrompt = prompt
      this.hashPrompt()
      this.validate.needUpdate = true
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
      if (!mapping) return [{label: 'prompt-admin'}]
      return [
        {label: 'prompt-admin'},
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
    },
    toggleHint() {
      if (this.widthHint == '25rem') {
        this.widthHint = '4rem'
      } else {
        this.widthHint = '25rem'
      }
    },
    toggleMenu() {
      if (this.widthMenu == '25rem') {
        this.widthMenu = '4rem'
      } else {
        this.widthMenu = '25rem'
      }
    },
    hashPrompt() {
      if (!this.selectedPrompt) return
      const mapping = this.mappingStore.getById(this.selectedPrompt.mapping_id)
      if (!mapping) return;
      this.$router.push({hash: `#/${mapping.connection_name}/${mapping.table}/${mapping.field}/${this.selectedPrompt.name}`})
    },
    hashLoadPrompt() {
      const hash = this.$route.hash
      const items = hash.split('/')
      if (items.length != 5 || items.length <= 0 || items[0] != '#') {
        this.$router.push({hash: ''})
        return
      }
      const connectionName = items[1]
      const table = items[2]
      const field = items[3]
      const name = items[4]
      const mapping = this.mappingStore.getByConnectionTableField(connectionName, table, field)
      if (!mapping || !mapping.id) {
        this.$router.push({hash: ''})
        return
      }
      const prompt = this.promptStore.promptByMappingName(mapping.id, name)
      if (!prompt) {
        this.$router.push({hash: ''})
        return
      }
      this.selectPrompt(prompt)
    }
  },
  mounted() {
    const loadPrompt = async () => {
      await Promise.all([
        this.promptStore.loadAll(),
        this.mappingStore.loadAll()
      ])
      this.hashLoadPrompt()
    }
    loadPrompt()

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
      <WorkplaceMenuView @selectPrompt="selectPrompt" @toggleFold="toggleMenu"/>
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
        <div style="color: var(--color-5); padding: 1rem; height: calc(100vh - 8rem);" v-else>
          Select need prompt...
        </div>
        <div class="breadcrumb-status">
          <Breadcrumb
              v-if="breadcrumbItems().length > 0" :model="breadcrumbItems()"
              class="breadcrumb"
              style="background-color: white; padding: 0.2rem 1rem; height: 2rem"
          />
          <div class="mr-2">
            <FontAwesomeIcon :spin="true" v-if="validate.needUpdate || validate.iteration || !selectedPrompt?.validate"
                             icon="spinner"
                             style="color: var(--color-4)"/>
            <FontAwesomeIcon v-else-if="selectedPrompt?.validate.errors.length <= 0" icon="check" style="color: green"/>
            <FontAwesomeIcon v-else-if="selectedPrompt?.validate.errors.length > 0" icon="xmark"
                             style="color: var(--color-1)"/>
          </div>
        </div>
      </div>
    </div>
    <div class="hint outer-y">
      <MainHintView
          :prompt="selectedPrompt"
          @preview="selectPrompt"
          @closePrompt="closePrompt"
          @toggleFold="toggleHint"
      />
    </div>
  </div>
</template>

<style scoped>
.workplace {
  --menu-width: v-bind(widthMenu);
  --hint-width: v-bind(widthHint);

  display: flex;
  height: 100%;
}

.menu {
  width: var(--menu-width);
  background-color: var(--color-4);
  overflow-x: hidden;
  transition: 200ms;
}

.editor {
  width: calc(100vw - var(--menu-width) - var(--hint-width));
  transition: 200ms;
}

.hint {
  width: var(--hint-width);
  background-color: var(--color-4);
  overflow-x: hidden;
  transition: 200ms;
}

.breadcrumb-status {
  background-color: white;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

</style>