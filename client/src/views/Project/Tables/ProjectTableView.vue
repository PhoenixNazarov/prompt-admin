<script lang="ts">
import {defineComponent} from 'vue'
import ProjectMainView from "../ProjectMainLayout.vue";
import {ComponentContextSchema, EventSchema, ReferenceGroupSchema,} from "./types";
import NavigationBuilder from "./Components/Navigation/NavigationBuilder.vue";
import EventDispatcher from "./EventDispatcher.ts";
import {useTableStore} from "../../../stores/project/tables/table.store.ts";


export default defineComponent({
  name: "ProjectTableView",
  components: {NavigationBuilder, ProjectMainView},
  props: {
    project: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      schema: undefined as ReferenceGroupSchema | undefined,
    }
  },
  setup() {
    const tableStore = useTableStore()
    return {
      tableStore
    }
  },
  methods: {
    onEventSchema(event: EventSchema) {
      EventDispatcher.onProjectEvent(event)
    },
    context(): ComponentContextSchema {
      return {
        componentContext: {
          project: this.project
        }
      }
    },
    async loadSchema() {
      this.schema = await this.tableStore.loadSchema(this.project)
    }
  },
  mounted() {
    this.loadSchema()
  },
})
</script>

<template>
  <ProjectMainView :project="project">
    <VSkeletonLoader type="card" v-if="schema == undefined"/>
    <NavigationBuilder
        v-if="schema"
        :component-schema="schema"
        :component-context="context()"
        @event-schema="onEventSchema"
    />
  </ProjectMainView>
</template>

<style scoped>

</style>