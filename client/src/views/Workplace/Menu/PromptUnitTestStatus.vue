<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt} from "../../../stores/prompt.store.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {SyncData} from "../../../stores/config/syncData.store.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";

export default defineComponent({
  name: "PromptUnitTestStatus",
  components: {FontAwesomeIcon},
  props: {
    prompt: {
      type: Object as PropType<Prompt>,
      required: true
    }
  },
  setup() {
    const mappingEntityStore = useMappingEntityStore()
    const mappingStore = useMappingStore()
    return {
      mappingEntityStore,
      mappingStore
    }
  },
  data() {
    return {
      show: false
    }
  },
  methods: {
    syncData(): SyncData | undefined {
      const mapping = this.mapping()
      if (mapping && this.prompt) return this.mappingEntityStore.getSyncDataByFilter(mapping, this.prompt)
      return undefined
    },
    mapping(): Mapping | undefined {
      if (this.prompt) return this.mappingStore.getById(this.prompt.mapping_id)
    },
    selectPrompt() {
      this.$emit('selectPrompt', {...this.prompt, unitTestData: {syncData: this.syncData()}})
    }
  }
})
</script>

<template>
  <VTooltip
      v-model="show"
      location="top"
      v-if="syncData()"
  >
    <template v-slot:activator="{ props }">
      <FontAwesomeIcon  @click.stop="selectPrompt" v-if="syncData()?.test_exception" :icon="['fas', 'circle']" style="color: var(--color-1)"
                       v-bind="props"/>
      <FontAwesomeIcon  @click.stop="selectPrompt" v-else-if="syncData()?.test_status == 'execution'" :icon="['fas', 'circle']" style="color: green"
                       v-bind="props"/>
      <FontAwesomeIcon  @click.stop="selectPrompt" v-else-if="syncData()?.test_status == 'wait'" :icon="['far', 'circle']"
                       v-bind="props"/>
      <FontAwesomeIcon  @click.stop="selectPrompt" v-else :spin="true" icon="spinner" v-bind="props"/>
    </template>
    <div>
      <span v-if="syncData()?.test_exception">{{ syncData()?.test_exception }}</span>
      <span v-else-if="syncData()?.test_status == 'execution'">Complete</span>
      <span v-else-if="syncData()?.test_status == 'wait'">Waiting</span>
      <span v-else>Processing</span>
    </div>
  </VTooltip>
</template>

<style scoped>

</style>