<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {SyncData, useSyncDataStore} from "../../../stores/config/syncData.store.ts";
import JsonEditorVue from "json-editor-vue";
import CodeText from "../../../components/CodeText.vue";
import {parseJson} from "../../Utils.ts";
import {useVarsStore} from "../../../stores/vars.store.ts";
import {Prompt, usePromptStore} from "../../../stores/prompt.store.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";

export default defineComponent({
  name: "HintSyncData",
  components: {CodeText, JsonEditorVue},
  setup() {
    const syncDataStore = useSyncDataStore()
    const varsStore = useVarsStore()
    const mappingStore = useMappingStore()
    const promptStore = usePromptStore()
    const mappingEntityStore = useMappingEntityStore()
    return {
      syncDataStore,
      varsStore,
      mappingStore,
      promptStore,
      mappingEntityStore
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
      service_model_info: undefined as object | undefined,
      template_context_type: undefined as object | undefined,
      template_context_default: undefined as object | undefined,
      history_context_default: undefined as object | undefined,
      parsed_model_type: undefined as object | undefined,
      parsed_model_default: undefined as object | string | undefined,
      parsed_model_default_type: 'object',
      parsed_model_default_tab: 'json',
      fail_parse_model_strategy: undefined as object | undefined,
      parsed_model_default_xml: undefined as string | undefined,
      context: undefined as object | undefined,
      loading: {
        preview: false
      }
    }
  },
  methods: {
    syncData(): SyncData | undefined {
      const mapping = this.mapping()
      if (mapping && this.prompt) return this.mappingEntityStore.getSyncDataByFilter(mapping, this.prompt)
      return undefined
    },
    initSyncData() {
      const syncData = this.syncData()
      if (!syncData) return
      this.service_model_info = parseJson(syncData.service_model_info)
      this.template_context_type = parseJson(syncData.template_context_type)
      this.template_context_default = parseJson(syncData.template_context_default)
      this.history_context_default = parseJson(syncData.history_context_default)
      this.parsed_model_type = parseJson(syncData.parsed_model_type)
      this.parsed_model_default = parseJson(syncData.parsed_model_default)
      if (!this.parsed_model_default && syncData.parsed_model_default) {
        this.parsed_model_default = syncData.parsed_model_default
        this.parsed_model_default_type = 'string'
      }
      this.fail_parse_model_strategy = parseJson(syncData.fail_parse_model_strategy)
      this.initVars()
    },
    async initVars() {
      const mapping = this.mapping()
      if (!mapping) return []
      await this.varsStore.load(mapping.connection_name)
      const v = {}
      this.varsStore.getByProject(mapping.connection_name)?.forEach(vr => v[vr.key] = vr.value)
      this.context = {...this.template_context_default, var: v}
    },
    mapping(): Mapping | undefined {
      if (this.prompt) return this.mappingStore.getById(this.prompt.mapping_id)
    },
    async preview() {
      if (!this.prompt) return
      this.loading.preview = true
      try {
        const previewPrompt = await this.promptStore.previewPrompt(this.prompt, this.context, this.mapping()?.connection_name)
        this.$emit('preview', previewPrompt)
      } catch (e) {
        alert('Cant preview this prompt. Dont use unsupported jinja fields')
      }
      this.loading.preview = false
    },
  },
  mounted() {
    this.initSyncData()
    this.initVars()
  },
  watch: {
    prompt() {
      this.initSyncData()
    },
  }
})
</script>

<template>
  <div>
    <VCard class="mt-4" title="Model information" variant="tonal">
      <VCardText>
        <JsonEditorVue v-model="service_model_info" mode="tree" :read-only="true" :mainMenuBar="false"
                       :navigationBar="false" class="jse-theme-dark"/>
      </VCardText>
    </VCard>
    <VCard class="mt-4" title="Context" variant="tonal">
      <VCardTitle>
        <VBtn variant="tonal" density="comfortable" @click.prevent="preview" :loading="loading.preview" text="Preview"/>
      </VCardTitle>
      <VCardText>
        <JsonEditorVue v-model="context" mode="tree" :mainMenuBar="false" :navigationBar="false"
                       class="jse-theme-dark"/>
      </VCardText>
    </VCard>
    <VCard class="mt-4" title="Output" variant="tonal" v-if="parsed_model_default">
      <VCardText>
        <VTabs v-if="parsed_model_default_type == 'object'" v-model="parsed_model_default_tab">
          <VTab value="json">JSON</VTab>
          <VTab value="xml" @click.prevent="syncDataStore.loadXmlParsedModelDefault(syncData())">XML</VTab>
        </VTabs>
        <VTabsWindow v-model="parsed_model_default_tab">
          <VTabsWindowItem value="json">
            <JsonEditorVue v-model="parsed_model_default" mode="tree" :mainMenuBar="false" :navigationBar="false"
                           class="jse-theme-dark"/>
          </VTabsWindowItem>
          <VTabsWindowItem value="xml">
            <CodeText :code="syncData()?.parsed_model_default_xml"/>
          </VTabsWindowItem>
        </VTabsWindow>

        <div v-if="parsed_model_default_type == 'string'">
          {{ parsed_model_default }}
        </div>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>

</style>