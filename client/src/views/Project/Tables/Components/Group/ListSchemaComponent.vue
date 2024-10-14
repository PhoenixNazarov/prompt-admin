<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {ChangeContextEvent, ListRowClickEvent, ListSchema, RenderReferenceEvent} from "../../types";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import GroupSchemaMixin from "../Mixins/GroupSchemaMixin.ts";
import {useTableStore} from "../../../../../stores/project/tables/table.store.ts";
import ListSchemaToolbarElement from "./ListSchemaToolbarElement.vue";

type SortItem = {
  key: string;
  order?: boolean | 'asc' | 'desc';
}


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

    const startLastSearch = {
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
      sortBy: [{key: 'id', order: 'desc'}] as SortItem[],
      page: 1,
      itemsPerPage: this.componentSchema.itemsPerPage ? this.componentSchema.itemsPerPage : 10,
    }
    if (this.inputSchema?.inputType == 'parameters-list') {
      if (this.inputSchema.page) startLastSearch.page = this.inputSchema.page
      if (this.inputSchema.itemsPerPage) startLastSearch.itemsPerPage = this.inputSchema.itemsPerPage
      if (this.inputSchema.sortBy && this.inputSchema.sortBy.length > 0) startLastSearch.sortBy = this.inputSchema.sortBy as SortItem[]
      if (this.inputSchema.additionalHeaders && this.inputSchema.additionalHeaders.length > 0) startLastSearch.additionalHeaders = this.inputSchema.additionalHeaders
      if (this.inputSchema.filters && this.inputSchema.filters.length > 0) startLastSearch.filters = this.inputSchema.filters
    }

    return {
      headers: actionHeader,
      items: [] as any[],
      count: 0,
      loading: {
        data: false,
        count: false
      },

      _lastSearch: {
        filters: [] as { key?: string, value?: string | number | boolean, operator?: string }[],
        additionalHeaders: [] as { title: string, key: string, sortable: boolean }[],
        sortBy: [] as { key: string, order: 'ask' | 'desc' }[],
        page: 1,
        itemsPerPage: this.componentSchema.itemsPerPage ? this.componentSchema.itemsPerPage : 10,
      },

      lastSearch: startLastSearch,

      columns: undefined as undefined | { column_name: string, data_type: string }[],
      exit: false
    }
  },
  methods: {
    updateOptions({sortBy}: { sortBy: SortItem[] }) {
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

      this.loadCount()
      this.loading.data = true
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
        this.loading.data = false
      }
    },
    async loadCount() {
      if (this.componentSchema.hideBottom) return
      this.loading.count = true
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
        this.loading.count = false
      }
    },
    async fetchColumns() {
      this.columns = await this.tableStore.fetchColumns(this.PROJECT, this.componentSchema.table)
    },
    getColumns(base: any = undefined) {
      return (base || this._lastSearch.additionalHeaders).map((i: any) => {
        const columnDb = this.componentSchema.columns.find(el => {
          return el.title == i.title
        })
        if (columnDb?.columnDbms) {
          return columnDb?.columnDbms
        }
        return i.key
      })
    },
    getFilters(base: any = undefined) {
      return (base || this._lastSearch.filters).filter((el: any) => el.key && el.operator) as {
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
        const eventRow = row.columns.map((el: any) => {
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
    },
  },
  watch: {
    componentContext: {
      handler() {
        if (this.componentSchema.filter) {
          this.initStartFilter()
        }
      },
      deep: true
    },
    _lastSearch: {
      handler() {
        if (this.inputSchema?.inputType == 'parameters-list') {
          this.inputSchema.page = this._lastSearch.page
          this.inputSchema.itemsPerPage = this._lastSearch.itemsPerPage
          this.inputSchema.sortBy = this._lastSearch.sortBy
          this.inputSchema.filters = this._lastSearch.filters
          this.inputSchema.additionalHeaders = this._lastSearch.additionalHeaders
        }
      },
      deep: true
    }
  },
  mounted() {
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
      v-model:sort-by="lastSearch.sortBy"
      :headers="[...lastSearch.additionalHeaders, ...headers]"
      item-value="id"
      :items="items"
      :items-length="count"
      :loading="loading.count || loading.data"
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
      v-model:sort-by="lastSearch.sortBy"
      :headers="[...lastSearch.additionalHeaders, ...headers]"
      item-value="id"
      :items="items"
      :items-length="count"
      :loading="loading.count || loading.data"
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