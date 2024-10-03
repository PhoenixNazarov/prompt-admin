<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {
  ChangeContextEvent,
  EventSchema,
  HistoryInput,
  InputSchema,
  inputToString,
  NamedGroup,
  ReferenceGroupSchema,
  SEPARATORS
} from "../../types";
import GroupBuilder from "../Group/GroupBuilder.vue";
import ComponentSchemaMixin from "../Mixins/ComponentSchemaMixin.ts";

export default defineComponent({
  name: "ReferenceGroupSchemaComponent",
  mixins: [ComponentSchemaMixin],
  components: {GroupBuilder},
  props: {
    componentSchema: {
      type: Object as PropType<ReferenceGroupSchema>,
      required: true
    }
  },
  data() {
    return {
      referenceHistory: [] as { group: NamedGroup, input?: InputSchema }[],
      referencePopup: undefined as { group: NamedGroup, input?: InputSchema } | undefined,
      referencePopupShow: false
    }
  },
  methods: {
    getNamedGroup(name: string) {
      return this.componentSchema.refs.find(s => s.name == name)
    },
    doSetReference(name: string, inputSchema: InputSchema | undefined) {
      const namedGroup = this.getNamedGroup(name)
      if (namedGroup) {
        this.referenceHistory = [{group: namedGroup, input: inputSchema}]
      }
    },
    doOverlappingReference(name: string, inputSchema: InputSchema | undefined) {
      const namedGroup = this.getNamedGroup(name)
      if (namedGroup) {
        this.referenceHistory.push({group: namedGroup, input: inputSchema})
      }
    },
    doPopup(name: string, inputSchema: InputSchema | undefined) {
      const namedGroup = this.getNamedGroup(name)
      if (namedGroup) {
        this.referencePopup = {group: namedGroup, input: inputSchema}
        this.referencePopupShow = true
      }
    },
    doCloseReference() {
      this.referenceHistory.pop()
    },
    doPopupClose() {
      this.referencePopupShow = false
      this.referencePopup = undefined
    },
    doGoToReference(index: number) {
      this.referenceHistory = this.referenceHistory.slice(0, index)
    },
    onEventSchema(event: EventSchema) {
      if (event.eventType == 'render-reference') {
        switch (event.overlay) {
          case "set":
            return this.doSetReference(event.name, event.inputSchema)
          case "overlapping":
            return this.doOverlappingReference(event.name, event.inputSchema)
          case 'popup':
            return this.doPopup(event.name, event.inputSchema)
          case 'close':
            return this.doCloseReference()
        }
      } else if (event.eventType == 'close-popup-reference') {
        this.doPopupClose()
      } else if (event.eventType == 'set-reference-context') {
        const suffixKey = event.keySuffix ? '.' + event.keySuffix : ''
        const newEvent: ChangeContextEvent = {
          eventType: 'change-context',
          contextKey: '$' + this.referenceHistory[this.referenceHistory.length - 1]?.group.name + suffixKey,
          value: event.value
        }
        this.doEmitEventSchema(newEvent)
      } else {
        this.doEmitEventSchema(event)
      }
    },
    doSetMainRef() {
      const startName = this.componentSchema.mainRefName ? this.componentSchema.mainRefName : this.componentSchema.refs[0].name
      // this.doSetReference(startName, undefined)
    },
    getMainRef() {
      const startName = this.componentSchema.mainRefName ? this.componentSchema.mainRefName : this.componentSchema.refs[0].name
      return this.getNamedGroup(startName)
    },
    doLoadHashPath(historyInput: HistoryInput) {
      const referenceHistory = [] as typeof this.referenceHistory
      if (historyInput.history.length <= 0) {
        return this.doSetMainRef()
      }
      for (let i of historyInput.history) {

        const nameGroup = this.getNamedGroup(i.name)
        const parsedInput = i.input
        if (!nameGroup) {
          return this.doSetMainRef()
        }
        referenceHistory.push({
          group: nameGroup,
          input: parsedInput
        })
      }
      this.referenceHistory = referenceHistory
    },
    doDumpHashPath() {
      const hash = this.referenceHistory.map(el => {
        if (el.input)
          return `${el.group.name}${SEPARATORS.INNER}${inputToString(el.input)}`
        else
          return `${el.group.name}`
      })
      this.$router.push(`/project/${this.PROJECT}/tables/${hash.join(SEPARATORS.EXTERNAL)}`)
    }
  },
  mounted() {
    if (this.inputSchema?.inputType == 'history') {
      this.doLoadHashPath(this.inputSchema)
    } else {
      this.doSetMainRef()
    }
  },
  watch: {
    referenceHistory: {
      handler() {
        setTimeout(this.doDumpHashPath, 100)
      },
      deep: true
    },
    inputSchema: {
      handler() {
        if (this.inputSchema?.inputType == 'history') {
          if (JSON.stringify(this.inputSchema.history.map(el => el.name)) != JSON.stringify(this.referenceHistory.map(el => el.group.name))) {
            this.doLoadHashPath(this.inputSchema)
          }
        }
      },
      deep: true
    }
  }
})
</script>

<template>
  <div>
    <VBreadcrumbs bg-color="var(--color-4)" class="mb-5" density="compact"
                  :items="[{group: getMainRef()!}, ...referenceHistory].map((el, ind) => { return { title: el.group.name, index: ind}})">
      <template v-slot:item="{ item }">
        <VBreadcrumbsItem @click="doGoToReference(item.index)">
          {{ item.title }}
        </VBreadcrumbsItem>
      </template>
    </VBreadcrumbs>
    <GroupBuilder
        v-if="referenceHistory.length <= 0"
        :component-schema="getMainRef()!.group"
        :component-context="componentContext"
        @event-schema="onEventSchema"
    />
    <GroupBuilder
        v-if="referenceHistory[referenceHistory.length - 1]?.group"
        :component-schema="referenceHistory[referenceHistory.length - 1]?.group.group"
        :component-context="componentContext"
        :input-schema="referenceHistory[referenceHistory.length - 1]?.input"
        @event-schema="onEventSchema"
    />
    <VDialog v-model="referencePopupShow">
      <GroupBuilder
          v-if="referencePopup"
          :component-schema="referencePopup.group.group"
          :component-context="componentContext"
          :input-schema="referencePopup.input"
          @event-schema="onEventSchema"
      />
    </VDialog>
  </div>
</template>

<style scoped>

</style>