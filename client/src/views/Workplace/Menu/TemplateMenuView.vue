<script lang="ts">
import {defineComponent} from 'vue'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {useVarsStore, Variable} from "../../../stores/vars.store.ts";
import {Prompt} from "../../../stores/prompt.store.ts";

export default defineComponent({
  name: "TemplateMenuView",
  components: {FontAwesomeIcon},
  props: {
    project: {
      type: String,
      required: true
    }
  },
  setup() {
    const varsStore = useVarsStore()
    return {
      varsStore
    }
  },
  data() {
    return {
      newVar: {
        key: ''
      },
      loadingSave: false
    }
  },
  methods: {
    async save(isActive: any) {
      this.loadingSave = true
      await this.varsStore.create(this.project, this.newVar.key, '', true)
      this.loadingSave = false
      isActive.value = false
    },
    doSelect(template: Variable) {
      const selectPrompt: Prompt = {
        id: 0,
        field: "",
        table: "",
        value: template.value,
        originValue: template.value,
        mapping_id: -1,
        templateData: {
          key: template.key,
          project: this.project
        }
      }
      this.$emit('selectPrompt', selectPrompt)
    }
  },
  mounted() {
    this.varsStore.load(this.project)
  }
})
</script>

<template>
  <VListGroup :value="project + '_template'" dense="compact">
    <template v-slot:activator="{ props }">
      <VListItem
          density="compact"
          v-bind="props"
      >
        <div>
          <FontAwesomeIcon icon="file"/>
          Templates
        </div>
      </VListItem>
    </template>

    <VListItem density="compact">

    </VListItem>

    <VListItem
        v-for="template in varsStore.getTemplateByProject(project)"
        @click.prevent="doSelect(template)"
        density="compact"
    >
      {{ template.key }}
    </VListItem>

    <VSkeletonLoader
        color="transparent"
        type="list-item"
        v-if="varsStore.loadings.load"
    ></VSkeletonLoader>

  </VListGroup>
</template>

<style scoped>

</style>