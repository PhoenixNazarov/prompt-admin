<script lang="ts">
import {defineComponent} from 'vue'
import {Prompt} from "../../../stores/prompt.store.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {useSettingsStore} from "../../../stores/config/settings.store.ts";
import PromptUnitTestStatus from "./PromptUnitTestStatus.vue";
import {ITEMS, ListItem, ListItemBuilder} from "./ListItemBuilder.ts";
import {useVarsStore} from "../../../stores/vars.store.ts";

export default defineComponent({
  name: "MenuPromptList",
  computed: {
    c() {
      return c
    }
  },
  components: {PromptUnitTestStatus, FontAwesomeIcon},
  props: {
    filter: {
      type: String
    }
  },
  setup() {
    const settingsStore = useSettingsStore()
    const varsStore = useVarsStore()
    return {
      settingsStore,
      varsStore
    }
  },
  data() {
    return {
      listItemBuilder: new ListItemBuilder(),
      items: ITEMS,

      createTemplate: {
        show: false,
        key: '',
        project: '',
        loading: false
      }
    }
  },
  methods: {
    isFilter(item: ListItem) {
      if (this.filter == '' || !this.filter) {
        return item.tags.some(el => !this.settingsStore.menuOpenedItems.includes(el))
      } else {
        if (item.type == 'prompt') {
          return item.name != undefined && !item.name.toLowerCase().includes(this.filter.toLowerCase())
        }
      }
    },
    onClick(item: ListItem) {
      if (item.type == 'group') {
        const tag = item.tag
        if (tag) {
          const index = this.settingsStore.menuOpenedItems.indexOf(tag)
          if (index > -1) {
            const oldMenuOpenedItems = [...this.settingsStore.menuOpenedItems]
            oldMenuOpenedItems.forEach(el => {
              if (el.startsWith(tag)) {
                const index2 = this.settingsStore.menuOpenedItems.indexOf(el)
                this.settingsStore.menuOpenedItems.splice(index2, 1)
              }
            })
          } else {
            this.settingsStore.menuOpenedItems.push(tag)
          }
        } else if (item.meta == 'template') {
          const selectPrompt: Prompt = {
            id: 0,
            field: "",
            table: "",
            value: item.metaData.value,
            originValue: item.metaData.value,
            mapping_id: -1,
            templateData: {
              key: item.metaData.key,
              project: item.metaData.project
            }
          }
          this.$emit('selectPrompt', selectPrompt)
        } else if (item.meta == 'create-template') {
          this.createTemplate.key = ''
          this.createTemplate.project = item.metaData.project
          this.createTemplate.show = true
        }
      } else if (item.type == 'prompt') {
        this.$emit('selectPrompt', item.prompt)
      }
    },
    async saveTemplate() {
      this.createTemplate.loading = true
      await this.varsStore.create(this.createTemplate.project, this.createTemplate.key, '', true)
      this.createTemplate.loading = false
      this.createTemplate.show = false
    },
  },
  mounted() {
    this.listItemBuilder.build()
  },
})
</script>

<template>
  <VDialog max-width="350px" v-model="createTemplate.show">
    <VContainer>
      <VCard>
        <VCardText>
          <VRow>
            <VTextField v-model="createTemplate.key" label="Key"/>
          </VRow>
          <VRow>
            <VBtn :loading="createTemplate.loading" class="mr-2" color="success" text="Save"
                  @click.prevent="saveTemplate"/>
          </VRow>
        </VCardText>
      </VCard>
    </VContainer>
  </VDialog>

  <VVirtualScroll :items="items" :renderless="true">
    <template v-slot:default="{ item }">
      <div
          class="main-button"
          :style="{'--tab': item.tab, '--filter-display': isFilter(item) ? 'none': ''}">
        <button @click.prevent="onClick(item)" class="button text-none">
          <FontAwesomeIcon
              v-if="item.type == 'group' && item.caret && item.tag && (filter == undefined || filter == '')"
              icon="angle-right"
              :style="{
                width: '1rem',
                marginRight: '0.2rem',
                transform: settingsStore.menuOpenedItems.includes(item.tag) ? 'rotate(90deg) scale(0.8)' : 'scale(0.8)',
              }"
          />
          <span v-else style="margin-right: 1.2rem"/>
          <FontAwesomeIcon v-if="item.type == 'group' && item.preIcon" :icon="item.preIcon" style="width: 1rem"/>
          <FontAwesomeIcon
              v-if="item.type == 'promise'"
              :spin="true"
              icon="spinner"
              style="width: 1rem"/>

          <PromptUnitTestStatus v-if="item.type=='prompt'" :prompt="item.prompt"
                                @selectPrompt="p => $emit('selectPrompt', p)"/>
          <span style="margin-left: 0.2rem">
            {{ item.name }}
          </span>
        </button>
      </div>
    </template>
  </VVirtualScroll>
</template>

<style scoped>
.main-button {
  --tab: 0;
  --filter-display: '';

  display: var(--filter-display);
  color: var(--color-5);
  font-weight: 450;
}

.button {
  padding-left: calc(0.4rem + var(--tab) * 1.2rem);
  width: 100%;
  text-align: start;
  transition: 150ms ease-in;
}

.button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

</style>