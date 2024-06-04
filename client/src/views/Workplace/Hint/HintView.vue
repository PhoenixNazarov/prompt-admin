<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt, usePromptStore} from "../../../stores/prompt.store.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {Macro} from "../../../stores/config/macro.store.ts";
import {Output} from "../../../stores/config/output.store.ts";
import {PromptAudit, usePromptAuditStore} from "../../../stores/config/promptAudit.store.ts";
import moment from 'moment';
import {useAccountStore} from "../../../stores/user.store.ts";


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
    const promptAuditStore = usePromptAuditStore()
    const accountStore = useAccountStore()
    return {
      mappingStore,
      mappingEntityStore,
      promptStore,
      promptAuditStore,
      accountStore
    }
  },
  methods: {
    mapping(): Mapping | undefined {
      return this.mappingStore.getById(this.prompt.mapping_id)
    },
    inputs(): Macro[] {
      const mapping = this.mapping()
      if (mapping) return this.mappingEntityStore.getInputsByFilter(mapping, this.prompt).sort((one, two) => one.macro > two.macro ? -1 : 1)
      return []
    },
    output(): Output | undefined {
      const mapping = this.mapping()
      if (mapping) return this.mappingEntityStore.getOutputByFilter(mapping, this.prompt)
      return undefined
    },
    macros(): Macro[] {
      const mapping = this.mapping()
      if (mapping) return this.mappingEntityStore.getMacroByFilter(mapping, this.prompt).sort((one, two) => one.macro > two.macro ? -1 : 1)
      return []
    },
    save() {
      this.promptStore.savePrompt(this.prompt)
      this.promptAuditStore.loadForPrompt(this.prompt)
    },
    changes(): PromptAudit[] | undefined {
      return this.promptAuditStore.getByPrompt(this.prompt)
    },
    dateFormat(input: Date): String {
      return moment(input).format('MM/DD/YYYY HH:mm')
    },
    getAccountLogin(id: number | undefined): String {
      if (id != undefined) {
        const account = this.accountStore.getById(id)
        if (account) return account.login
      }
      return 'undefined'
    },
    previewPromptAudit(promptAudit: PromptAudit) {
      const prompt: Prompt = {
        mapping_id: this.prompt.mapping_id,
        table: this.prompt.table,
        field: this.prompt.field,
        id: this.prompt.id,
        value: this.prompt.value,
        name: this.prompt.name,
        audit: promptAudit
      }
      this.$emit('preview', prompt)
    },
    async preview() {
      try {
        const previewPrompt = await this.promptStore.previewPrompt(this.prompt)
        this.$emit('preview', previewPrompt)
      } catch (e) {
        alert('Cant preview this prompt. Dont use unsupported jinja fields')
      }
    }
  },
})
</script>

<template>
  <div class="hint outer-y">
    <h1 v-if="prompt.preview != true && !prompt.audit">
      <button class="pointer" @click.prevent="save">Save</button>
      <button class="pointer" @click.prevent="preview" style="margin-left: 1rem">Preview</button>
    </h1>
    <h1 v-if="prompt.preview == true">Preview</h1>
    <h1 v-if="prompt.audit">Change history</h1>
    <h2 v-if="prompt.audit"><b>Time change: </b> {{ dateFormat(new Date(prompt.audit.time_create)) }}</h2>
    <h2 v-if="prompt.audit"><b>Account: </b> {{ getAccountLogin(prompt.audit.account_id) }}</h2>

    <h1> {{ mapping()?.table }}.{{ mapping()?.field }}</h1>
    <h2><b>connection_name: </b> {{ mapping()?.connection_name }}</h2>
    <h2><b>field_name: </b> {{ mapping()?.field_name }}</h2>
    <h2><b>prompt_id: </b> {{ prompt.id }}</h2>


    <h1> {{ prompt.name }}</h1>
    <h2>{{ mapping()?.description }}</h2>


    <h1 v-if="inputs().length > 0">Inputs</h1>
    <div v-for="mappingVariable in inputs()">
      <h2><b>{{ mappingVariable.macro }}</b>: </h2>
      <h2>{{ mappingVariable.description }}</h2>
    </div>

    <h1 v-if="macros().length > 0">Macros</h1>
    <div v-for="mappingVariable in macros()">
      <h2><b>{{ mappingVariable.macro }}</b>: </h2>
      <h2>{{ mappingVariable.description }}</h2>
    </div>

    <h1 v-if="output()">Required output format</h1>
    <h2 class="program">{{ output()?.output }}</h2>


    <h1>Changes History</h1>
    <h2 v-if="changes() != undefined && changes()?.length == 0">Not changed</h2>
    <h2 v-for="promptAudit in changes()" class="pointer" @click.prevent="previewPromptAudit(promptAudit)">
      {{ dateFormat(new Date(promptAudit.time_create)) }}: {{ getAccountLogin(promptAudit.account_id) }}
    </h2>

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

.program {
  font-family: 'JetBrains Mono', serif;
  color: var(--color-4);
  background-color: var(--color-5);
}

</style>