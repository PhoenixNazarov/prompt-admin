<script lang="ts">
import {defineAsyncComponent, defineComponent, PropType} from 'vue'
import {
  ApprovedDeleteItemEvent,
  CardSchema,
  ChangeContextEvent,
  CloseReferencePopupEvent,
  ComponentContextType,
  DeleteItemEvent,
  EventSchema,
  RenderReferenceEvent,
  SaveItemEvent,
  SetReferenceContextEvent
} from "../../types";
import GroupSchemaMixin from "../Mixins/GroupSchemaMixin.ts";
import {useTableStore} from "../../../../../stores/project/tables/table.store.ts";
import EventDispatcher from "../../EventDispatcher.ts";
import UtilSchema from "../UtilSchema.ts";

export default defineComponent({
  name: "CardSchemaComponent",
  mixins: [GroupSchemaMixin],
  components: {
    GroupBuilder: defineAsyncComponent(() => import("../Group/GroupBuilder.vue") as any),
  },
  setup() {
    const tableStore = useTableStore()
    return {
      tableStore
    }
  },
  props: {
    componentSchema: {
      type: Object as PropType<CardSchema>,
      required: true
    }
  },
  data() {
    return {
      loading: true
    }
  },
  methods: {
    setReferenceContext(value: ComponentContextType) {
      if (this.componentSchema.reference) {
        const event: ChangeContextEvent = {
          eventType: 'change-context',
          contextKey: this.componentSchema.reference,
          value: value
        }
        this.$emit('event-schema', event)
      } else {
        const event: SetReferenceContextEvent = {
          eventType: 'set-reference-context',
          value: value
        }
        this.$emit('event-schema', event)
      }
    },
    async doLoadItem(table: string, id: number) {
      try {
        this.loading = true
        const item = await this.tableStore.loadItem(this.PROJECT, table, id)
        this.setReferenceContext(
            {
              item: item,
              _item: JSON.parse(JSON.stringify(item))
            }
        )
      } finally {
        this.loading = false
      }
    },
    doTriggerInput() {
      if (this.inputSchema?.inputType == 'create-item') {
        this.setReferenceContext(
            {
              item: undefined,
              _item: undefined
            }
        )
        this.loading = false
      } else if (this.inputSchema?.inputType == 'item') {
        const table = this.inputSchema.table || this.componentSchema.table
        if (table) {
          this.doLoadItem(table, this.inputSchema.id)
        } else {
          this.loading = false
        }
      } else if (this.inputSchema?.inputType == 'delete-item') {
        this.setReferenceContext(
            {
              _delete: {
                id: this.inputSchema.id,
                table: this.inputSchema.table
              }
            }
        )
        this.loading = false
      } else {
        this.loading = false
      }
    },
    getId() {
      if (!this.componentSchema.reference || !this.componentContext) return
      const id = UtilSchema.getValueByKeyForContext(this.componentSchema.reference + '.item.id', this.componentContext)
      if (typeof id == 'number') return id
    },
    async doSaveItem(event: SaveItemEvent) {
      if (!this.componentSchema.reference || !this.componentContext) return
      const table = event.table || this.componentSchema.table
      if (!table) return
      const cardItem = UtilSchema.getValueByKeyForContext(this.componentSchema.reference, this.componentContext)
      if (cardItem == undefined) return
      if (typeof cardItem != 'object') return;
      const item = cardItem['item']
      const _item = cardItem['_item']

      if (item && typeof item == 'object') {
        this.loading = true
        let id = item['id']
        try {
          if (!id) {
            id = (await EventDispatcher.onCreateItemEvent(item, table, this.componentContext)).id
          } else if (_item && typeof _item == 'object' && typeof id == 'number') {
            await EventDispatcher.onUpdateItemEvent(item, _item, id, table, this.componentContext)
          }
        } finally {
          if (typeof id == 'number') {
            await this.doLoadItem(table, id)
          }
          this.loading = false
        }
      }
    },
    doDeleteItem(event: DeleteItemEvent) {
      const id = this.getId()
      if (!this.componentSchema.table || !id) return
      const newEvent: RenderReferenceEvent = {
        eventType: 'render-reference',
        name: event.name,
        overlay: 'popup',
        inputSchema: {
          inputType: 'delete-item',
          table: this.componentSchema.table,
          id: id,
          closeReferenceAfter: true
        }
      }
      this.doEmitEventSchema(newEvent)
    },
    async approvedDeleteItem(_: ApprovedDeleteItemEvent) {
      if (this.inputSchema?.inputType != 'delete-item' || !this.componentContext) return
      try {
        this.loading = true
        await EventDispatcher.onDeleteItemEvent(this.inputSchema.table, this.inputSchema.id, this.componentContext)
      } catch (e) {
        alert('Exception on delete item')
      } finally {
        const newEvent: CloseReferencePopupEvent = {
          eventType: 'close-popup-reference',
        }
        this.doEmitEventSchema(newEvent)
        this.loading = false
      }
      if (this.inputSchema.closeReferenceAfter) {
        const newEvent: RenderReferenceEvent = {
          eventType: 'render-reference',
          name: '',
          overlay: 'close'
        }
        this.doEmitEventSchema(newEvent)
      }
    },
    doEmitEventSchema(event: EventSchema) {
      if (event.eventType == 'save-item') {
        this.doSaveItem(event)
      } else if (event.eventType == 'delete-item') {
        this.doDeleteItem(event)
      } else if (event.eventType == 'approved-delete-item') {
        this.approvedDeleteItem(event)
      } else {
        this.$emit('event-schema', event)
      }
    },
  },
  mounted() {
    this.doTriggerInput()
  },
  watch: {
    inputSchema: {
      handler() {
        this.doTriggerInput()
      },
      deep: true
    }
  }
})
</script>

<template>
  <VCard :title="componentSchema.title" :loading="loading">
    <VCardText v-if="!loading">
      <GroupBuilder
          v-for="component in componentSchema.components"
          :component-schema="component"
          :component-context="componentContext"
          :input-schema="inputSchema"
          @event-schema="doEmitEventSchema"
      />
    </VCardText>
  </VCard>
</template>

<style scoped>

</style>