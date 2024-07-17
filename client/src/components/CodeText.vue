<script lang="ts">
import {defineComponent} from 'vue'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

export default defineComponent({
  name: "CodeText",
  components: {FontAwesomeIcon},
  props: {
    title: {
      type: String
    },
    code: {
      type: String
    },
    error: {
      type: String
    },
    infoIcon: {
      type: Boolean,
      default: false
    }
  }
})
</script>

<template>
  <VCard variant="text">
    <VCardTitle>
      {{ title }}
      <FontAwesomeIcon v-if="infoIcon" icon="circle-info" class="pointer" @click.prevent="$emit('info')"/>
    </VCardTitle>
    <VCardText>
      <div class="program-general" :class="{'program-error': code != undefined}" v-if="error">
        {{ error }}
      </div>
      <div class="program-general program" v-if="code">{{ code }}</div>
    </VCardText>
  </VCard>
</template>

<style scoped>
@import '/src/styles/hint.css';

.program-general {
  padding: 1rem;
  border-radius: 0.5rem;
  white-space: break-spaces;
}

.program-error {
  margin-bottom: 1rem;
}

.v-card-text {
  padding: 0;
}
</style>