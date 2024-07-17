<script lang="ts">
import {defineComponent} from 'vue'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {RouterService} from "../plugins/router.ts";

export default defineComponent({
  name: "MainLayout",
  computed: {
    RouterService() {
      return RouterService
    }
  },
  components: {FontAwesomeIcon}
})
</script>

<template>
  <div>
    <div class="header">
      <div class="name case" @click.prevent="RouterService.goToWorkplace()">Prompt Admin</div>
      <div class="case" @click.prevent="RouterService.goToWorkplace()">
        <FontAwesomeIcon icon="pen"/>
        Editor
      </div>

      <div class="case" @click.prevent="RouterService.goToFormat()">
        <FontAwesomeIcon icon="calculator"/>
        Format
      </div>

      <div class="case" @click.prevent="RouterService.goToTableList()">
        <FontAwesomeIcon icon="table"/>
        Table
      </div>
    </div>
    <div class="inner">
      <RouterView/>
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