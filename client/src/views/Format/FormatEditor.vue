<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Codemirror} from "vue-codemirror";
import {EditorView} from "@codemirror/view";
import {xml} from "@codemirror/lang-xml";
import {json} from "@codemirror/lang-json";

export default defineComponent({
  name: "FormatEditor",
  components: {Codemirror},
  props: {
    inputObject: {
      type: Object as PropType<{ text: string }>,
      required: true
    },
    mode: {
      type: Object as PropType<'json' | 'xml' | 'object'>,
      default: 'json'
    }
  },
  computed: {
    extensions() {
      if (this.mode == 'xml') return [EditorView.lineWrapping, xml()]
      if (this.mode == 'json') return [EditorView.lineWrapping, json()]
    }
  },
  data() {
    return {
      height: (15 * parseFloat(getComputedStyle(document.documentElement).fontSize)) + 'px'
    }
  }
})
</script>

<template>
  <div class="codemirror">
    <Codemirror
        v-model="inputObject.text"
        placeholder="OutputFormat"
        :autofocus="true"
        :style="{ height: height }"
        :indent-with-tab="true"
        :extensions="extensions"
        :tab-size="2"
    />
  </div>
</template>

<style scoped>

</style>