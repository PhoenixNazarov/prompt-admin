<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt} from "../../../stores/prompt.store.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {Codemirror} from "vue-codemirror";
import {EditorView} from "@codemirror/view";
import {xml} from "@codemirror/lang-xml";
import {json} from "@codemirror/lang-json";
import JsonEditorVue from "json-editor-vue";
import CodeText from "../../../components/CodeText.vue";
import {SyncData, useSyncDataStore} from "../../../stores/config/syncData.store.ts";
import {parseJson} from "../../Utils.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";

export default defineComponent({
  name: "UnitTestView",
  components: {CodeText, JsonEditorVue, Codemirror, FontAwesomeIcon},
  props: {
    prompt: {
      type: Object as PropType<Prompt>,
      required: true
    }
  },
  setup() {
    const syncDataStore = useSyncDataStore()
    const mappingStore = useMappingStore()
    const mappingEntityStore = useMappingEntityStore()
    return {
      syncDataStore,
      mappingStore,
      mappingEntityStore
    }
  },
  computed: {
    extensions() {
      return [EditorView.lineWrapping, xml(), json()]
    }
  },
  methods: {
    parseJson,
    unitTest() {
      return this.prompt.unitTestData?.unitTest
    },
    mapping(): Mapping | undefined {
      if (this.prompt) return this.mappingStore.getById(this.prompt.mapping_id)
    },
    syncData(): SyncData | undefined {
      const mapping = this.mapping()
      if (mapping && this.prompt) return this.mappingEntityStore.getSyncDataByFilter(mapping, this.prompt)
      return undefined
    }
  },
  data() {
    return {
      height: (window.innerHeight - 15 * parseFloat(getComputedStyle(document.documentElement).fontSize))
    }
  }
})
</script>

<template>
  <div style="height: calc(100vh - 8rem); background-color: var(--color-3)" class="outer-y">
    <VContainer fluid>
      <VRow>
        <VCol>
          <VCard title="Status">
            <VCardText>
              <div>
                <FontAwesomeIcon v-if="unitTest()?.test_status == 'preview' && unitTest()?.test_exception"
                                 :icon="['fas', 'circle']" style="color: var(--color-1)"/>
                <FontAwesomeIcon v-else-if="unitTest()?.test_status == 'execution'" :icon="['fas', 'circle']"
                                 style="color: green"/>
                <FontAwesomeIcon v-else :spin="true" icon="spinner"/>
                Preview
              </div>
              <div>
                <FontAwesomeIcon v-if="unitTest()?.test_status == 'execution' && unitTest()?.test_exception"
                                 :icon="['fas', 'circle']" style="color: var(--color-1)"/>
                <FontAwesomeIcon v-else-if="unitTest()?.test_status == 'execution'" :icon="['fas', 'circle']"
                                 style="color: green"/>
                <FontAwesomeIcon v-else :spin="true" icon="spinner"/>
                Execution
              </div>
            </VCardText>
          </VCard>

          <VExpansionPanels multiple>
            <VExpansionPanel
                title="Preview"
                class="mt-4"
                :disabled="prompt.unitTestData?.unitTest.test_preview == undefined"
            >
              <VExpansionPanelText v-if="prompt.unitTestData?.unitTest.test_preview">
                <Codemirror
                    v-model="prompt.unitTestData!.unitTest.test_preview"
                    placeholder="Code goes here..."
                    :style="{ height: height }"
                    :autofocus="true"
                    :indent-with-tab="true"
                    :extensions="extensions"
                    :tab-size="2"
                />
              </VExpansionPanelText>
            </VExpansionPanel>
            <VExpansionPanel
                title="Response Model"
                class="mt-4"
                :disabled="prompt.unitTestData?.unitTest.test_response_model == undefined"
            >
              <VExpansionPanelText v-if="prompt.unitTestData!.unitTest.test_response_model">
                <JsonEditorVue
                    :modelValue="parseJson(prompt.unitTestData!.unitTest.test_response_model)"
                    mode="tree"
                    :mainMenuBar="false"
                    :navigationBar="false"
                    :read-only="true"
                    class="jse-theme-dark"
                />
              </VExpansionPanelText>
            </VExpansionPanel>

            <VExpansionPanel
                title="Exception"
                class="mt-4"
                :disabled="prompt.unitTestData?.unitTest.test_exception == undefined"
            >
              <VExpansionPanelText v-if="prompt.unitTestData?.unitTest.test_exception">
                <CodeText :error="prompt.unitTestData?.unitTest.test_exception"/>
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

</style>