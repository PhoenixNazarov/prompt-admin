<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {RouterService} from "../../../plugins/router.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {cropText} from "../../Utils.ts";
import {Macro, useMacroStore} from "../../../stores/config/macro.store.ts";
import RemoveButton from "./Components/RemoveButton.vue";

export default defineComponent({
  name: "MacroList",
  methods: {cropText},
  components: {RemoveButton, FontAwesomeIcon},
  computed: {
    RouterService() {
      return RouterService
    }
  },
  setup() {
    const macroStore = useMacroStore()
    return {
      macroStore
    }
  },
  props: {
    macros: {
      type: Object as PropType<Macro[]>
    },
    tableName: {
      type: String,
      default: 'MACROS'
    },
    create: {
      tpe: Boolean,
      default: true
    }
  },
  data() {
    return {
      headers: [
        {title: 'Id', key: 'id'},
        {title: 'Macro', key: 'macro'},
        {title: 'Macro Value', key: 'macro_value'},
        {title: 'Action', value: 'action'}
      ],
    }
  }
})
</script>

<template>
  <VDataTable
      :headers="headers"
      :items="macros ? macros : macroStore.entity"
      density="compact"
      variant="outlined"
      :loading="macroStore.loadings.loadAll"
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
            @click.prevent="RouterService.goToTableItem('macro')"
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
    <template v-slot:item.description="{ item }">
      {{ cropText(item.description) }}
    </template>
    <template v-slot:item.macro_value="{ item }">
      {{ cropText(item.macro_value) }}
    </template>
    <template v-slot:item.action="{ item }">
      <FontAwesomeIcon class="pointer" style="margin-right: 0.5rem" icon="fa-pen"
                       @click.prevent="RouterService.goToTableItem('macro', item.id)"/>
      <RemoveButton variant="icon" :text="cropText(item.macro_value)"
                    :remove="() => macroStore.remove(item.id)"/>
    </template>
  </VDataTable>
</template>

<style scoped>

</style>