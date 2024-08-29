<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {xml} from '@codemirror/lang-xml'
import {json} from '@codemirror/lang-json'
import {Codemirror} from 'vue-codemirror'
import {Prompt} from "../../../stores/prompt.store.ts";
import {useMappingStore} from "../../../stores/config/mapping.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {EditorView} from '@codemirror/view'
import {createCompletions} from "./completion.ts";
import {buildJinjaListLinter, buildJinjaSyntaxLinter, buildJinjaVarLinter} from "./linter.ts";
import {useSettingsStore} from "../../../stores/config/settings.store.ts";

export default defineComponent({
  name: "EditorView",
  setup() {
    const mappingStore = useMappingStore()
    const mappingEntityStore = useMappingEntityStore()
    const settingsStore = useSettingsStore()
    return {
      mappingStore,
      mappingEntityStore,
      settingsStore
    }
  },
  computed: {
    extensions() {
      const ext: any[] = [xml(), json()]
      if (this.settingsStore.editor_line_wrapping) {
        ext.push(EditorView.lineWrapping)
      }
      const mapping = this.mappingStore.getById(this.prompt.mapping_id)
      ext.push(buildJinjaVarLinter())
      ext.push(buildJinjaListLinter())
      if (this.prompt.validate?.errors) ext.push(buildJinjaSyntaxLinter(this.prompt.validate?.errors))
      if (mapping) {
        ext.push(createCompletions(mapping, this.prompt))
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
      height: (window.innerHeight - 8 * parseFloat(getComputedStyle(document.documentElement).fontSize)) + 'px'
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
  height: calc(100vh - 8rem);
  margin: 0;
  overflow: auto;
  background-color: white;
  color: black;
}
</style>