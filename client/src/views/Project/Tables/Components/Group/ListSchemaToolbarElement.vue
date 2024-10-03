<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {ListSchema} from "../../types";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

export default defineComponent({
  name: "ListSchemaToolbarElement",
  components: {FontAwesomeIcon},
  props: {
    componentSchema: {
      type: Object as PropType<ListSchema>,
      required: true
    },
    additionalHeaders: {
      type: Object as PropType<{ title: string, key: string, sortable?: boolean }[]>,
      required: true
    },
    columns: {
      type: Object as PropType<{ column_name: string, data_type: string }[]>,
    },
    filters: {
      type: Object as PropType<{ key?: string, value?: string | number | boolean, operator?: string }[]>,
      required: true
    }
  },
  emits: [
    'doNewElement',
    'doRemoveAdditionalHeader',
    'doAddAdditionalHeader',
    'doRemoveFilter',
    'doAddFilter'
  ]
})
</script>

<template>
  <VToolbar
      flat
      color="transparent"
      density="compact"
      :title="componentSchema.title"
      style="{z-index: 0}"
  >
    <VBtn
        v-if="componentSchema.createElementName"
        variant="outlined"
        text="New Item"
        @click.prevent="$emit('doNewElement')"
    />
  </VToolbar>
  <VExpansionPanels v-if="!componentSchema.filter?.hideFilterField" >
    <VExpansionPanel title="Filters">
      <VExpansionPanelText>
        <VRow v-for="(filter, i) in filters">
          <VCol sm="2">
            <VSelect v-model="filter.key" density="compact" :items="columns?.map(e => e.column_name)" hide-details/>
          </VCol>
          <VCol sm="2">
            <VSelect
                v-model="filter.operator"
                v-if="columns?.find(el => el.column_name == filter.key)?.data_type == 'integer'"
                density="compact"
                :items="['=', '>', '>=', '<', '<=', '!=', 'is']"
                hide-details
            />
            <VSelect
                v-model="filter.operator"
                v-else
                density="compact"
                :items="['=', '!=', 'like', '%like', 'like%', '%like%', 'is']"
                hide-details
            />
          </VCol>
          <VCol>
            <VTextField
                v-model="filter.value"
                label="Search"
                type=""
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="compact"
                hide-details
                single-line
            />
          </VCol>
          <VCol sm="1" class="center">
            <FontAwesomeIcon class="pointer ml-2" icon="fa-trash"
                             @click.prevent="$emit('doRemoveFilter', i)"/>
          </VCol>
        </VRow>
        <VBtn class="ma-5" @click.prevent="$emit('doAddFilter')" density="compact">Add filter</VBtn>
      </VExpansionPanelText>
    </VExpansionPanel>
    <VExpansionPanel title="Headers">
      <VExpansionPanelText>
        <VContainer>
          <VRow
              align="center"
              justify="start"
              class="mb-4"
          >
            <VCol
                v-for="(selection, i) in additionalHeaders"
                :key="selection.title"
                class="py-1 pe-0"
                cols="auto"
            >
              <VChip
                  closable
                  @click:close="$emit('doRemoveAdditionalHeader', i)"
              >
                {{ selection.title }}
              </VChip>
            </VCol>
          </VRow>
          <VDivider/>
          <VList density="compact" v-if="additionalHeaders">
            <template v-for="item in columns">
              <VListItem
                  v-if="!additionalHeaders.map(el => el.key).includes(item.column_name)"
                  :key="item.column_name"
                  @click="$emit('doAddAdditionalHeader', item.column_name)"
              >
                <v-list-item-title v-text="item.column_name"/>
              </VListItem>
            </template>
          </VList>
        </VContainer>
      </VExpansionPanelText>
    </VExpansionPanel>
  </VExpansionPanels>
</template>

<style scoped>
.center {
  display: flex;
  align-items: center;
}

.v-expansion-panels {
  z-index: 0
}
</style>