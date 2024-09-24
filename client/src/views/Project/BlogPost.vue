<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {BlogPost, useBlogPostStore} from "../../stores/project/blogPost.store.ts";
import Editor from 'primevue/editor';
import RemoveButton from "../Tables/Edit/Components/RemoveButton.vue";

import "quill/dist/quill.core.css"
import "quill/dist/quill.snow.css"

export default defineComponent({
  name: "BlogPost",
  components: {RemoveButton, Editor},
  setup() {
    const blogPostStore = useBlogPostStore()
    return {
      blogPostStore
    }
  },
  props: {
    post: {
      type: Object as PropType<BlogPost>,
      required: true
    }
  },
  data() {
    return {
      title: this.post.title,
      content: this.post.content,
      edit: false,
      loading: false
    }
  },
  methods: {
    async save() {
      this.loading = true
      await this.blogPostStore.save({
        ...this.post,
        title: this.title,
        content: this.content
      })
      this.loading = false
      this.edit = false
    }
  },
  watch: {
    post(newVal: BlogPost) {
      this.title = newVal.title
      this.content = newVal.content
    }
  }
})
</script>

<template>
  <VCard>
    <VCardTitle>
      <div style="display: flex;align-items: center;justify-content: space-between;">
        <VTextField v-if="edit" hide-details v-model="title" density="compact"/>
        <div v-if="!edit">
          {{ post.title }}
        </div>
        <div>
          <VBtn v-if="!edit" icon="mdi-pen" density="compact" @click.prevent="edit=true"/>

          <VBtn :loading="loading" v-if="edit" icon="mdi-content-save" color="success" density="compact"
                @click.prevent="save()"
                style="margin-right: 0.5rem"/>
          <VBtn v-if="edit" icon="mdi-close" color="" density="compact"
                @click.prevent="edit=false; content = post.content"
                style="margin-right: 0.5rem"/>

          <RemoveButton v-if="edit" variant="icon" :text="post.title"
                        :remove="() => blogPostStore.remove(post.id)"/>
        </div>
      </div>
    </VCardTitle>
    <VCardText>
      <div class="ql-editor ql-snow" v-if="!edit" v-html="content"></div>
      <Editor v-if="edit" v-model="content" editorStyle="height: 500px"/>
    </VCardText>
  </VCard>
</template>

<style scoped>

</style>