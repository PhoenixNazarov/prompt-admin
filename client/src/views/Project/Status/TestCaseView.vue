<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {TestCase} from "../../../stores/project/status/testCase.store.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {TestCaseInfo, useTestCaseInfoStore} from "../../../stores/project/status/testCaseInfo.store.ts";
import CodeText from "../../../components/CodeText.vue";

export default defineComponent({
  name: "TestCaseView",
  components: {CodeText, FontAwesomeIcon},
  props: {
    testCase: {
      type: Object as PropType<TestCase>,
      required: true
    }
  },
  setup() {
    const testCaseInfoStore = useTestCaseInfoStore()
    return {
      testCaseInfoStore
    }
  },
  data() {
    return {
      outcomeColor: this.getOutcomeColor()
    }
  },
  methods: {
    getOutcomeColor(outcome: string) {
      if (outcome == 'passed')
        return '#03ce03'
      if (outcome == 'skipped')
        return '#8b8b8b'
      return '#ff0000'
    },
    testCaseInfo(): TestCaseInfo | undefined {
      if (this.testCase.id)
        return this.testCaseInfoStore.entity.get(this.testCase.id)
    }
  }
})
</script>

<template>
  <VExpansionPanel v-if="testCase.id">
    <VExpansionPanelTitle @click.prevent="testCaseInfoStore.loadTestCase(testCase.id)">
      <FontAwesomeIcon icon="circle" class="mr-1" :style="{color: getOutcomeColor(testCase.outcome)}"/>
      {{ testCase.metadata_url || testCase.nodeid }}
      <span class="ml-1" style="color: var(--color-4)">
        {{
          Math.floor(testCase.setup_duration + (testCase.call_duration || 0) + testCase.teardown_duration)
        }}s
        <span class="ml-1">
          {{ testCase.metadata_scenario }}
        </span>
      </span>
    </VExpansionPanelTitle>
    <VExpansionPanelText>
      <div class="mb-2">
        <div class="mb-2">
          <span>
          {{ testCase.nodeid }}
          </span>
          <span class="ml-1" style="color: var(--color-4)">
            lineno {{ testCase.lineno }}
          </span>
        </div>
        <div class="mb-1">
          Url: {{ testCase.metadata_url }}
        </div>
        <div v-if="testCase.metadata_scenario" class="mb-1">
          Scenario: {{ testCase.metadata_scenario }}
        </div>
        <div class="mb-1">
          Status:
          <VChip density="compact" :color="getOutcomeColor(testCase.outcome)">
            {{ testCase.outcome }}
          </VChip>
        </div>
        <div class="mb-3">
          Duration:
          <VChip density="compact">
            {{ Math.floor(testCase.setup_duration + (testCase.call_duration || 0) + testCase.teardown_duration) }} s
          </VChip>
        </div>
        <div class="mb-1">
          Setup:
          <VChip density="compact" :color="getOutcomeColor(testCase.setup_outcome)">
            {{ testCase.setup_outcome }}
          </VChip>
          {{ testCase.setup_duration }} s
        </div>
        <div class="mb-1">
          Call:
          <VChip v-if="testCase.call_outcome" density="compact" :color="getOutcomeColor(testCase.call_outcome)">
            {{ testCase.call_outcome }}
          </VChip>
          {{ testCase.call_duration }} s
        </div>
        <div class="mb-5">
          Teardown:
          <VChip density="compact" :color="getOutcomeColor(testCase.teardown_outcome)">
            {{ testCase.teardown_outcome }}
          </VChip>
          {{ testCase.teardown_duration }} s
        </div>
      </div>
      <VSkeletonLoader type="article" v-if="
        testCaseInfoStore.loaded.get(testCase.id) == undefined ||
        testCaseInfoStore.loaded.get(testCase.id) == true
      "/>

      <div v-if="testCaseInfo()">
        <div v-if="testCaseInfo()?.setup_longrepr" class="mb-2" >
          <CodeText title="setup_longrepr" :error="testCaseInfo()?.setup_longrepr"/>
          {{  }}
        </div>

        <div v-if="testCaseInfo()?.call_crash_path" class="mb-2">
          call_crash_path:
          {{ testCaseInfo()?.call_crash_path }}
        </div>

        <div v-if="testCaseInfo()?.call_crash_lineno" class="mb-2">
          call_crash_lineno:
          {{ testCaseInfo()?.call_crash_lineno }}
        </div>

        <div v-if="testCaseInfo()?.call_crash_message" class="mb-2" >
          <CodeText title="call_crash_message" :error="testCaseInfo()?.call_crash_message"/>
        </div>
        <div v-if="testCaseInfo()?.request" class="mb-2" >
          <CodeText title="request" :code="testCaseInfo()?.request"/>
        </div>
        <div v-if="testCaseInfo()?.response" class="mb-2" >
          <CodeText title="response" :code="testCaseInfo()?.response"/>
        </div>

      </div>

    </VExpansionPanelText>
  </VExpansionPanel>
</template>

<style scoped>
</style>