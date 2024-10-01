<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {ChangeContextEvent, ListRowClickEvent, ListSchema, RenderReferenceEvent} from "../../types";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import GroupSchemaMixin from "../Mixins/GroupSchemaMixin.ts";
import {useTableStore} from "../../../../../stores/project/tables/table.store.ts";
import ListSchemaToolbarElement from "./ListSchemaToolbarElement.vue";

export default defineComponent({
  name: "ListSchemaComponent",
  mixins: [GroupSchemaMixin],
  components: {ListSchemaToolbarElement, FontAwesomeIcon},
  props: {
    componentSchema: {
      type: Object as PropType<ListSchema>,
      required: true
    }
  },
  setup() {
    const tableStore = useTableStore()
    return {
      tableStore
    }
  },
  data() {
    const actionHeader = []
    if (this.componentSchema.editElementName) {
      actionHeader.push({
        title: 'actions',
        value: 'actions',
        sortable: false
      })
    }
    return {
      headers: actionHeader,
      items: [] as any[],
      count: 0,
      loading: false,

      _lastSearch: {
        filters: [] as { key?: string, value?: string | number | boolean, operator?: string }[],
        additionalHeaders: [] as { title: string, key: string, sortable: boolean }[],
        sortBy: [] as { key: string, order: 'ask' | 'desc' }[],
        page: 1,
        itemsPerPage: this.componentSchema.itemsPerPage ? this.componentSchema.itemsPerPage : 10,
      },

      lastSearch: {
        filters: [] as {
          key?: string,
          value?: string | number | boolean,
          operator?: string
        }[],
        additionalHeaders: this.componentSchema.columns.filter(el => el.display != 'none').map(el => {
          return {
            title: el.title,
            key: el.column,
            sortable: true
          }
        }),
        sortBy: [] as { key: string, order: 'ask' | 'desc' }[],
        page: 1,
        itemsPerPage: this.componentSchema.itemsPerPage ? this.componentSchema.itemsPerPage : 10,
      },

      columns: undefined as undefined | { column_name: string, data_type: string }[],
      exit: false
    }
  },
  methods: {
    updateOptions({sortBy}: { sortBy: { key: string, order: 'ask' | 'desc' }[] }) {
      this.lastSearch.sortBy = sortBy
      this.loadData()
    },
    loadDataWatcher() {
      if (!this.exit) {
        setTimeout(this.loadDataWatcher, 1000)
        this.loadData()
      }
    },
    initStartFilter() {
      if (this.componentSchema.filter?.startFilters) {
        this.lastSearch.filters = this.componentSchema.filter?.startFilters.map(el => {
          return {...el, value: this.doRenderContextText(String(el.value))}
        })
      }
    },
    async loadData() {
      if (
          JSON.stringify(this.getFilters(this.lastSearch.filters)) == JSON.stringify(this.getFilters(this._lastSearch.filters)) &&
          JSON.stringify(this.lastSearch.additionalHeaders) == JSON.stringify(this._lastSearch.additionalHeaders) &&
          JSON.stringify(this.lastSearch.sortBy) == JSON.stringify(this._lastSearch.sortBy) &&
          this.lastSearch.page == this._lastSearch.page &&
          this.lastSearch.itemsPerPage == this._lastSearch.itemsPerPage
      ) {
        return
      }

      this._lastSearch.filters = JSON.parse(JSON.stringify(this.lastSearch.filters))
      this._lastSearch.additionalHeaders = JSON.parse(JSON.stringify(this.lastSearch.additionalHeaders))
      this._lastSearch.sortBy = JSON.parse(JSON.stringify(this.lastSearch.sortBy))
      this._lastSearch.page = this.lastSearch.page
      this._lastSearch.itemsPerPage = this.lastSearch.itemsPerPage

      this.loading = true
      this.loadCount()
      try {
        this.items = await this.tableStore.listLoad(
            this.PROJECT,
            this.componentSchema.table,
            this.getColumns(),
            this._lastSearch.page,
            this._lastSearch.itemsPerPage,
            this._lastSearch.sortBy,
            this.getFilters(),
            this.componentSchema.joins
        )
      } finally {
        this.loading = false
      }
    },
    async loadCount() {
      if (this.componentSchema.hideBottom) return
      this.loading = true
      try {
        const response = await this.tableStore.listCount(
            this.PROJECT,
            this.componentSchema.table,
            this.getColumns(),
            this.getFilters(),
            this.componentSchema.joins
        )
        this.count = response.count
      } finally {
        this.loading = false
      }
    },
    async fetchColumns() {
      this.columns = await this.tableStore.fetchColumns(this.PROJECT, this.componentSchema.table)
    },
    getColumns(base: any = undefined) {
      return (base || this._lastSearch.additionalHeaders).map(i => {
        const columnDb = this.componentSchema.columns.find(el => {
          return el.title == i.title
        })
        console.log(columnDb, i)
        if (columnDb?.columnDbms) {
          return columnDb?.columnDbms
        }
        return i.key
      })
    },
    getFilters(base: any = undefined) {
      return (base || this._lastSearch.filters).filter(el => el.key && el.operator) as {
        key: string,
        value?: string | number | boolean | undefined,
        operator: string
      }[]
    },
    doEditElement(id: number) {
      if (this.componentSchema.editElementName) {
        const event: RenderReferenceEvent = {
          eventType: 'render-reference',
          name: this.componentSchema.editElementName,
          overlay: 'overlapping',
          inputSchema: {
            inputType: 'item',
            table: this.componentSchema.table,
            id: id
          }
        }
        this.doEmitEventSchema(event)
      }
    },
    doDeleteElement(id: number) {
      if (this.componentSchema.deleteElementName) {
        const event: RenderReferenceEvent = {
          eventType: 'render-reference',
          name: this.componentSchema.deleteElementName,
          overlay: 'popup',
          inputSchema: {
            inputType: 'delete-item',
            table: this.componentSchema.table,
            id: id,
            closeReferenceAfter: true
          }
        }
        this.doEmitEventSchema(event)
      }
    },
    doIdentCard(id: number, name: string, table: string | undefined) {
      const event: RenderReferenceEvent = {
        eventType: 'render-reference',
        name: name,
        overlay: 'overlapping',
        inputSchema: {
          inputType: 'item',
          table: table,
          id: id
        }
      }
      this.doEmitEventSchema(event)
    },
    doNewElement() {
      if (this.componentSchema.createElementName) {
        const event: RenderReferenceEvent = {
          eventType: 'render-reference',
          name: this.componentSchema.createElementName,
          overlay: 'overlapping',
          inputSchema: {
            inputType: 'create-item'
          }
        }
        this.doEmitEventSchema(event)
      }
    },
    doClickRow(_: any, row: any) {
      if (this.inputSchema?.inputType == 'list-row-click') {
        const eventRow = row.columns.map(el => {
          return {
            column: {
              title: el.title,
              column: el.key
            },
            value: row.internalItem.columns[el.key]
          }
        })
        const event: ListRowClickEvent = {
          eventType: 'list-row-click',
          row: eventRow
        }
        this.doEmitEventSchema(event)
      }
      if (this.inputSchema?.inputType == 'select') {
        if (this.inputSchema.targetColumn?.column) {
          const event: ChangeContextEvent = {
            eventType: 'change-context',
            contextKey: this.inputSchema.reference,
            value: row.item[this.inputSchema.targetColumn.column]
          }
          this.doEmitEventSchema(event)
          this.doEmitEventSchema({eventType: 'close-popup-reference'})
        }
      }
    }
  },
  watch: {
    componentContext: {
      handler() {
        if (this.componentSchema.filter) {
          this.initStartFilter()
        }
      },
      deep: true
    }
  },
  beforeMount() {
    this.initStartFilter()
    this.fetchColumns()
    this.loadDataWatcher()
  },
  unmounted() {
    this.exit = true
  },
})
</script>

<template>
  <VDataTableServer
      v-if="inputSchema?.inputType == 'select' || inputSchema?.inputType == 'list-row-click'"
      v-model:page="lastSearch.page"
      v-model:items-per-page="lastSearch.itemsPerPage"
      :headers="[...lastSearch.additionalHeaders, ...headers]"
      item-value="id"
      :items="items"
      :items-length="count"
      :loading="loading"
      @update:options="updateOptions"
      @click:row="doClickRow"
      density="compact"
      :class="{
        'table-border': componentSchema.border
      }"
  >
    <template v-slot:top>
      <ListSchemaToolbarElement
          :component-schema="componentSchema"
          :additional-headers="lastSearch.additionalHeaders"
          :columns="columns"
          :filters="lastSearch.filters"
          @doNewElement="doNewElement"
          @doAddAdditionalHeader="el => lastSearch.additionalHeaders.push({title: el, key: el, sortable: true})"
          @doRemoveAdditionalHeader="ind => lastSearch.additionalHeaders.splice(ind, 1)"
          @doAddFilter="lastSearch.filters.push({})"
          @doRemoveFilter="ind => lastSearch.filters.splice(ind, 1)"
      />
    </template>
    <template #bottom v-if="componentSchema.hideBottom"></template>
    <template v-slot:[`item.${column.column}`]="{ item }"
              v-for="column in componentSchema.columns.filter(el => el.ident)">
      <a
          href="#"
          @click.prevent="doIdentCard(item[column.column], column.ident.name, column.ident.table)"
          v-if="column.ident"
      >
        {{ item[column.column] }}
      </a>
    </template>
    <template v-slot:[`item.${column.column}`]="{ item }"
              v-for="column in componentSchema.columns.filter(el => el.display == 'image')">
      <img
          :src="'data:image/png;base64,'+ item[column.column]"
          :height="column.imageSize ? CONST_SCHEMA_COMPONENT.image_size[column.imageSize] : CONST_SCHEMA_COMPONENT.image_size_default"
      />
    </template>
  </VDataTableServer>

  <VDataTableServer
      v-else
      v-model:page="lastSearch.page"
      v-model:items-per-page="lastSearch.itemsPerPage"
      :headers="[...lastSearch.additionalHeaders, ...headers]"
      item-value="id"
      :items="items"
      :items-length="count"
      :loading="loading"
      @update:options="updateOptions"
      density="compact"
      :class="{
        'table-border': componentSchema.border
      }"
  >
    <template v-slot:top>
      <ListSchemaToolbarElement
          :component-schema="componentSchema"
          :additional-headers="lastSearch.additionalHeaders"
          :columns="columns"
          :filters="lastSearch.filters"
          @doNewElement="doNewElement"
          @doAddAdditionalHeader="el => lastSearch.additionalHeaders.push({title: el, key: el, sortable: true})"
          @doRemoveAdditionalHeader="ind => lastSearch.additionalHeaders.splice(ind, 1)"
          @doAddFilter="lastSearch.filters.push({})"
          @doRemoveFilter="ind => lastSearch.filters.splice(ind, 1)"
      />
    </template>
    <template #bottom v-if="componentSchema.hideBottom"></template>
    <template v-slot:[`item.${column.column}`]="{ item }"
              v-for="column in componentSchema.columns.filter(el => el.ident)">
      <a href="#" @click.prevent="doIdentCard(item[column.column], column.ident.name, column.ident.table)"
         v-if="column.ident">{{ item[column.column] }}</a>
    </template>
    <template v-slot:[`item.${column.column}`]="{ item }"
              v-for="column in componentSchema.columns.filter(el => el.display == 'image')">
      <img
          :src="'data:image/png;base64,'+ item[column.column]"
          :height="column.imageSize ? CONST_SCHEMA_COMPONENT.image_size[column.imageSize] : CONST_SCHEMA_COMPONENT.image_size_default"
      />
    </template>
    <template v-slot:item.actions="{ item }">
      <FontAwesomeIcon v-if="item.id && componentSchema.editElementName" class="pointer" icon="fa-pen"
                       @click.prevent="doEditElement(item.id)"/>
      <FontAwesomeIcon v-if="item.id && componentSchema.deleteElementName" class="pointer ml-2" icon="fa-trash"
                       @click.prevent="doDeleteElement(item.id)"/>
    </template>
  </VDataTableServer>
</template>

<style scoped>
table {
  background-color: red;
}

.table-border {
  border-radius: 0.5rem;
  border: solid 1px #ababab;
}
</style>