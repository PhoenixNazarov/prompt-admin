<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {ChangeContextEvent, ListRowClickEvent, ListSchema, RenderReferenceEvent} from "../../types";
import UtilSchema from "../UtilSchema.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import GroupSchemaMixin from "../Mixins/GroupSchemaMixin.ts";
import {useTableStore} from "../../../../../stores/project/tables/table.store.ts";

export default defineComponent({
  name: "ListSchemaComponent",
  mixins: [GroupSchemaMixin],
  components: {FontAwesomeIcon},
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
      headers: [
        ...this.componentSchema.columns.map(el => {
          return {
            title: el.title,
            key: el.column,
            sortable: true
          }
        }),
        ...actionHeader
      ],
      items: [] as any[],
      count: 0,
      loading: false,
      page: 1,
      test: 'name',
      itemsPerPage: this.componentSchema.itemsPerPage ? this.componentSchema.itemsPerPage : 10,

      searchField: this.componentSchema.filter?.columns[0].key,
      searchFieldKeys: this.componentSchema.filter?.columns.map(el => el.key),
      startSearch: this.componentSchema.filter?.startValue ? this.doRenderContextText(this.componentSchema.filter?.startValue) : undefined,
      search: this.componentSchema.filter?.startValue ? this.doRenderContextText(this.componentSchema.filter?.startValue) : undefined,
      searchNull: !(this.componentSchema.filter?.startValue != null && this.componentSchema.filter.hideFilterField)
    }
  },
  methods: {
    async loadData({sortBy}: { sortBy: { key: string, order: 'ask' | 'desc' }[] }) {
      this.loading = true
      this.loadCount()
      try {
        const project = UtilSchema.getProject(this.componentContext)
        this.items = await this.tableStore.listLoad(
            project as string,
            this.componentSchema.table,
            this.componentSchema.columns.map(i => i.column),
            this.page,
            this.itemsPerPage,
            sortBy,
            this.searchNull && !this.search ? undefined : {
              key: this.searchField,
              value: this.search == '' ? undefined : this.search,
              like: this.componentSchema.filter?.columns.find(el => el.key == this.searchField)?.like
            }
        )
      } finally {
        this.loading = false
      }
    },
    async loadCount() {
      if (this.componentSchema.hideBottom) return
      this.loading = true
      try {
        const project = UtilSchema.getProject(this.componentContext)
        const response = await this.tableStore.listCount(
            project as string,
            this.componentSchema.table,
            this.componentSchema.columns.map(i => i.column),
            this.searchNull && !this.search ? undefined : {
              key: this.searchField,
              value: this.search == '' ? undefined : this.search,
              like: this.componentSchema.filter?.columns.find(el => el.key == this.searchField)?.like
            }
        )
        this.count = response.count
      } finally {
        this.loading = false
      }
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
          const newStartSearch = this.componentSchema.filter?.startValue ? this.doRenderContextText(this.componentSchema.filter?.startValue) : undefined
          if (newStartSearch != this.startSearch) {
            this.startSearch = newStartSearch
            this.search = newStartSearch
            this.loadData({sortBy: []})
          }
        }
      },
      deep: true
    }
  }
})
</script>

<template>
  <VDataTableServer
      v-if="inputSchema?.inputType == 'select' || inputSchema?.inputType == 'list-row-click'"
      v-model:page="page"
      v-model:items-per-page="itemsPerPage"
      :headers="headers"
      item-value="id"
      :items="items"
      :items-length="count"
      :loading="loading"
      :search="search"
      @update:options="loadData"
      @click:row="doClickRow"
      density="compact"
      :class="{
        'table-border': componentSchema.border
      }"
  >
    <template v-slot:top>
      <VToolbar
          flat
          color="transparent"
          density="compact"
          :title="componentSchema.title"
      />
      <VRow v-if="componentSchema.filter && !componentSchema.filter.hideFilterField">
        <VCol sm="2">
          <VSelect v-model="searchField" density="compact" :items="searchFieldKeys"/>
        </VCol>
        <VCol>
          <VTextField
              v-model="search"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              hide-details
              single-line
          />
        </VCol>
      </VRow>
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
  </VDataTableServer>

  <VDataTableServer
      v-else
      v-model:page="page"
      v-model:items-per-page="itemsPerPage"
      :headers="headers"
      item-value="id"
      :items="items"
      :items-length="count"
      :loading="loading"
      @update:options="loadData"
      :search="search"
      density="compact"
      :class="{
        'table-border': componentSchema.border
      }"
  >
    <template v-slot:top>
      <VToolbar
          flat
          color="transparent"
          density="compact"
          :title="componentSchema.title"
      >
        <VBtn
            v-if="componentSchema.createElementName"
            variant="outlined"
            text="New Item"
            @click.prevent="doNewElement"
        />
      </VToolbar>
      <VRow v-if="componentSchema.filter && !componentSchema.filter.hideFilterField">
        <VCol sm="2">
          <VSelect v-model="searchField" density="compact" :items="searchFieldKeys"/>
        </VCol>
        <VCol>
          <VTextField
              v-model="search"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              hide-details
              single-line
          />
        </VCol>
      </VRow>

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