<script lang="ts">
import {defineComponent, PropType} from 'vue'
import ElementSchemaMixins from "../Mixins/DataElementSchemaMixin.ts";
import {ItemRowSchema} from "../../types";
import {useTableStore} from "../../../../../stores/project/tables/table.store.ts";

export default defineComponent({
  name: "ItemRowSchemaComponent",
  mixins: [ElementSchemaMixins],
  props: {
    componentSchema: {
      type: Object as PropType<ItemRowSchema>,
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
    return {
      headers: this.componentSchema.columns.map(el => {
        return {
          title: el.title,
          value: el.column
        }
      }),
      items: [] as any[],
      loading: false,
      selfModel: this.doRenderReference(this.componentSchema.reference)
    }
  },
  methods: {
    async doLoadItem(table: string, id: number) {
      try {
        this.loading = true
        this.items = [await this.tableStore.loadItem(this.PROJECT, table, id)]
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    this.doLoadItem(this.componentSchema.table, this.model as number)
  },
  watch: {
    componentContext: {
      handler() {
        const newModel = this.doRenderReference(this.componentSchema.reference)
        if (newModel != this.selfModel) {
          this.doLoadItem(this.componentSchema.table, newModel as number)
          this.selfModel = newModel
        }
      },
      deep: true
    }
  }
})
</script>

<template>
  <h4 v-if="componentSchema.label" style="margin-left: 0.5rem;">
    {{ componentSchema.label }}
  </h4>
  <VDataTable
      :headers="headers"
      :items="items"
      :loading="loading"
      density="compact"
      class="table"
  >
    <template #top>
    </template>
    <template #bottom></template>
  </VDataTable>
</template>

<style scoped>
.table {
  border-radius: 0.5rem;
  border: solid 1px #ababab;
}
</style>