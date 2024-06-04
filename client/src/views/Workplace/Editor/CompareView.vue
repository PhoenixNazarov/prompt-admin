<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt} from "../../../stores/prompt.store.ts";
import {Diff} from "vue-diff";

export default defineComponent({
  name: "CompareView",
  components: {Diff},
  props: {
    prompt: {
      type: Object as PropType<Prompt>,
      required: true
    }
  },
  data() {
    return {
      height: (window.innerHeight - 5 * parseFloat(getComputedStyle(document.documentElement).fontSize))
    }
  }
})
</script>

<template>
  <div>
    <Diff
        mode="split"
        theme="light"
        language="xml"
        :prev="prompt.audit!!.value"
        :current="prompt.value"
        :virtual-scroll="{ height: height, 'asd': '123' }"
        style="    font-size: 0.5rem;"
    />
  </div>
</template>

<style scoped>
</style>