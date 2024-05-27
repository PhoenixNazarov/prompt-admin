<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt, usePromptStore} from "../../../stores/prompt.store.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {Macro} from "../../../stores/config/macro.store.ts";

export default defineComponent({
  name: "HintView",
  props: {
    prompt: {
      type: Object as PropType<Prompt>,
      required: true
    }
  },
  setup() {
    const mappingStore = useMappingStore()
    const mappingEntityStore = useMappingEntityStore()
    const promptStore = usePromptStore()
    return {
      mappingStore,
      mappingEntityStore,
      promptStore
    }
  },
  methods: {
    mapping(): Mapping | undefined {
      return this.mappingStore.getById(this.prompt.mapping_id)
    },
    inputs(): Macro[] {
      const mapping = this.mapping()
      if (mapping) return this.mappingEntityStore.getInputsByFilter(mapping, this.prompt)
      return []
    },
    save() {
      this.promptStore.savePrompt(this.prompt)
    }
  }
})
</script>

<template>
  <div class="hint outer-y">
    <h1>
      <button @click.prevent="save">Save</button>
    </h1>
    <h1> {{ mapping()?.table }}.{{ mapping()?.field }}</h1>
    <h2><b>connection_name: </b> {{ mapping()?.connection_name }}</h2>
    <h2><b>field_name: </b> {{ mapping()?.field_name }}</h2>


    <h1> {{ prompt.name }}</h1>
    <h2>{{ mapping()?.description }}</h2>


    <h1>Inputs</h1>
    <div v-for="mappingVariable in inputs()">
      <h2><b>{{ mappingVariable.macro }}</b>: </h2>
      <h2>{{ mappingVariable.description }}</h2>
    </div>

    <h1>Output</h1>
    <h2>{{ mapping()?.output }}</h2>

  </div>
</template>

<style scoped>
.hint {
  color: var(--color-5);
}

h1 {
  margin-top: 1rem;
  margin-bottom: 0;
  font-size: 1.2rem;
  text-transform: uppercase;
  margin-left: 1rem;
  width: calc(100% - 1rem);
}

h2 {
  font-size: 1rem;
  font-weight: 400;
  margin: 0 0 0 2rem;
  white-space: break-spaces;
  width: calc(100% - 2rem);
}


table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}


</style>