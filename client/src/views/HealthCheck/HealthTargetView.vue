<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {HealthTarget, useHealthCheckStore} from "../../stores/healthcheck.store.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import StatusRect from "../Project/Status/StatusRect.vue";
import {HealthDayService} from "./HealthDay.service.ts";
import {Line} from 'vue-chartjs'
import moment from "moment";

export default defineComponent({
  name: "HealthTargetView",
  components: {StatusRect, FontAwesomeIcon, Line},
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
  computed: {
    options() {
      return {
        plugins: {
          tooltip: {
            mode: 'index',
            intersect: false
          },
          legend: {
            display: false // это отключает отображение легенды на графике
          },
        },
        elements: {
          point: {
            radius: 0.1
          }
        },
        scales: {
          y: {
            ticks: {
              // Include a dollar sign in the ticks
              callback: function(value, index, ticks) {
                return value + ' s';
              }
            },
          },
          x: {
            type: 'time',
            grid: {
              display: false
            }
          }
        },
        responsive: true,
        maintainAspectRatio: false,
      }
    }
  },
  methods: {
    getTargetStatus() {
      const lastUnit = this.healthCheckStore.getLastUnit(this.healthTarget)
      if (lastUnit == undefined) return
      const timeSpent = ((new Date()).getTime() - (new Date(lastUnit.request_datetime)).getTime()) / 1000
      if (timeSpent > 180)
        return;

      return lastUnit.status
    },
    getChartData() {
      const units = this.healthCheckStore.getUnits(this.healthTarget)?.reverse()
      if (units == undefined) return []
      return {
        labels: units?.map(el => moment(el.request_datetime)),
        datasets: [{
          label: 'Response Time',
          data: units?.map(el => el.response_time),
          borderWidth: 1,
          borderColor: 'rgb(0,83,255)',
        }]
      }
    },
    buildDayStatuses() {
      const result = []
      for (let i = 1; i < 90; i++) {
        const healthDayService = HealthDayService.fromDay(this.healthTarget, i);
        result.push({
          percentage: healthDayService.getPercentage(),
          date: HealthDayService.showDate(i),
          status: healthDayService.getStatus(),
          description: healthDayService.getDescription(),
        })
      }
      return result
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
            :percentage="d.percentage"
            :date="d.date"
            :status="d.status"
            :description="d.description"
            v-for="d in buildDayStatuses()"
        />
      </div>
      <p class="ma-1">
        Response Times:
      </p>
      <div v-if="healthCheckStore.getUnits(healthTarget)" style="height: 10rem">
        <Line :data="getChartData()" :options="options"/>
      </div>
      <VSkeletonLoader type="article" v-else/>

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