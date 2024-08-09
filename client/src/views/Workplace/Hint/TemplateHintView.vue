<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Prompt} from "../../../stores/prompt.store.ts";
import {useVarsStore} from "../../../stores/vars.store.ts";
import RemoveButton from "../../Tables/Edit/Components/RemoveButton.vue";
import {cropText} from "../../Utils.ts";

export default defineComponent({
  name: "TemplateHintView",
  components: {RemoveButton},
  props: {
    prompt: {
      type: Object as PropType<Prompt>,
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
      loading: {
        save: false
      }
    }
  },
  methods: {
    cropText,
    async save() {
      this.loading.save = true
      if (this.prompt.templateData?.project && this.prompt.templateData?.key)
        await this.varsStore.change(this.prompt.templateData?.project, this.prompt.templateData?.key, this.prompt.value)
      this.loading.save = false
    },
    async remove() {
      if (this.prompt.templateData?.project && this.prompt.templateData?.key)
        await this.varsStore.remove(this.prompt.templateData?.project, this.prompt.templateData?.key)
      this.$emit('closePrompt', this.prompt)
    }
  }
})
</script>

<template>
  <div class="hint">
    <div>
      <VBtn class="mr-4" variant="tonal" density="comfortable" @click.prevent="save" :loading="loading.save">Save</VBtn>
      <RemoveButton :text="cropText(prompt.value)" density="comfortable" :remove="() => remove()"/>
    </div>
    <VCard class="mt-4" variant="tonal">
      <VCardTitle>
        Template {{ prompt.templateData?.key }}
      </VCardTitle>
      <VCardText>
        <b>project: </b> {{ prompt.templateData?.project }}<br>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.hint {
  padding: 1rem;
  color: var(--color-5);
}
</style>