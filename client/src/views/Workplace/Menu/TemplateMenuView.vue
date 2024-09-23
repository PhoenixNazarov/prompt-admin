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
      <VDialog max-width="350px">
        <template v-slot:activator="{ props: activatorProps }">
          <div class="pointer" v-bind="activatorProps">
            Create new template
            <FontAwesomeIcon icon="plus"/>
          </div>
        </template>
        <template v-slot:default="{ isActive }">
          <VContainer>
            <VCard>
              <VCardText>
                <VRow>
                  <VTextField v-model="newVar.key" label="Key"/>
                </VRow>
                <VRow>
                  <VBtn :loading="loadingSave" class="mr-2" color="success" text="Save"
                        @click.prevent="save(isActive)"/>
                </VRow>
              </VCardText>
            </VCard>
          </VContainer>
        </template>
      </VDialog>
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