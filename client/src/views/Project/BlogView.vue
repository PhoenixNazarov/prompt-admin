<script lang="ts">
import {defineComponent} from 'vue'
import ProjectMainView from "./ProjectMainLayout.vue";
import {useBlogPostStore} from "../../stores/project/blogPost.store.ts";
import BlogPost from "./BlogPost.vue";

export default defineComponent({
  name: "BlogView",
  components: {BlogPost, ProjectMainView},
  setup() {
    const blogPostStore = useBlogPostStore()
    return {
      blogPostStore
    }
  },
  props: {
    project: {
      type: String,
      required: true
    },
    groupId: {
      type: Number,
      required: true
    }
  },
  methods: {},
  mounted() {
    this.blogPostStore.loadAll()
  }
})
</script>

<template>
  <ProjectMainView :project="project" :group-id="groupId == -1? undefined : String(groupId)">
    <VSkeletonLoader type="card" v-if="blogPostStore.loadings.loadAll"/>
    <BlogPost class="mb-5" :post="post"
              v-for="post in blogPostStore.getPostByGroup(project, groupId == -1? undefined : groupId)"/>
  </ProjectMainView>
</template>

<style scoped>

</style>