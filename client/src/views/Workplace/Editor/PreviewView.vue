<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt, usePromptStore} from "../../../stores/prompt.store.ts";
import {SyncData} from "../../../stores/config/syncData.store.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import JsonEditorVue from "json-editor-vue";
import CodeText from "../../../components/CodeText.vue";
import {Codemirror} from "vue-codemirror";
import {EditorView} from "@codemirror/view";
import {xml} from "@codemirror/lang-xml";
import {json} from "@codemirror/lang-json";

export default defineComponent({
  name: "PreviewView",
  components: {Codemirror, CodeText, JsonEditorVue},
  props: {
    prompt: {
      type: Object as PropType<Prompt>,
      required: true
    }
  },
  computed: {
    extensions() {
      return [EditorView.lineWrapping, xml(), json()]
    }
  },
  setup() {
    const promptStore = usePromptStore()
    const mappingStore = useMappingStore()
    const mappingEntityStore = useMappingEntityStore()
    return {
      promptStore,
      mappingStore,
      mappingEntityStore
    }
  },
  data() {
    return {
      height: (window.innerHeight - 15 * parseFloat(getComputedStyle(document.documentElement).fontSize)),
      previewMode: 'diff',
      loading: {
        execute: false
      }
    }
  },
  methods: {
    mapping(): Mapping | undefined {
      if (this.prompt) return this.mappingStore.getById(this.prompt.mapping_id)
    },
    syncData(): SyncData | undefined {
      const mapping = this.mapping()
      if (mapping && this.prompt) return this.mappingEntityStore.getSyncDataByFilter(mapping, this.prompt)
      return undefined
    },
    async execute() {
      const syncData = this.syncData()
      if (!syncData) return
      this.loading.execute = true
      try {
        await this.promptStore.execute(this.prompt, syncData)
      } catch (e) {
        alert('Error execution: ' + e)
      }
      this.loading.execute = false
    }
  }
})
</script>

<template>
  <div style="height: calc(100vh - 8rem); background-color: var(--color-3)" class="outer-y">

    <VCard title="History">
      <VCardText>
        <VTextarea v-for="obj in prompt.previewData!.history" :label="obj.role" variant="outlined" :model-value="obj.content"></VTextarea>
      </VCardText>
    </VCard>

    <VCard title="Preview">
      <VCardText>
        <VTabs v-model="previewMode">
          <VTab value="diff">Different</VTab>
          <VTab value="edit">Edit</VTab>
        </VTabs>
        <VTabsWindow v-model="previewMode">
          <VTabsWindowItem value="diff">
            <Diff
                mode="unified"
                theme="light"
                language="xml"
                :prev="prompt.value"
                :current="prompt.previewData?.value"
                :folding="false"
                :virtual-scroll="{ height: height }"
                style="    font-size: 0.5rem;"
            />
          </VTabsWindowItem>
          <VTabsWindowItem value="edit">
            <Codemirror
                v-model="prompt.previewData!.value"
                placeholder="Code goes here..."
                :style="{ height: height }"
                :autofocus="true"
                :indent-with-tab="true"
                :extensions="extensions"
                :tab-size="2"
            />
          </VTabsWindowItem>
        </VTabsWindow>
      </VCardText>
    </VCard>
    <div style="display: flex;" class="mt-4">
      <VBtn density="comfortable" @click.prevent="execute" :loading="loading.execute" text="Execute"
            style="margin-left: auto; margin-right: auto"/>
    </div>

    <VCard title="Compile messages" class="mt-4" v-if="prompt.previewData?.executeData?.messages">
      <VCardText>
        <JsonEditorVue
            :modelValue="prompt.previewData?.executeData?.messages"
            mode="tree"
            :mainMenuBar="false"
            :navigationBar="false"
            :read-only="true"
            class="jse-theme-dark"
        />
      </VCardText>
    </VCard>

    <VCard title="Response" class="mt-4" v-if="prompt.previewData?.executeData?.response_model.raw_text">
      <VCardText>
        <div style="white-space: pre-wrap;">
          {{ prompt.previewData?.executeData?.response_model.raw_text }}
        </div>
      </VCardText>
    </VCard>

    <VCard title="Parsed output" class="mt-4" v-if="prompt.previewData?.executeData && syncData()?.parsed_model_type">
      <VCardText>
        <div style="white-space: pre-wrap;" v-if="!prompt.previewData.executeData.parsed_model_error">
          {{ prompt.previewData?.executeData?.response_model.parsed_model }}
        </div>

        <CodeText error="Parsed output error" v-else/>
      </VCardText>
    </VCard>

    <VCard title="Response Anthropic Info" class="mt-4"
           v-if="prompt.previewData?.executeData?.response_model.origin_message">
      <VCardText>
        <JsonEditorVue
            :modelValue="prompt.previewData?.executeData?.response_model.origin_message"
            mode="tree"
            :mainMenuBar="false"
            :navigationBar="false"
            :read-only="true"
            class="jse-theme-dark"
        />
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>

</style>