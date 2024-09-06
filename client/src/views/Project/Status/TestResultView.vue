<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {TestResult} from "../../../stores/project/status/testResult.store.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {dateTimeFormat} from '../../Utils';

export default defineComponent({
  name: "TestResultView",
  components: {FontAwesomeIcon},
  props: {
    testResult: {
      type: Object as PropType<TestResult>,
      required: true
    }
  },
  methods: {
    toDateFormat(timestamp: number) {
      return dateTimeFormat(new Date(timestamp * 1000))
    },
    toTimeFormat(seconds: number) {
      return `${Math.floor(seconds / 60)} m : ${Math.floor(seconds % 60)} s`
    }
  }
})
</script>

<template>
  <VCard>
    <VCardTitle>
      <a class="pointer" :href="`#${testResult.id}`" @click.prevent="$emit('selectTestResult', testResult)">TestCase #{{ testResult.id }}</a>
    </VCardTitle>
    <VCardText>
      <div class="mb-2">
        <VChip variant="outlined">
          <FontAwesomeIcon icon="calendar-plus" class="mr-1"/>
          Created
        </VChip>
        {{ toDateFormat(testResult.created) }}
      </div>
      <div class="mb-2">
        <VChip variant="outlined">
          <FontAwesomeIcon icon="clock" class="mr-1"/>
          Duration
        </VChip>
        {{ toTimeFormat(testResult.duration) }}
      </div>
      <div>
        <FontAwesomeIcon icon="circle" class="mr-1" style="color: #03ce03"/>
        Passed: {{ testResult.passed }}
      </div>
      <div>
        <FontAwesomeIcon icon="circle" class="mr-1" style="color: #8b8b8b"/>
        Skipped: {{ testResult.skipped }}
      </div>
      <div>
        <FontAwesomeIcon icon="circle" class="mr-1" style="color: #ff0000"/>
        Error: {{ testResult.error }}
      </div>
      <div>
        <FontAwesomeIcon icon="circle" class="mr-1" style="color: #ff0000"/>
        Failed: {{ testResult.failed }}
      </div>
      <div>
        <FontAwesomeIcon :icon="['far', 'circle']" class="mr-1"/>
        Total: {{ testResult.total }}
      </div>
      <div>
        <FontAwesomeIcon :icon="['far', 'circle']" class="mr-1"/>
        Collected: {{ testResult.collected }}
      </div>
    </VCardText>
  </VCard>
</template>

<style scoped>

</style>