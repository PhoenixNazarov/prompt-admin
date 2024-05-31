<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {xml} from '@codemirror/lang-xml'
import {json} from '@codemirror/lang-json'
import {autocompletion, CompletionContext} from "@codemirror/autocomplete"
import {Codemirror} from 'vue-codemirror'
import {Prompt} from "../../../stores/prompt.store.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import { EditorView } from '@codemirror/view'

function createCompetions(mapping: Mapping, prompt: Prompt) {
  const mappingEntityStore = useMappingEntityStore()
  const options = []
  mappingEntityStore.getInputsByFilter(mapping, prompt).forEach(v => {
    options.push({label: v.macro, type: "text", apply: v.macro_value, detail: v.description})
  })

  mappingEntityStore.getMacroByFilter(mapping, prompt).forEach(v => {
    options.push({label: v.macro, type: "text", apply: v.macro_value, detail: v.description})
  })

  function myCompletions(context: CompletionContext) {
    let word = context.matchBefore(/\w*/)
    if (!word) return
    if (word.from == word.to && !context.explicit)
      return null


    return {
      from: word.from,
      options: options
    }
  }

  return myCompletions
}

export default defineComponent({
  name: "EditorView",
  setup() {
    const mappingStore = useMappingStore()
    const mappingEntityStore = useMappingEntityStore()
    return {
      mappingStore,
      mappingEntityStore
    }
  },
  computed: {
    extensions() {
      const ext = [EditorView.lineWrapping, xml(), json()]
      const mapping = this.mappingStore.getByTableField(this.prompt.table, this.prompt.field)
      if (mapping) {
        ext.push(autocompletion({override: [createCompetions(mapping, this.prompt)]}))
      }
      return ext
    }
  },
  props: {
    prompt: {
      type: Object as PropType<Prompt>,
      required: true
    }
  },
  components: {Codemirror},
  data() {
    return {
      height: (window.innerHeight - 3 * parseFloat(getComputedStyle(document.documentElement).fontSize)) + 'px'
    }
  }
})
</script>

<template>
  <div class="codemirror">
    <Codemirror
        v-model="prompt.value"
        placeholder="Code goes here..."
        :style="{ height: height }"
        :autofocus="true"
        :indent-with-tab="true"
        :extensions="extensions"
        :tab-size="2"
    />
  </div>
</template>

<style scoped>

.codemirror {
  width: 100%;
  height: calc(100vh - 3rem);
  margin: 0;
  overflow: auto;
  background-color: white;
  color: black;
}
</style>