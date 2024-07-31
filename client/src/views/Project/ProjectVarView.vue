<script lang="ts">
import {defineComponent} from 'vue'
import {useVarsStore} from "../../stores/vars.store.ts";
import ProjectMainView from "./ProjectMainLayout.vue";
import {cropText} from "../Utils.ts";
import InputList from "../Tables/Edit/InputList.vue";
import RemoveButton from "../Tables/Edit/Components/RemoveButton.vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

export default defineComponent({
  name: "ProjectVarView",
  components: {FontAwesomeIcon, RemoveButton, InputList, ProjectMainView},
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
      headers: [
        {title: 'Key', key: 'key'},
        {title: 'Value', key: 'value'},
        {title: 'Action', value: 'actions'}
      ],
      newVar: {
        key: '',
        value: ''
      },
      loadingSave: false
    }
  },
  methods: {
    cropText,
    async save(isActive: any) {
      this.loadingSave = true
      await this.varsStore.create(this.project, this.newVar.key, this.newVar.value)
      this.loadingSave = false
      isActive.value = false
    },
    async change(key: string, value: string) {
      this.loadingSave = true
      await this.varsStore.change(this.project, key, value)
      this.loadingSave = false
    }
  }
})
</script>

<template>
  <ProjectMainView :project="project">
    <VDataTable
        :headers="headers"
        :items="varsStore.getByProject(project)"
        density="compact"
        variant="outlined"
        :loading="varsStore.loadings.load"
    >
      <template v-slot:top>
        <VToolbar
            flat
            color="transparent"
            density="compact"
        >
          <VToolbarTitle>Variables {{ project }}</VToolbarTitle>
          <VDialog>
            <template v-slot:activator="{ props: activatorProps }">
              <VBtn
                  variant="outlined"
                  dark
                  text="New Item"
                  v-bind="activatorProps"
              />
            </template>
            <template v-slot:default="{ isActive }">
              <VCard>
                <VCardText>
                  <VRow>
                    <VTextField v-model="newVar.key" label="Key"/>
                  </VRow>
                  <VRow>
                    <VTextarea v-model="newVar.value" label="Value"/>
                  </VRow>
                  <VRow>
                    <VBtn :loading="loadingSave" class="mr-2" color="success" text="Save" @click.prevent="save(isActive)"/>
                  </VRow>
                </VCardText>
              </VCard>
            </template>
          </VDialog>
        </VToolbar>
      </template>
      <template v-slot:loading>
        <VSkeletonLoader type="table-row@5"></VSkeletonLoader>
      </template>
      <template v-slot:item.value="{ item }">
        {{ cropText(item.value!) }}
      </template>
      <template v-slot:item.actions="{ item }">
        <VDialog>
          <template v-slot:activator="{ props: activatorProps }">
            <FontAwesomeIcon class="pointer" style="margin-right: 0.5rem" icon="fa-pen" v-bind="activatorProps"/>
          </template>
          <template v-slot:default="{ isActive }">
            <VCard>
              <VCardText>
                <VRow>
                  <VTextField v-model="item.key" label="Key"/>
                </VRow>
                <VRow>
                  <VTextarea v-model="item.value" label="Value"/>
                </VRow>
                <VRow>
                  <VBtn :loading="loadingSave" class="mr-2" color="success" text="Save"
                        @click.prevent="change(item.key, item.value!)"/>
                </VRow>
              </VCardText>
            </VCard>
          </template>
        </VDialog>
        <RemoveButton variant="icon" :text="cropText(item.value!)"
                      :remove="() => varsStore.remove(project, item.key)"/>
      </template>
    </VDataTable>
  </ProjectMainView>
</template>

<style scoped>

</style>