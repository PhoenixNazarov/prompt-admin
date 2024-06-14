<script lang="ts">
import {defineComponent} from 'vue'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

export default defineComponent({
  name: "MainLayout",
  components: {FontAwesomeIcon}
})
</script>

<template>
  <div>
    <div class="header">
      <div class="name case" @click.prevent="$emit('setView', 'workplace')">Prompt Admin</div>
      <div class="case" @click.prevent="$emit('setView', 'workplace')">
        <FontAwesomeIcon icon="pen"/>
        Editor
      </div>

      <div class="case" @click.prevent="$emit('setView', 'format')">
        <FontAwesomeIcon icon="calculator"/>
        Format
      </div>
    </div>
    <div class="inner">
      <slot/>
    </div>
  </div>
</template>

<style scoped>
.header {
  height: 3rem;
  background-color: var(--color-5);
  display: flex;
  align-items: center;
}

.name {
  color: var(--color-3);
  font-size: 1.5rem;
  text-transform: uppercase;
  font-weight: 600;
  padding: 0.35rem;
}

.inner {
  height: calc(100vh - 3rem);
  background-color: var(--color-3);
}

.case {
  margin-right: 2rem;
  cursor: pointer;
}

</style>