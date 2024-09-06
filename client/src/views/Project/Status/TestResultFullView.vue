<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {TestResult} from "../../../stores/project/status/testResult.store.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import TestResultView from "./TestResultView.vue";
import {useTestCaseStore} from "../../../stores/project/status/testCase.store.ts";
import TestCaseView from "./TestCaseView.vue";

export default defineComponent({
  name: "TestResultFullView",
  components: {TestCaseView, TestResultView, FontAwesomeIcon},
  props: {
    testResult: {
      type: Object as PropType<TestResult>,
      required: true
    }
  },
  setup() {
    const testCaseStore = useTestCaseStore()
    return {
      testCaseStore
    }
  },
  async mounted() {
    if (this.testResult.id) {
      await this.testCaseStore.loadTestResult(this.testResult.id)
    }
  },
})
</script>

<template>
  <VCard>
    <VCardTitle>
      <FontAwesomeIcon icon="arrow-left" class="pointer" @click.prevent="$emit('back')"/>
    </VCardTitle>
    <VCardText v-if="testResult.id">
      <TestResultView class="mb-4" :test-result="testResult"/>

      <VSkeletonLoader type="paragraph" v-if="
        testCaseStore.loaded.get(testResult.id) == undefined ||
        testCaseStore.loaded.get(testResult.id) == true
      "/>

      <VExpansionPanels multiple v-else>
        <TestCaseView :test-case="testCase"
                      v-for="testCase in testCaseStore.getByTestResultId(testResult.id).filter(v => v.outcome == 'error' || v.outcome == 'failed' || v.outcome == 'skipped')"/>
        <TestCaseView :test-case="testCase"
                      v-for="testCase in testCaseStore.getByTestResultId(testResult.id).filter(v => !(v.outcome == 'error' || v.outcome == 'failed' || v.outcome == 'skipped'))"/>
      </VExpansionPanels>

    </VCardText>
  </VCard>
</template>

<style scoped>

</style>