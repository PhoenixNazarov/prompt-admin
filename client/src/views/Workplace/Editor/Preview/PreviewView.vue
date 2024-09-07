<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt, usePromptStore} from "../../../../stores/prompt.store.ts";
import {SyncData} from "../../../../stores/config/syncData.store.ts";
import {Mapping, useMappingStore} from "../../../../stores/config/mapping.store.ts";
import {useMappingEntityStore} from "../../../../stores/config/mappingEntity.store.ts";
import JsonEditorVue from "json-editor-vue";
import CodeText from "../../../../components/CodeText.vue";
import {Codemirror} from "vue-codemirror";
import {EditorView} from "@codemirror/view";
import {xml} from "@codemirror/lang-xml";
import {json} from "@codemirror/lang-json";
import {parseJson} from "../../../Utils.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

export default defineComponent({
  name: "PreviewView",
  components: {FontAwesomeIcon, Codemirror, CodeText, JsonEditorVue},
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
    parseJson,
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
    <VContainer fluid>
      <VRow>
        <VCol>
          <VCard title="History">
            <VCardText>
              <div class="message-group" v-for="(obj, ind) in prompt.previewData!.history">
                <VTextarea
                    :label="obj.role"
                    variant="outlined"
                    auto-grow
                    :prepend-icon="obj.role == 'user' ? 'mdi-account' : 'mdi-assistant'"
                    rows="1"
                    v-model="obj.content"
                />
                <div class="message-control">
                  <FontAwesomeIcon icon="circle-plus" class="pointer"
                                   @click.prevent="prompt.previewData!.history!.splice(ind, 0, {role: 'user', content: 'Hello'})"/>
                  <FontAwesomeIcon icon="trash" class="pointer"
                                   @click.prevent="prompt.previewData!.history!.splice(ind, 1)"/>
                  <FontAwesomeIcon icon="repeat" class="pointer"
                                   @click.prevent="obj.role == 'user' ? obj.role = 'asistant' : obj.role = 'user' "/>
                </div>
              </div>

              <VTextarea
                  variant="outlined"
                  :label="parseJson(syncData()?.service_model_info).config.prompt_position"
                  :prepend-icon="syncData()?.service_model_info?.config?.prompt_position == 'user' ? 'mdi-account' : 'mdi-assistant'"
                  auto-grow
                  rows="1"
                  v-model="prompt.previewData!.value"
              />
              <VBtn
                  density="comfortable"
                  @click.prevent="execute"
                  :loading="loading.execute"
                  text="Send"
                  prepend-icon="mdi-send"
                  style="margin-left: auto; margin-right: auto"
              />
            </VCardText>
          </VCard>
        </VCol>
        <VCol>
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
        </VCol>
      </VRow>
    </VContainer>

    <VContainer fluid>
      <VRow>
        <VCol>
          <VCard title="Response">
            <VCardText>
              <div style="white-space: pre-wrap;" v-if="prompt.previewData?.executeData?.response_model.raw_text">
                {{ prompt.previewData?.executeData?.response_model.raw_text }}
              </div>
              <div style="white-space: pre-wrap;" v-else-if="prompt.previewData?.executeStream">
                {{ prompt.previewData?.executeStream }}
              </div>
              <div v-else>
                Empty
              </div>
            </VCardText>
          </VCard>
        </VCol>
        <VCol>
          <VExpansionPanels multiple>
            <VExpansionPanel
                title="Compile messages"
                class="mt-4"
                :disabled="prompt.previewData?.executeData?.messages == undefined">
              <VExpansionPanelText v-if="prompt.previewData?.executeData?.messages">
                <JsonEditorVue
                    :modelValue="prompt.previewData?.executeData?.messages"
                    mode="tree"
                    :mainMenuBar="false"
                    :navigationBar="false"
                    :read-only="true"
                    class="jse-theme-dark"
                />
              </VExpansionPanelText>
            </VExpansionPanel>
            <VExpansionPanel
                title="Response Anthropic Info"
                class="mt-4"
                :disabled="prompt.previewData?.executeData?.response_model.origin_message == undefined">
              <VExpansionPanelText v-if="prompt.previewData?.executeData?.response_model.origin_message">
                <JsonEditorVue
                    :modelValue="prompt.previewData?.executeData?.response_model.origin_message"
                    mode="tree"
                    :mainMenuBar="false"
                    :navigationBar="false"
                    :read-only="true"
                    class="jse-theme-dark"
                />
              </VExpansionPanelText>
            </VExpansionPanel>
            <VExpansionPanel
                title="Parsed output"
                class="mt-4"
                :disabled="prompt.previewData?.executeData?.response_model.raw_text == undefined || prompt.previewData?.executeData && syncData()?.parsed_model_type == undefined"
            >
              <VExpansionPanelText
                  v-if="prompt.previewData?.executeData && syncData()?.parsed_model_type"
              >
                <CodeText
                    :code="prompt.previewData?.executeData?.response_model.parsed_model"
                    :error="prompt.previewData.executeData.parsed_model_error ? 'Parsed output error' : ''"
                />
              </VExpansionPanelText>
            </VExpansionPanel>
            <VExpansionPanel
                title="Required JSON output schema"
                class="mt-4"
                :disabled="syncData()?.parsed_model_type == undefined"
            >
              <VExpansionPanelText>
                <JsonEditorVue
                    :modelValue="parseJson(syncData()?.parsed_model_type)"
                    mode="tree"
                    :mainMenuBar="false"
                    :navigationBar="false"
                    :read-only="true"
                    class="jse-theme-dark"
                />
              </VExpansionPanelText>
            </VExpansionPanel>
          </VExpansionPanels>
        </VCol>
      </VRow>
    </VContainer>
  </div>
</template>

<style scoped>

.message-group {
  display: flex;
}

.message-control {
  transition: 200ms;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.5rem;
  opacity: 0;
}

.message-group:hover > .message-control {
  opacity: 1;
}

</style>