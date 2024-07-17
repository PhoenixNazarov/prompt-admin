<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Output, useOutputStore} from "../../../stores/config/output.store.ts";
import {cropText} from "../../Utils.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import OutputItem from "./OutputItem.vue";
import {RouterService} from "../../../plugins/router.ts";
import RemoveButton from "./Components/RemoveButton.vue";

export default defineComponent({
  name: "OutputList",
  computed: {
    RouterService() {
      return RouterService
    }
  },
  props: {
    outputs: {
      type: Object as PropType<Output[]>
    },
    tableName: {
      type: String,
      default: 'OUTPUTS'
    },
    create: {
      tpe: Boolean,
      default: true
    }
  },
  methods: {
    cropText
  },
  components: {RemoveButton, OutputItem, FontAwesomeIcon},
  setup() {
    const outputsStore = useOutputStore()
    return {
      outputsStore
    }
  },
  data() {
    return {
      headers: [
        {title: 'Id', key: 'id'},
        {title: 'Output', key: 'output'},
        {title: 'Action', value: 'action'}
      ],
    }
  }
})
</script>

<template>
  <VDataTable
      :headers="headers"
      :items="outputs ? outputs : outputsStore.entity"
      density="compact"
      variant="outlined"
      :loading="outputsStore.loadings.loadAll"
      @click:row="(event, row) => $emit('clickRow', row.item)"
  >
    <template v-slot:top>
      <VToolbar
          flat
          color="transparent"
          density="compact"
      >
        <VToolbarTitle>{{ tableName }}</VToolbarTitle>
        <VBtn
            v-if="create"
            variant="outlined"
            dark
            text="New Item"
            @click.prevent="RouterService.goToTableItem('output')"
        />
      </VToolbar>
    </template>
    <template v-slot:loading>
      <VSkeletonLoader type="table-row"></VSkeletonLoader>
    </template>
    <template v-slot:item.data-table-select="{ internalItem, isSelected, toggleSelect }">
      <VCheckboxBtn
          :model-value="isSelected(internalItem)"
          color="primary"
          @update:model-value="toggleSelect(internalItem)"
      ></VCheckboxBtn>
    </template>
    <template v-slot:item.output="{ item }">
      {{ cropText(item.output) }}
    </template>
    <template v-slot:item.action="{ item }">
      <FontAwesomeIcon class="pointer" style="margin-right: 0.5rem" icon="fa-pen"
                       @click.prevent="RouterService.goToTableItem('output', item.id)"/>
      <RemoveButton variant="icon" :text="item.output" :remove="() => outputsStore.remove(item.id)"/>
    </template>
  </VDataTable>
</template>

<style scoped>

</style>