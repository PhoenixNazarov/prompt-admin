<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {MappingEntity, useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {RouterService} from "../../../plugins/router.ts";
import RemoveButton from "./Components/RemoveButton.vue";

export default defineComponent({
  name: "MappingEntityList",
  computed: {
    RouterService() {
      return RouterService
    }
  },
  props: {
    mappingsEntity: {
      type: Object as PropType<MappingEntity[]>
    },
    tableName: {
      type: String,
      default: 'MAPPINGS ENTITY'
    },
    create: {
      tpe: Boolean,
      default: true
    }
  },
  components: {RemoveButton, FontAwesomeIcon},
  setup() {
    const mappingEntityStore = useMappingEntityStore()
    return {
      mappingEntityStore
    }
  },
  data() {
    return {
      headers: [
        {title: 'Filter', value: 'ident'},
        {title: 'Type', value: 'entity'},
        {title: 'Action', value: 'action'}
      ]
    }
  },
  methods: {
    name(item: MappingEntity) {
      return `${item.mapping_id || ''} ${
          item.connection_name || '*'
      }.${item.table || '*'}.${item.field || '*'}.${item.name || '*'}`
    }
  }
})
</script>

<template>
  <VDataTable
      :headers="headers"
      :items="mappingsEntity ? mappingsEntity : mappingEntityStore.entity"
      density="compact"
      variant="outlined"
      :loading="mappingEntityStore.loadings.loadAll"
  >
    <template v-slot:top>
      <VToolbar
          flat
          color="transparent"
          density="compact"
      >
        <VToolbarTitle>{{ tableName }}</VToolbarTitle>
        <VBtn
            variant="outlined"
            dark
            v-if="create"
            text="New item"
            @click.prevent="RouterService.goToTableItem('mapping-entity')"
        />
      </VToolbar>
    </template>
    <template v-slot:loading>
      <VSkeletonLoader type="table-row@5"></VSkeletonLoader>
    </template>
    <template v-slot:item.ident="{ item }">
      {{ name(item) }}
    </template>
    <template v-slot:item.action="{ item }">
      <FontAwesomeIcon class="pointer" style="margin-right: 0.5rem" icon="fa-pen"
                       @click.prevent="RouterService.goToTableItem('mapping-entity', item.id)"/>
      <RemoveButton variant="icon" :text="name(item)"
                    :remove="() => mappingEntityStore.remove(item.id)"/>
    </template>
  </VDataTable>
</template>

<style scoped>

</style>