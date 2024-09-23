<script lang="ts">
import {defineComponent} from 'vue'
import ProjectMainView from "../ProjectMainLayout.vue";
import {useTableStore} from "../../../stores/project/tables/table.store.ts";

export default defineComponent({
  name: "EditTableView",
  components: {ProjectMainView},
  props: {
    project: {
      type: String,
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
      loading: false
    }
  },
  methods: {
    async downloadFile() {
      this.loading = true
      try {
        const result = await this.tableStore.loadSchema(this.project)
        if (!result || !result.table_schema) return
        const blob = new Blob([JSON.stringify(result.table_schema)], { type: 'application/json' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = `${this.project}_schema.json`
        link.click()
        URL.revokeObjectURL(link.href)
      } finally {
        this.loading = false
      }
    },
    uploadFile(files: File | File[]) {
      const file = files instanceof Array ? files[0] : files
      const reader = new FileReader();
      reader.readAsText(file)
      reader.onload = async () => {
        if (typeof reader?.result == 'string') {
          const json = JSON.parse(reader?.result)
          try {
            this.loading = true
            await this.tableStore.uploadSchema(this.project, json)
          } finally {
            this.loading = false
          }
        }
      }
    }
  }
})
</script>

<template>
  <ProjectMainView :project="project">
    <VCard title="Edit Tables Schema" :loading="loading">
      <VCardText v-if="!loading">
        <VRow>
          <VCol>
            <VBtn block text="Download current schema" variant="outlined" @click.prevent="downloadFile"/>
          </VCol>
        </VRow>
        <VRow>
          <VCol>
            <VFileInput label="Upload Schema" variant="outlined" @update:model-value="uploadFile"></VFileInput>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>
  </ProjectMainView>
</template>

<style scoped>

</style>