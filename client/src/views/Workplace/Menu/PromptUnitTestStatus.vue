<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt} from "../../../stores/prompt.store.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {SyncData} from "../../../stores/config/syncData.store.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {UnitTest, useUnitTestStore} from "../../../stores/config/unitTest.store.ts";

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
    const unitTestStore = useUnitTestStore()
    return {
      mappingEntityStore,
      mappingStore,
      unitTestStore
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
    unitTest(): UnitTest | undefined {
      const syncData = this.syncData()
      if (syncData && syncData.id && this.prompt.name) return this.unitTestStore.getBySyncDataName(syncData.id, this.prompt.name)
    },
    mapping(): Mapping | undefined {
      if (this.prompt) return this.mappingStore.getById(this.prompt.mapping_id)
    },
    selectPrompt() {
      const unitTest = this.unitTest()
      if (unitTest) this.$emit('selectPrompt', {...this.prompt, unitTestData: {unitTest: unitTest}})
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
      <FontAwesomeIcon @click.stop="selectPrompt" v-if="unitTest()?.test_exception" :icon="['fas', 'circle']"
                       style="color: var(--color-1)"
                       v-bind="props"/>
      <FontAwesomeIcon @click.stop="selectPrompt" v-else-if="unitTest()?.test_status == 'execution'"
                       :icon="['fas', 'circle']" style="color: green"
                       v-bind="props"/>
      <FontAwesomeIcon @click.stop="selectPrompt" v-else-if="unitTest()?.test_status == 'wait'"
                       :icon="['far', 'circle']"
                       v-bind="props"/>
      <FontAwesomeIcon @click.stop="selectPrompt" v-else :spin="true" icon="spinner" v-bind="props"/>
    </template>
    <div>
      <span v-if="unitTest()?.test_exception">{{ unitTest()?.test_exception }}</span>
      <span v-else-if="unitTest()?.test_status == 'execution'">Complete</span>
      <span v-else-if="unitTest()?.test_status == 'wait'">Waiting</span>
      <span v-else>Processing</span>
    </div>
  </VTooltip>
</template>

<style scoped>

</style>