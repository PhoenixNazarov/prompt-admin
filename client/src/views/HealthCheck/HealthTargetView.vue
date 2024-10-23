<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {HealthDay, HealthTarget, useHealthCheckStore} from "../../stores/healthcheck.store.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import StatusRect from "../Project/Status/StatusRect.vue";

export default defineComponent({
  name: "HealthTargetView",
  components: {StatusRect, FontAwesomeIcon},
  props: {
    healthTarget: {
      type: Object as PropType<HealthTarget>,
      required: true
    }
  },
  setup() {
    const healthCheckStore = useHealthCheckStore()
    return {
      healthCheckStore
    }
  },
  methods: {
    getTargetStatus() {
      const lastUnit = this.healthCheckStore.getLastUnit(this.healthTarget)
      if (lastUnit == undefined) return
      const timeSpent = ((new Date()).getTime() - (new Date(lastUnit.request_datetime)).getTime()) / 1000
      if (timeSpent > 180)
        return;

      return lastUnit.status;
    },
    getStatus(d: number) {
      const day = this.getDay(d)
      if (day == undefined) return 'Undefined'
      const fallTimes = this.getFallTimes(day)
      if (fallTimes > 0) {
        return 'Downtime'
      }
      return `Operational`
    },
    getDescription(d: number) {
      const day = this.getDay(d)
      if (day == undefined) return undefined
      const fallTimes = this.getFallTimes(day)
      if (fallTimes > 0) {
        return `Down for ${fallTimes} minutes`
      }
    },
    getPercentage(d: number) {
      const day = this.getDay(d)
      if (day == undefined) return undefined
      const fallTimes = this.getFallTimes(day)
      return (fallTimes / (60 * 24)) * 200
    },
    getFallTimes(day: HealthDay) {
      let maxTimes = 60 * 24
      if (day.id == this.getDay(1)?.id) {
        const now = new Date()
        maxTimes = now.getHours() * 24 + now.getMinutes()
      }

      const lostTimes = maxTimes - day.count_response_time
      return day.fall_times + lostTimes > 5 ? lostTimes : 0
    },
    showDate(d: number) {
      const date = new Date();
      date.setDate(date.getDate() - d + 1);
      return date
    },
    getDay(d: number) {
      const date = this.showDate(d)
      return this.healthCheckStore.getDays(this.healthTarget)?.find(el => {
        const day = new Date(el.date)
        return day.getDate() == date.getDate() && day.getMonth() == date.getMonth() && day.getFullYear() == date.getFullYear()
      })
    }
  }
})
</script>

<template>
  <VCard variant="outlined">
    <VCardTitle style="font-size: 1rem">
      <div>
        <div>
          <FontAwesomeIcon icon="circle-info" v-if="getTargetStatus() == undefined" color="gray"/>
          <FontAwesomeIcon icon="circle-exclamation" v-else-if="getTargetStatus() == false" color="red"/>
          <FontAwesomeIcon icon="circle-plus" v-else color="green"/>

          {{ healthTarget.title }}
          <a :href="healthTarget.url">
            <FontAwesomeIcon icon="link"/>
          </a>
        </div>
      </div>

    </VCardTitle>
    <VCardText>
      <div class="chart">
        <StatusRect
            :percentage="getPercentage(d)"
            :date="showDate(d)"
            :status="getStatus(d)"
            :description="getDescription(d)"
            v-for="d in 90"
        />
      </div>
    </VCardText>
  </VCard>
</template>

<style scoped>
.chart {
  display: flex;
  flex-direction: row-reverse;
  gap: 0.1rem;
  justify-content: center;
}
</style>