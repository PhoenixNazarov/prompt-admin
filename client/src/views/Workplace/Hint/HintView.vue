<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt, usePromptStore} from "../../../stores/prompt.store.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {Macro} from "../../../stores/config/macro.store.ts";
import {Output} from "../../../stores/config/output.store.ts";
import {usePromptAuditStore} from "../../../stores/config/promptAudit.store.ts";
import {useAccountStore} from "../../../stores/user.store.ts";
import {useSettingsStore} from "../../../stores/config/settings.store.ts";
import CodeText from "../../../components/CodeText.vue";
import ChangesHistory from "./ChangesHistory.vue";
import {dateFormat} from "../../Utils.ts";


export default defineComponent({
  name: "HintView",
  components: {ChangesHistory, CodeText},
  props: {
    prompt: {
      type: Object as PropType<Prompt>
    }
  },
  setup() {
    const mappingStore = useMappingStore()
    const mappingEntityStore = useMappingEntityStore()
    const promptStore = usePromptStore()
    const promptAuditStore = usePromptAuditStore()
    const accountStore = useAccountStore()
    const settingsStore = useSettingsStore()
    return {
      mappingStore,
      mappingEntityStore,
      promptStore,
      promptAuditStore,
      accountStore,
      settingsStore
    }
  },
  data() {
    return {
      loading: {
        save: false,
        preview: false
      },
    }
  },
  methods: {
    dateFormat,
    mapping(): Mapping | undefined {
      if (this.prompt) return this.mappingStore.getById(this.prompt.mapping_id)
    },
    inputs(): Macro[] {
      const mapping = this.mapping()
      if (mapping && this.prompt) return this.mappingEntityStore.getInputsByFilter(mapping, this.prompt).sort((one, two) => one.macro > two.macro ? -1 : 1)
      return []
    },
    output(): Output | undefined {
      const mapping = this.mapping()
      if (mapping && this.prompt) return this.mappingEntityStore.getOutputByFilter(mapping, this.prompt)
      return undefined
    },
    macros(): Macro[] {
      const mapping = this.mapping()
      if (mapping && this.prompt) return this.mappingEntityStore.getMacroByFilter(mapping, this.prompt).sort((one, two) => one.macro > two.macro ? -1 : 1)
      return []
    },
    async save() {
      this.loading.save = true
      if (this.prompt) await this.promptStore.savePrompt(this.prompt)
      if (this.prompt) await this.promptAuditStore.loadForPrompt(this.prompt, 5, 0)
      this.loading.save = false
    },
    async preview() {
      if (!this.prompt) return
      this.loading.preview = true
      try {
        const previewPrompt = await this.promptStore.previewPrompt(this.prompt)
        this.$emit('preview', previewPrompt)
      } catch (e) {
        alert('Cant preview this prompt. Dont use unsupported jinja fields')
      }
      this.loading.preview = false
    }
  },
})
</script>

<template>
  <div class="hint outer-y">
    <div v-if="prompt">

      <div v-if="prompt.preview != true && !prompt.auditData?.audit">
        <VBtn variant="tonal" density="comfortable" @click.prevent="save" :loading="loading.save">Save</VBtn>
        <VBtn variant="tonal" density="comfortable" @click.prevent="preview" :loading="loading.preview"
              style="margin-left: 1rem">Preview
        </VBtn>
      </div>
      <h1 v-if="prompt.preview == true">Preview</h1>
      <h1 v-if="prompt.auditData?.audit">Change history</h1>
      <h2 v-if="prompt.auditData?.audit"><b>Time change: </b>
        {{ dateFormat(new Date(prompt.auditData?.audit.time_create)) }}</h2>
      <h2 v-if="prompt.auditData?.audit"><b>Account: </b> {{ accountStore.getLoginById(prompt.auditData?.audit.account_id) }}</h2>


      <VCard class="mt-4" :title="mapping()?.table + '.' + mapping()?.field" variant="tonal">
        <VCardText>
          <b>connection_name: </b> {{ mapping()?.connection_name }}<br>
          <b>field_name: </b> {{ mapping()?.field_name }}<br>
          <b>prompt_id: </b> {{ prompt.id }}<br>
        </VCardText>
      </VCard>

      <VCard class="mt-4" :title="prompt.name" variant="tonal">
        <VCardText>
          {{ mapping()?.description }}
        </VCardText>
      </VCard>

      <VCard class="mt-4" v-if="inputs().length > 0" title="Inputs" variant="tonal">
        <VCardText>
          <div v-for="mappingVariable in inputs()">
            <b>{{ mappingVariable.macro }}</b>:
            {{ mappingVariable.description }}<br>
          </div>
        </VCardText>
      </VCard>

      <VCard class="mt-4" v-if="macros().length > 0" title="Macros" variant="tonal">
        <VCardText>
          <div v-for="mappingVariable in macros()">
            <b>{{ mappingVariable.macro }}</b>:
            {{ mappingVariable.description }} <br>
          </div>
        </VCardText>
      </VCard>


      <CodeText
          v-if="output()"
          title="Required output format"
          :code="output()?.output"
      />

      <ChangesHistory class="mt-4" :prompt="prompt" @preview="prompt => $emit('preview', prompt)"/>
    </div>

    <h1>Settings</h1>
    <h2>changelog_folding <input type="checkbox" v-model="settingsStore.changelog_folding"/></h2>
    <h2>changelog_different_current <input type="checkbox" v-model="settingsStore.changelog_different_current"/></h2>
    <h2>changelog_different_current
      <input type="radio" v-model="settingsStore.changelog_mode" value="split"/> Split
      <input type="radio" v-model="settingsStore.changelog_mode" value="unified"/> Unfilled
    </h2>

  </div>
</template>

<style scoped>
@import '/src/styles/hint.css';

.hint {
  padding: 1rem;
  color: var(--color-5);
}
</style>