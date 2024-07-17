<script lang="ts">
import {defineComponent} from 'vue'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {RouterService} from "../../../../plugins/router.ts";
import CodeText from "../../../../components/CodeText.vue";

export default defineComponent({
  name: "RemoveButton",
  components: {CodeText, FontAwesomeIcon},
  props: {
    variant: {
      type: String,
      default: 'btn'
    },
    title: {
      type: String
    },
    text: {
      type: String
    },
    remove: {
      type: Function,
      required: true
    },
    listName: {
      type: String,
    }
  },
  data() {
    return {
      loadingDelete: false,
      error: ''
    }
  },
  methods: {
    async doRemove() {
      if (!this.remove) return
      this.loadingDelete = true
      let error = false
      try {
        await this.remove()
      } catch (e: any) {
        this.error = e.toJSON()['message']
        error = true
      }
      this.loadingDelete = false
      if (!error && this.listName) {
        await RouterService.goToTableList(this.listName)
      }
      return error
    }
  }
})
</script>

<template>
  <VDialog max-width="500px">
    <template v-slot:activator="{ props: activatorProps }">
      <VBtn v-if="variant == 'btn'" :loading="loadingDelete" color="var(--color-2)" text="Remove"
            v-bind="activatorProps"/>
      <FontAwesomeIcon v-else class="pointer" icon="fa-trash" v-bind="activatorProps"/>
    </template>
    <template v-slot:default="{ isActive }">
      <VCard>
        <VCardTitle v-if="title">
          Remove {{ title }}?
        </VCardTitle>
        <VCardText v-if="text">
          <CodeText title="Are you sure about deleting this object?" :code="String(text)" :error="error"/>
        </VCardText>
        <VCardActions>
          <div>
            <VBtn text="close" @click.prevent="isActive.value = false"/>
            <VBtn color="var(--color-2)" text="Remove"
                  :loading="loadingDelete"
                  @click.prevent="async () => {await doRemove() ? undefined : isActive.value = false}"/>
          </div>
        </VCardActions>
      </VCard>
    </template>
  </VDialog>
</template>

<style scoped>
@import '/src/styles/hint.css';
</style>