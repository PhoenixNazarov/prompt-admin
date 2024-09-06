<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt} from "../../../stores/prompt.store.ts";
import {PromptAudit, usePromptAuditStore} from "../../../stores/config/promptAudit.store.ts";
import {useAccountStore} from "../../../stores/user.store.ts";
import {dateTimeFormat} from "../../Utils.ts";

export default defineComponent({
  name: "ChangesHistory",
  props: {
    prompt: {
      type: Object as PropType<Prompt>
    }
  },
  setup() {
    const promptAuditStore = usePromptAuditStore()
    const accountStore = useAccountStore()
    return {
      promptAuditStore,
      accountStore
    }
  },
  data() {
    return {
      headers: [
        {title: 'Date', key: 'time_create', sortable: false},
        {title: 'Account', key: 'account_id', sortable: false}
      ],
      loading: true,
      itemsPerPage: 5,
      page: 1
    }
  },
  methods: {
    dateFormat: dateTimeFormat,
    changes(): PromptAudit[] | undefined {
      if (this.prompt) return this.promptAuditStore.getByPrompt(this.prompt)
    },
    async loadItems({page, itemsPerPage}: {
      page: number
      itemsPerPage: number
      sortBy?: { key: string; order: 'desc' | 'ask' }[]
    }) {
      if (!this.prompt) return
      this.loading = true
      await this.promptAuditStore.loadForPrompt(this.prompt, itemsPerPage, page - 1)
      this.loading = false
    },
    previewPromptAudit(_: any, row: any) {
      const promptAudit = row.item
      if (!this.prompt) return
      const changes = this.changes()
      const prevPromptAudit = changes ? changes[row.index + 1] : undefined
      const prompt: Prompt = {
        mapping_id: this.prompt.mapping_id,
        table: this.prompt.table,
        field: this.prompt.field,
        id: this.prompt.id,
        value: this.prompt.value,
        name: this.prompt.name,
        auditData: {
          audit: promptAudit,
          prevAudit: prevPromptAudit
        }
      }
      this.$emit('preview', prompt)
    },
    getItems() {
      if (!this.prompt) return []
      const items = this.promptAuditStore.getByPrompt(this.prompt)
      if (!items) return []
      return items.slice(this.itemsPerPage * (this.page - 1), this.itemsPerPage * (this.page))
    },
    getItemCount() {
      if (!this.prompt) return 0
      const count = this.promptAuditStore.getByPromptCount(this.prompt)
      if (!count) return 0
      return count
    }
  },
  watch: {
    async prompt() {
      await this.loadItems({page: this.page, itemsPerPage: this.itemsPerPage})
    }
  }
})
</script>

<template>
  <div>
    <VDataTableServer
        v-model:items-per-page="itemsPerPage"
        v-model:page="page"
        :headers="headers"
        :items="getItems()"
        :items-length="getItemCount()"
        :loading="loading"
        item-value="id"
        @update:options="loadItems"
        density="compact"
        @click:row="previewPromptAudit"
    >
      <template v-slot:[`item.time_create`]="{ item }">
        {{ dateTimeFormat(new Date(item.time_create)) }}
      </template>
      <template v-slot:[`item.account_id`]="{ item }">
        {{ accountStore.getLoginById(item.account_id) }}
      </template>
    </VDataTableServer>
  </div>

</template>

<style scoped>
.v-table {
  background: unset;
}
</style>