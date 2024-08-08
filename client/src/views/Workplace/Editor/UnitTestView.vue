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

export default defineComponent({
  name: "UnitTestView",
  components: {CodeText, JsonEditorVue, Codemirror, FontAwesomeIcon},
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
  methods: {
    unitTest() {
      return this.prompt.unitTestData?.unitTest
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

    <VCard title="Preview" class="mt-4" v-if="prompt.unitTestData?.unitTest.test_preview">
      <VCardText>
        <Codemirror
            v-model="prompt.unitTestData!.unitTest.test_preview"
            placeholder="Code goes here..."
            :style="{ height: height }"
            :autofocus="true"
            :indent-with-tab="true"
            :extensions="extensions"
            :tab-size="2"
        />
      </VCardText>
    </VCard>

    <VCard title="Response Model" class="mt-4" v-if="prompt.unitTestData?.unitTest.test_response_model">
      <VCardText>
        <JsonEditorVue
            :modelValue="JSON.parse(prompt.unitTestData!.unitTest.test_response_model)"
            mode="tree"
            :mainMenuBar="false"
            :navigationBar="false"
            :read-only="true"
            class="jse-theme-dark"
        />
      </VCardText>
    </VCard>

    <VCard title="Exception" class="mt-4" v-if="prompt.unitTestData?.unitTest.test_exception">
      <VCardText>
        <CodeText :error="prompt.unitTestData?.unitTest.test_exception"/>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>

</style>