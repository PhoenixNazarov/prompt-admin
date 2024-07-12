<script lang="ts">
import {defineComponent} from 'vue'
import MainLayout from "../../layouts/MainLayout.vue";
import FormatEditor from "./FormatEditor.vue";
import {CalculateOutput, useFormatStore, ValidateOutput} from "../../stores/format.store.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import ConsistentReport from "./ConsistentReport.vue";
import CodeText from "../../components/CodeText.vue";

const startObject =
    `{
  "result": {
    "recommendation": [
      {
          "category_id": 123,
          "importance": 100,
          "relevance": "[based on my answers, explain relevance of this category to me to make we want to focus on it. refer to my answers. up to 50 words]"
      }
    ]
  }
}
`


export default defineComponent({
  name: "FormatView",
  components: {CodeText, ConsistentReport, FontAwesomeIcon, FormatEditor, MainLayout},
  setup() {
    const formatStore = useFormatStore()
    return {
      formatStore
    }
  },
  data() {
    return {
      formatObject: {text: startObject},
      validateObject: {text: startObject},
      mode: 'generate',
      inputFormat: 'json',
      calculateOutput: null as CalculateOutput | null,
      validateOutput: null as ValidateOutput | null,
      loading: {
        calculate: false,
        validate: false
      }
    }
  },
  methods: {
    async calculate() {
      this.loading.calculate = true
      if (this.mode == 'load') {
        this.calculateOutput = await this.formatStore.load(this.formatObject.text)
      } else if (this.mode == 'generate') {
        this.calculateOutput = await this.formatStore.generate(this.formatObject.text, this.inputFormat)
      }
      this.loading.calculate = false
    },
    async validate() {
      this.loading.validate = true
      if (this.calculateOutput?.format_json) {
        this.validateOutput = await this.formatStore.validate(this.calculateOutput?.format_json, this.validateObject.text)
      }
      this.loading.validate = false
    }
  }
})
</script>

<template>
  <MainLayout @setView="$emit('setView')">
    <div class="format outer-y">

      <h1>Format calculator
      </h1>
      <h2>
        <VBtn variant="tonal" density="comfortable" @click.prevent="calculate" :loading="loading.calculate">Calculate
        </VBtn>
      </h2>

      <h1>
        Mode
      </h1>
      <h2>
        <VRadioGroup v-model="mode" inline>
          <VRadio label="Load schema from json" value="load"></VRadio>
          <VRadio label="Generate schema for object" value="generate"></VRadio>
        </VRadioGroup>
      </h2>

      <div v-if="mode == 'load'">
        <h1>
          Schema json
        </h1>
        <FormatEditor :input-object="formatObject" mode="json"/>
      </div>

      <div v-if="mode == 'generate'">
        <h1>
          Input object
        </h1>
        <h2>
          <VRadioGroup v-model="inputFormat" inline>
            <template v-slot:label>
              <div>Input object format:</div>
            </template>
            <VRadio label="Object" value="object"></VRadio>
            <VRadio label="Json" value="json"></VRadio>
            <VRadio label="Xml" value="xml"></VRadio>
          </VRadioGroup>
        </h2>
        <FormatEditor :input-object="formatObject" :mode="inputFormat"/>
      </div>
      <h2 class="program-error" v-if="calculateOutput?.cant_load_schema_error">
        {{ calculateOutput?.cant_load_schema_error }}
      </h2>

      <h2 class="program-error" v-if="calculateOutput?.cant_generate_schema_error">
        {{ calculateOutput?.cant_generate_schema_error }}
      </h2>

      <ConsistentReport :report="calculateOutput?.consistent_report"/>

      <div v-if="calculateOutput != null">
        <CodeText
            title="Output schema in json"
            :code="calculateOutput.format_json"
            :error="calculateOutput.cant_load_schema_error"
        />
        <CodeText
            title="Output schema example in json"
            :code="calculateOutput.example_json"
            :error="calculateOutput.cant_make_example_json_error"
        />
        <CodeText
            title="Output schema example in xml"
            :code="calculateOutput.example_xml"
            :error="calculateOutput.cant_make_example_xml_error"
        />


        <div v-if="calculateOutput.format_json">
          <h1>
            Validation
          </h1>
          <h2>
            <VBtn variant="tonal" density="comfortable" :loading="loading.validate" @click.prevent="validate">Validate
            </VBtn>
          </h2>
          <h1>
            Output string
          </h1>

          <FormatEditor :input-object="validateObject" mode="object"/>

          <CodeText
              v-if="validateOutput"
              title="Validation result in python format"
              :code="validateOutput.validate_value"
              :error="validateOutput.cant_validate_value_error"
          />
        </div>


      </div>
    </div>
  </MainLayout>
</template>

<style scoped>
@import '/src/styles/hint.css';

.format {
  color: var(--color-5);
  height: 100%;
}
</style>