<script lang="ts">
import {defineComponent, PropType} from 'vue'
import ProjectMainView from "../ProjectMainLayout.vue";
import {
  ComponentContextSchema,
  EventSchema,
  HistoryInput,
  inputFromString,
  ReferenceGroupSchema,
  SEPARATORS,
} from "./types";
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
    },
    hash: {
      type: Object as PropType<string[]>
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
    },
    doLoadHashPath(hash_: string[] | undefined): HistoryInput | undefined {
      if (!hash_) return {
        inputType: 'history',
        history: []
      }
      const hash = hash_

      const referenceHistory = []
      for (let i of hash) {
        const nameInput = i.split(SEPARATORS.INNER)
        if (nameInput.length != 1 && nameInput.length != 2) {
          return {
            inputType: 'history',
            history: []
          }
        }
        const name = nameInput[0]
        const input = nameInput[1]

        const parsedInput = input ? inputFromString(input) : undefined
        referenceHistory.push({
          name: name,
          input: parsedInput
        })
      }
      return {
        inputType: 'history',
        history: referenceHistory
      }
    },
  },
  mounted() {
    this.loadSchema()
  }
})
</script>

<template>
  <ProjectMainView :project="project">
    <VSkeletonLoader type="card" v-if="schema == undefined"/>
    <NavigationBuilder
        v-if="schema"
        :component-schema="schema"
        :component-context="context()"
        :input-schema="doLoadHashPath(hash)"
        @event-schema="onEventSchema"
    />
  </ProjectMainView>
</template>

<style scoped>

</style>