<script lang="ts">
import {defineComponent} from 'vue'
import MainLayout from "../../layouts/MainLayout.vue";
import FormatEditor from "./FormatEditor.vue";
import {CalculateOutput, useFormatStore, ValidateOutput} from "../../stores/format.store.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import ConsistentReport from "./ConsistentReport.vue";

const startObject = `
{
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
  components: {ConsistentReport, FontAwesomeIcon, FormatEditor, MainLayout},
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
      validateOutput: null as ValidateOutput | null
    }
  },
  methods: {
    async calculate() {
      if (this.mode == 'load') {
        this.calculateOutput = await this.formatStore.load(this.formatObject.text)
      } else if (this.mode == 'generate') {
        this.calculateOutput = await this.formatStore.generate(this.formatObject.text, this.inputFormat)
      }
    },
    async validate() {
      if (this.calculateOutput?.format_json) {
        this.validateOutput = await this.formatStore.validate(this.calculateOutput?.format_json, this.validateObject.text)
      }
    }
  }
})
</script>

<template>
  <MainLayout @setView="$emit('setView')">
    <div class="format outer-y">

      <h1>Format calculator</h1>
      <h2>
        <button class="pointer" @click.prevent="calculate">Calculate</button>
      </h2>
      <h1>
        Mode
      </h1>
      <h2>
        <input type="radio" v-model="mode" value="load"/> Load schema from json
        <input type="radio" v-model="mode" value="generate"/> Generate schema from object
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
        <h2>Input object format
          <input type="radio" v-model="inputFormat" value="object"/> Object
          <input type="radio" v-model="inputFormat" value="json"/> Json
          <input type="radio" v-model="inputFormat" value="xml"/> Xml
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
        <h1>
          Output schema in json
        </h1>
        <h2 class="program" v-if="calculateOutput.format_json">{{ calculateOutput.format_json }}</h2>
        <h2 class="program-error" v-if="calculateOutput.cant_load_schema_error">
          {{ calculateOutput.cant_load_schema_error }}</h2>

        <h1>
          Output schema example in json
        </h1>
        <h2 class="program" v-if="calculateOutput.example_json">{{ calculateOutput.example_json }}</h2>
        <h2 class="program-error" v-if="calculateOutput.cant_make_example_json_error">
          {{ calculateOutput.cant_make_example_json_error }}</h2>


        <h1>
          Output schema example in xml
        </h1>
        <h2 class="program" v-if="calculateOutput.example_xml">{{ calculateOutput.example_xml }}</h2>
        <h2 class="program-error" v-if="calculateOutput.cant_make_example_xml_error">
          {{ calculateOutput.cant_make_example_xml_error }}</h2>

        <div v-if="calculateOutput.format_json">
          <h1>
            Validation
          </h1>
          <h2>
            <button class="pointer" @click.prevent="validate">Validate</button>
          </h2>
          <h1>
            Output string
          </h1>

          <FormatEditor :input-object="validateObject" mode="object"/>
          <div v-if="validateOutput">
            <h1 v-if="validateOutput.validate_value">Validation result in python format</h1>
            <h2 class="program" v-if="validateOutput.validate_value">{{ validateOutput.validate_value }}</h2>
            <h2 class="program-error" v-if="validateOutput.cant_validate_value_error">
              Cant validate value: {{ validateOutput.cant_validate_value_error }}</h2>
          </div>
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