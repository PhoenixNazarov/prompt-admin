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
import {dateTimeFormat} from "../../Utils.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {RouterService} from "../../../plugins/router.ts";
import SettingsEditView from "../../Account/SettingsEditView.vue";
import InputList from "../../Tables/Edit/InputList.vue";
import MacroList from "../../Tables/Edit/MacroList.vue";
import OutputList from "../../Tables/Edit/OutputList.vue";
import {SyncData, useSyncDataStore} from "../../../stores/config/syncData.store.ts";
import JsonEditorVue from 'json-editor-vue'
import 'vanilla-jsoneditor/themes/jse-theme-dark.css'
import HintSyncData from "./HintSyncData.vue";

export default defineComponent({
  name: "HintView",
  computed: {
    RouterService() {
      return RouterService
    }
  },
  components: {
    HintSyncData,
    OutputList,
    MacroList,
    InputList,
    SettingsEditView,
    FontAwesomeIcon,
    ChangesHistory,
    CodeText,
    JsonEditorVue
  },
  props: {
    prompt: {
      type: Object as PropType<Prompt>,
    }
  },
  setup() {
    const mappingStore = useMappingStore()
    const mappingEntityStore = useMappingEntityStore()
    const promptStore = usePromptStore()
    const promptAuditStore = usePromptAuditStore()
    const accountStore = useAccountStore()
    const settingsStore = useSettingsStore()
    const syncDataStore = useSyncDataStore()
    return {
      mappingStore,
      mappingEntityStore,
      promptStore,
      promptAuditStore,
      accountStore,
      settingsStore,
      syncDataStore,
    }
  },
  data() {
    return {
      loading: {
        save: false,
        preview: false,
        disable: false
      },
      context: undefined as object | undefined,
      history_context_default: undefined as object | undefined,
    }
  },
  methods: {
    dateTimeFormat,
    dateFormat: dateTimeFormat,
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
    syncData(): SyncData | undefined {
      const mapping = this.mapping()
      if (mapping && this.prompt) return this.mappingEntityStore.getSyncDataByFilter(mapping, this.prompt)
      return undefined
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
      const syncData = this.syncData()
      if (syncData) {
        try {
          const previewPrompt = await this.promptStore.previewPrompt(this.prompt, this.context, this.mapping()?.connection_name)
          previewPrompt.previewData!.history = this.history_context_default
          this.$emit('preview', previewPrompt)
        } catch (e) {
          alert('Cant preview this prompt. Dont use unsupported jinja fields')
        }
      } else {
        try {
          const previewPrompt = await this.promptStore.previewPrompt(this.prompt)
          this.$emit('preview', previewPrompt)
        } catch (e) {
          alert('Cant preview this prompt. Dont use unsupported jinja fields')
        }
      }
      this.loading.preview = false
    },
    async createMappingEntity(entity: string, entity_id: number) {
      await RouterService.goToTableItem('mapping-entity', -1, {
        connection_name: this.mapping()?.connection_name,
        table: this.prompt?.table,
        field: this.prompt?.field,
        name: this.prompt?.name,
        entity: entity,
        entity_id: entity_id
      })
    },
    async doDisable() {
      const mapping = this.mapping()
      if (!mapping) return
      this.loading.disable = true
      await this.mappingEntityStore.save({
        connection_name: mapping.connection_name,
        table: mapping.table,
        field: mapping.field,
        name: this.prompt?.name,
        entity: 'disable',
        entity_id: 1
      })
      this.loading.disable = false
    },
    async doUnDisable() {
      const mappingEntity = this.isDisable()
      this.loading.disable = true
      if (mappingEntity) await this.mappingEntityStore.remove(mappingEntity.id)
      this.loading.disable = false
    },
    isDisable() {
      const mapping = this.mapping()
      if (!mapping) return
      const name = this.prompt?.name
      if (name)
        return this.mappingEntityStore.entity.find(
            el =>
                el.connection_name == mapping.connection_name &&
                el.table == mapping.table &&
                el.field == mapping.field &&
                el.name == name &&
                el.entity == 'disable'
        )
    }
  },
})
</script>

<template>
  <div v-if="settingsStore.hint_fold">
    <div v-if="prompt && !prompt.previewData && !prompt.auditData?.audit">
      <VTooltip text="Save">
        <template v-slot:activator="{ props }">
          <VBtn
              variant="tonal"
              class="mb-4"
              density="comfortable"
              style="min-width: 0"
              :disabled="prompt.originValue == prompt.value"
              @click.prevent="save"
              v-bind="props"
              :loading="loading.save"
          >
            <FontAwesomeIcon icon="floppy-disk"/>
          </VBtn>
        </template>
      </VTooltip>
      <VTooltip text="Preview">
        <template v-slot:activator="{ props }">
          <VBtn
              v-bind="props"
              variant="tonal"
              class="mb-4"
              density="comfortable"
              style="min-width: 0"
              @click.prevent="preview"
              :loading="loading.preview"
              :disabled="syncDataStore.loadings.loadAll != undefined"
          >
            <FontAwesomeIcon icon="magnifying-glass"/>
          </VBtn>
        </template>
      </VTooltip>

      <VTooltip text="Enable" v-if="isDisable() != undefined">
        <template v-slot:activator="{ props }">
          <VBtn
              v-bind="props"
              variant="tonal"
              class="mb-4"
              density="comfortable"
              style="min-width: 0"
              @click.prevent="doUnDisable"
              :loading="loading.disable"
          >
            <FontAwesomeIcon icon="eye"/>
          </VBtn>
        </template>
      </VTooltip>

      <VTooltip text="Disable" v-if="isDisable() == undefined">
        <template v-slot:activator="{ props }">
          <VBtn
              v-bind="props"
              variant="tonal"
              class="mb-4"
              density="comfortable"
              style="min-width: 0"
              @click.prevent="doDisable"
              :loading="loading.disable"
          >
            <FontAwesomeIcon icon="eye-slash"/>
          </VBtn>
        </template>
      </VTooltip>

    </div>
  </div>
  <div :style="{'display': settingsStore.hint_fold ? 'none': 'block'}">
    <div v-if="prompt">
      <div v-if="!prompt.previewData && !prompt.auditData?.audit">
        <VBtn variant="tonal" density="comfortable" @click.prevent="save" :loading="loading.save"
              :disabled="prompt.originValue == prompt.value">Save
        </VBtn>
        <VBtn variant="tonal" density="comfortable" @click.prevent="preview"
              :loading="loading.preview"
              style="margin-left: 1rem">Preview
        </VBtn>
        <VBtn v-if="isDisable() == undefined"
              variant="tonal" density="comfortable" @click.prevent="doDisable()" :loading="loading.disable"
              style="margin-left: 1rem">Disable
        </VBtn>
        <VBtn v-if="isDisable() != undefined"
              variant="tonal" density="comfortable" @click.prevent="doUnDisable()" :loading="loading.disable"
              style="margin-left: 1rem">Enable
        </VBtn>
      </div>
      <h1 v-if="prompt.preview == true">Preview</h1>
      <h1 v-if="prompt.auditData?.audit">Change history</h1>
      <h2 v-if="prompt.auditData?.audit"><b>Time change: </b>
        {{ dateTimeFormat(prompt.auditData?.audit.time_create) }}</h2>
      <h2 v-if="prompt.auditData?.audit"><b>Account: </b>
        {{ accountStore.getLoginById(prompt.auditData?.audit.account_id) }}</h2>


      <VCard class="mt-4" variant="tonal">
        <VCardTitle>
          {{ mapping()?.table + '.' + mapping()?.field }}
          <FontAwesomeIcon icon="circle-info" class="pointer"
                           @click.prevent="RouterService.goToTableItem('mapping', mapping()?.id)"/>
        </VCardTitle>
        <VCardText>
          <b>connection_name: </b> {{ mapping()?.connection_name }}<br>
          <b>field_name: </b> {{ mapping()?.field_name }}<br>
          <b>prompt_id: </b> {{ prompt.id }}<br>
        </VCardText>
      </VCard>

      <VCard class="mt-4" :title="prompt.name" variant="tonal">
        <VCardText>
          {{ mapping()?.description }}
          <div v-if="syncData()?.time_create">
            <b>Last time synchronization: </b> {{ dateTimeFormat(syncData()?.time_create) }}
          </div>
        </VCardText>
      </VCard>

      <HintSyncData
          v-if="syncData() && prompt"
          :prompt="prompt"
          @update_context="c => context = c"
          @update_history_context_default="c => history_context_default = c"
      />
      <div v-else>
        <VCard class="mt-4" variant="tonal">
          <VCardTitle>
            Inputs
            <VDialog>
              <template v-slot:activator="{ props: activatorProps }">
                <FontAwesomeIcon icon="circle-plus" class="pointer" v-bind="activatorProps"/>
              </template>
              <template v-slot:default="{ isActive }">
                <VCard>
                  <InputList :create="false" @clickRow="e => createMappingEntity('input', e.id)"/>
                </VCard>
              </template>
            </VDialog>
          </VCardTitle>
          <VCardText>
            <div v-for="mappingVariable in inputs()">
              <FontAwesomeIcon icon="circle-info" class="pointer circle-info"
                               @click.prevent="RouterService.goToTableItem('input', mappingVariable.id)"/>
              <b>{{ mappingVariable.macro }}</b>:
              {{ mappingVariable.description }}<br>
            </div>
          </VCardText>
        </VCard>

        <VCard class="mt-4" variant="tonal">
          <VCardTitle>
            Macros
            <VDialog>
              <template v-slot:activator="{ props: activatorProps }">
                <FontAwesomeIcon icon="circle-plus" class="pointer" v-bind="activatorProps"/>
              </template>
              <template v-slot:default="{ isActive }">
                <VCard>
                  <MacroList :create="false" @clickRow="e => createMappingEntity('macro', e.id)"/>
                </VCard>
              </template>
            </VDialog>
          </VCardTitle>
          <VCardText>
            <div v-for="mappingVariable in macros()">
              <FontAwesomeIcon icon="circle-info" class="pointer circle-info"
                               @click.prevent="RouterService.goToTableItem('macro', mappingVariable.id)"/>
              <b>{{ mappingVariable.macro }}</b>:
              {{ mappingVariable.description }} <br>
            </div>
          </VCardText>
        </VCard>

        <VCard variant="plain" title="Output" v-if="!output()">
          <VCardText>
            <VDialog>
              <template v-slot:activator="{ props: activatorProps }">
                <div class="pointer" v-bind="activatorProps">
                  Bind output
                  <FontAwesomeIcon icon="circle-plus" class="pointer"/>
                </div>
              </template>
              <template v-slot:default="{ isActive }">
                <VCard>
                  <OutputList :create="false" @clickRow="e => createMappingEntity('output', e.id)"/>
                </VCard>
              </template>
            </VDialog>
          </VCardText>
        </VCard>
        <CodeText
            v-if="output()"
            title="Required output format"
            :code="output()?.output"
            :info-icon="true"
            @info="RouterService.goToTableItem('output', output()?.id)"
        />
      </div>

      <ChangesHistory class="mt-4" :prompt="prompt" @preview="p => $emit('preview', p)"/>
    </div>

    <SettingsEditView/>
  </div>
</template>

<style scoped>
@import '/src/styles/hint.css';

.circle-info {
  margin-right: 0.25rem
}
</style>