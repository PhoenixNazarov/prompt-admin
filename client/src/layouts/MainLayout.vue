<script lang="ts">
import {defineComponent} from 'vue'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {RouterService} from "../plugins/router.ts";
import {useProjectStore} from "../stores/project/project.store.ts";

export default defineComponent({
  name: "MainLayout",
  computed: {
    RouterService() {
      return RouterService
    }
  },
  components: {FontAwesomeIcon},
  setup() {
    const projectStore = useProjectStore()
    return {
      projectStore
    }
  },
  mounted() {
    this.projectStore.loadProjects()
  },
})
</script>

<template>
  <div>
    <div class="header">
      <a href="/workplace" class="name" @click.prevent="RouterService.goToWorkplace()">Prompt Admin</a>
      <a href="/workplace" class="case" @click.prevent="RouterService.goToWorkplace()">
        <FontAwesomeIcon icon="pen"/>
        Editor
      </a>

      <VMenu>
        <template v-slot:activator="{ props }">
          <div class="case" v-bind="props">
            <FontAwesomeIcon icon="diagram-project"/>
            Project
          </div>
        </template>
        <div style="background-color: var(--color-5); padding:0.25rem; border-radius: 0.2rem">
          <div v-for="project in projectStore.projects" style="display: flex;justify-content: center;">
            <a :href="`/project/${project}/group/-1`" class="pointer case"
               @click.prevent="RouterService.goToProject(project)"
               style="margin-right: 0 !important; text-align: center; width: 100%;"
            >
              {{ project }}
            </a>
          </div>
        </div>
      </VMenu>

      <a href="/table/mapping" class="case" @click.prevent="RouterService.goToTableList()">
        <FontAwesomeIcon icon="table"/>
        Table
      </a>

      <a href="/account" class="case" @click.prevent="RouterService.goToAccount()">
        <FontAwesomeIcon icon="user"/>
        Account
      </a>

      <a href="/healthcheck" class="case" @click.prevent="RouterService.goToHealthCheck()">
        <FontAwesomeIcon icon="heart-pulse"/>
        Health Monitor
      </a>

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
  font-size: 1rem;
  text-transform: uppercase;
  font-weight: 600;
  padding: 0.4rem;
  margin-right: 2rem;
  cursor: pointer;
  text-decoration: none;
}

.inner {
  height: calc(100vh - 3rem);
  background-color: var(--color-3);
}

.case {
  margin-right: 1rem;
  cursor: pointer;
  padding: 0.4rem 0.8rem;
  text-decoration: none;
}

.case:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 0.4rem;
}

.case:visited {
  color: inherit;
}

</style>