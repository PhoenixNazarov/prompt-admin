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
      const hue = ((1 - color) * 120).toString(10);
      return ["hsl(", hue, ",100%,50%)"].join("");
    }
  }
})
</script>

<template>
  <VTooltip
      v-model="show"
      location="top"
  >
    <template v-slot:activator="{ props }">
      <div class="rect pointer" v-bind="props" @click.prevent="$emit('select')"/>
    </template>
    <div>
      <span>{{ dateFormat(date) }}</span>
    </div>
  </VTooltip>
</template>

<style scoped>
.rect {
  width: 0.5rem;
  height: 2rem;
  background-color: v-bind(color);
}
</style>