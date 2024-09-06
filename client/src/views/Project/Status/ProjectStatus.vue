<script lang="ts">
import {defineComponent} from 'vue'
import ProjectMainView from "../ProjectMainLayout.vue";
import StatusRect from "./StatusRect.vue";
import {TestResult, useTestResultStore} from "../../../stores/project/status/testResult.store.ts";
import {dateFormat} from "../../Utils.ts";
import TestResultView from "./TestResultView.vue";
import TestResultFullView from "./TestResultFullView.vue";

export default defineComponent({
  name: "ProjectStatus",
  components: {TestResultFullView, TestResultView, StatusRect, ProjectMainView},
  props: {
    project: {
      type: String,
      required: true
    },
    testResultId: {
      type: Number
    }
  },
  setup() {
    const testResultStore = useTestResultStore()
    return {
      testResultStore
    }
  },
  data() {
    return {
      selectDate: 1,
      selectTestResult: undefined as undefined | TestResult
    }
  },
  methods: {
    dateFormat,
    showDate(d: number) {
      const date = new Date();
      date.setDate(date.getDate() - d + 1);
      return date
    },
    getDateResults(d: number) {
      const now = new Date();
      now.setDate(now.getDate() - d + 1);
      now.setHours(0)
      now.setMinutes(0)
      now.setSeconds(0)
      const secondComp = new Date(now)
      secondComp.setHours(24)
      const prevT = now.getTime() / 1000
      const nextT = secondComp.getTime() / 1000
      return this.testResultStore.entity.filter(el => prevT <= el.created && el.created < nextT).sort((a, b) => b.created - a.created)
    },
    showPercentage(d: number) {
      const currentResults = this.getDateResults(d)
      if (currentResults.length <= 0) return -1
      const total = currentResults.reduce((sm, el) => sm += el.total, 0)
      const passed = currentResults.reduce((sm, el) => sm += el.passed + el.skipped, 0)
      console.log(total, passed)
      if (total == 0) return -1
      return 1 - passed / total
    },
    doSelectDate(d: number) {
      this.selectDate = d
      this.selectTestResult = undefined
      this.$router.push({hash: ''})
    },
    doSelectTestResult(testResult: TestResult) {
      this.$router.push({hash: `#${testResult.id}`})
      this.selectTestResult = testResult
    },
    loadHashTestResult() {
      const id = this.$route.hash.replace('#', '')
      try {
        const numberId = Number.parseInt(id)
        const testResult = this.testResultStore.getById(numberId)
        if (!testResult) {
          this.$router.push({hash: ''})
          return
        }
        this.selectTestResult = testResult
      } catch (e) {
        this.$router.push({hash: ''})
      }
    }
  },
  async mounted() {
    await this.testResultStore.load30Project(this.project)
    this.loadHashTestResult()
  },
})
</script>

<template>
  <ProjectMainView :project="project">
    <VCard class="mb-5">
      <VCardTitle>
        Status
      </VCardTitle>
      <VCardText>
        <VSkeletonLoader type="card" v-if="testResultStore.loading.load30"/>
        <div class="chart-external" v-else>
          <div>
            <div class="chart">
              <StatusRect
                  :percentage="showPercentage(d)"
                  :date="showDate(d)"
                  @select="doSelectDate(d)"
                  v-for="d in 30"
              />
            </div>
            <div class="mt-1 chart-hint">
              <span>
                30 days ago
              </span>
              <span>
                Today
              </span>
            </div>
          </div>
        </div>
      </VCardText>
    </VCard>
    <VCard variant="text" v-if="!testResultStore.loading.load30 && selectTestResult == undefined">
      <VCardTitle style="color: black">
        Date: {{ dateFormat(showDate(selectDate)) }}
      </VCardTitle>
      <VCardText>
        <TestResultView class="mb-4" :test-result="tr" v-for="tr in getDateResults(selectDate)"
                        @selectTestResult="doSelectTestResult"/>
      </VCardText>
    </VCard>
    <TestResultFullView :test-result="selectTestResult" v-if="selectTestResult" @back="doSelectDate(selectDate)"/>
  </ProjectMainView>
</template>

<style scoped>
.chart {
  display: flex;
  flex-direction: row-reverse;
  gap: 0.25rem;
}

.chart-external {
  display: flex;
  justify-content: center;
}

.chart-hint {
  display: flex;
  justify-content: space-between;
}
</style>