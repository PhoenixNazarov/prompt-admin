<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt} from "../../../stores/prompt.store.ts";
import HintView from "./HintView.vue";
import TemplateHintView from "./TemplateHintView.vue";

export default defineComponent({
  name: "MainHintView",
  components: {TemplateHintView, HintView},
  props: {
    prompt: {
      type: Object as PropType<Prompt>
    }
  },
})
</script>

<template>
  <div>
    <TemplateHintView :prompt="prompt" v-if="prompt?.templateData" @closePrompt="p =>$emit('closePrompt', p)"/>
    <HintView :prompt="prompt" v-else @preview="p => $emit('preview', p)"/>
  </div>
</template>

<style scoped>

</style>