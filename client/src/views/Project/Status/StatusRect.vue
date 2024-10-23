<script lang="ts">
import {defineComponent} from 'vue'
import {dateFormat} from "../../Utils.ts";

export default defineComponent({
  name: "StatusRect",
  props: {
    date: {
      type: Date,
      required: true
    },
    percentage: {
      type: Number
    },
    status: {
      type: String
    },
    description: {
      type: String
    }
  },
  data() {
    return {
      show: false,
      color: this.getColor(this.percentage)
    }
  },
  methods: {
    dateFormat,
    getColor(color: number | undefined) {
      if (color != 0 && (!color || color == -1)) {
        return 'var(--color-4)'
      }
      const hue = (Math.max(1 - color, 0) * 100).toString(10);
      return ["hsl(", hue, ",100%,45%)"].join("");
    }
  }
})
</script>

<template>
  <VTooltip
      v-model="show"
      location="bottom"
  >
    <template v-slot:activator="{ props }">
      <div class="rect pointer" v-bind="props" @click.prevent="$emit('select')"/>
    </template>
    <div class="t-window">
      <div v-if="status">
        {{ status }}
      </div>
      <div v-if="description" v-html="description">
      </div>
      <div>
        {{ dateFormat(date) }}
      </div>
    </div>
  </VTooltip>
</template>

<style scoped>
.rect {
  width: 0.5rem;
  height: 2rem;
  background-color: v-bind(color);
}

.t-window {
  min-width: 150px;
}
</style>