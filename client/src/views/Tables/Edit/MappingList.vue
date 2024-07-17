<script lang="ts">
import {defineComponent} from 'vue'
import {useMappingStore} from "../../../stores/config/mapping.store.ts";
import {cropText} from "../../Utils.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import TableLayout from "./Components/TableLayout.vue";
import {RouterService} from "../../../plugins/router.ts";
import RemoveButton from "./Components/RemoveButton.vue";

export default defineComponent({
  name: "MappingList",
  computed: {
    RouterService() {
      return RouterService
    }
  },
  components: {RemoveButton, TableLayout, FontAwesomeIcon},
  methods: {cropText},
  setup() {
    const mappingStore = useMappingStore()
    return {
      mappingStore
    }
  },
  data() {
    return {
      headers: [
        {title: 'Connection', key: 'connection_name'},
        {title: 'Name', value: "name"},
        {title: 'Action', value: 'action'}
      ],
    }
  }
})
</script>

<template>
  <VDataTable
      :headers="headers"
      :items="mappingStore.entity"
      density="compact"
      variant="outlined"
      :loading="mappingStore.loadings.loadAll"
  >
    <template v-slot:top>
      <VToolbar
          flat
          color="transparent"
          density="compact"
      >
        <VToolbarTitle>MAPPINGS</VToolbarTitle>
        <VBtn
            variant="outlined"
            dark
            text="New Item"
            @click.prevent="RouterService.goToTableItem('mapping')"
        />
      </VToolbar>
    </template>
    <template v-slot:loading>
      <VSkeletonLoader type="table-row@5"></VSkeletonLoader>
    </template>
    <template v-slot:item.name="{ item }">
      <b>{{ item.table }}.{{ item.field }}</b> {{ cropText(item.description) }}
    </template>
    <template v-slot:item.action="{ item }">
      <FontAwesomeIcon class="pointer" style="margin-right: 0.5rem" icon="fa-pen"
                       @click.prevent="RouterService.goToTableItem('mapping', item.id)"/>
      <RemoveButton variant="icon" :text="`${item.table}.${item.field} ${cropText(item.description)}`"
                    :remove="() => mappingStore.remove(item.id)"/>
    </template>
  </VDataTable>
</template>

<style scoped>

</style>