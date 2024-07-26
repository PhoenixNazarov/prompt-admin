<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {SyncData, useSyncDataStore} from "../../../stores/config/syncData.store.ts";
import JsonEditorVue from "json-editor-vue";
import CodeText from "../../../components/CodeText.vue";

export default defineComponent({
  name: "HintSyncData",
  components: {CodeText, JsonEditorVue},
  setup() {
    const syncDataStore = useSyncDataStore()
    return {
      syncDataStore
    }
  },
  props: {
    syncData: {
      type: Object as PropType<SyncData>,
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
      parsed_model_default_xml: undefined as string | undefined
    }
  },
  methods: {
    initSyncData() {
      this.service_model_info = this.parseJson(this.syncData.service_model_info)
      this.template_context_type = this.parseJson(this.syncData.template_context_type)
      this.template_context_default = this.parseJson(this.syncData.template_context_default)
      this.history_context_default = this.parseJson(this.syncData.history_context_default)
      this.parsed_model_type = this.parseJson(this.syncData.parsed_model_type)
      this.parsed_model_default = this.parseJson(this.syncData.parsed_model_default)
      if (!this.parsed_model_default && this.syncData.parsed_model_default) {
        this.parsed_model_default = this.syncData.parsed_model_default
        this.parsed_model_default_type = 'string'
      }
      this.fail_parse_model_strategy = this.parseJson(this.syncData.fail_parse_model_strategy)
    },
    parseJson(input: string | undefined) {
      if (!input) return
      try {
        return JSON.parse(input)
      } catch (e) {
      }
      return
    }
  },
  mounted() {
    this.initSyncData()
  },
  watch: {
    syncData() {
      this.initSyncData()
    }
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
      <VCardText>
        <JsonEditorVue v-model="template_context_default" mode="tree" :mainMenuBar="false" :navigationBar="false"
                       class="jse-theme-dark"/>
      </VCardText>
    </VCard>
    <VCard class="mt-4" title="Output" variant="tonal" v-if="parsed_model_default">
      <VCardText>
        <VTabs v-if="parsed_model_default_type == 'object'" v-model="parsed_model_default_tab">
          <VTab value="json">JSON</VTab>
          <VTab value="xml" @click.prevent="syncDataStore.loadXmlParsedModelDefault(syncData)">XML</VTab>
        </VTabs>
        <VTabsWindow v-model="parsed_model_default_tab">
          <VTabsWindowItem value="json">
            <JsonEditorVue v-model="parsed_model_default" mode="tree" :mainMenuBar="false" :navigationBar="false"
                           class="jse-theme-dark"/>
          </VTabsWindowItem>
          <VTabsWindowItem value="xml">
            <CodeText :code="syncData.parsed_model_default_xml"/>
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