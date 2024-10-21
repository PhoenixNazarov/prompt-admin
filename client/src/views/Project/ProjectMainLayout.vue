<script lang="ts">
import {defineComponent} from 'vue'
import {useBlogGroupStore} from "../../stores/project/blogGroup.store.ts";
import MegaMenu from 'primevue/megamenu';
import {RouterService} from "../../plugins/router.ts";
import {useBlogPostStore} from "../../stores/project/blogPost.store.ts";
import {useProjectStore} from "../../stores/project/project.store.ts";


export default defineComponent({
  name: "ProjectMainView",
  computed: {
    RouterService() {
      return RouterService
    }
  },
  components: {MegaMenu},
  props: {
    project: {
      type: String,
      required: true
    },
    groupId: {
      type: String
    }
  },
  setup() {
    const blogGroupStore = useBlogGroupStore()
    const blogPostStore = useBlogPostStore()
    const projectStore = useProjectStore()
    return {
      blogGroupStore,
      blogPostStore,
      projectStore
    }
  },
  methods: {
    async createGroup() {
      await this.blogGroupStore.save({
        project: this.project,
        title: 'New Group',
      })
    },
    async createPost() {
      const groupId_ = !this.groupId ? undefined : Number.parseInt(this.groupId)
      await this.blogPostStore.save(
          {
            project: this.project,
            content: "Content",
            title: "Title",
            group_id: groupId_ == -1 ? undefined : groupId_,
          }
      )
    },
    editGroup() {
      if (this.groupId == '-1' || this.groupId == undefined) {
        return []
      }
      return [
        {
          label: 'Edit group',
          command: () => {
            if (!this.groupId) return
            const blogGroup = this.blogGroupStore.getById(Number.parseInt(this.groupId))
            if (!blogGroup) return
            this.editGroupDialog = true
            this.editGroupTitle = blogGroup.title
          }
        },
        {
          label: 'Remove group',
          command: () => {
            this.removeGroupDialog = true
          }
        }
      ]
    },
    async removeGroup() {
      if (this.groupId) await this.blogGroupStore.remove(Number.parseInt(this.groupId))
      await RouterService.goToProject(this.project)
    },
    async doEditGroup() {
      if (!this.groupId) return
      const blogGroup = this.blogGroupStore.getById(Number.parseInt(this.groupId))
      if (!blogGroup) return
      if (this.groupId) await this.blogGroupStore.save({
        ...blogGroup,
        title: this.editGroupTitle
      })
    }
  },
  data() {
    return {
      removeGroupDialog: false,
      editGroupDialog: false,
      editGroupTitle: ''
    }
  },
  mounted() {
    this.blogGroupStore.findByKey('project', this.project)
  },
})
</script>

<template>
  <div class="outer-y" style="height: 100%">
    <VContainer>
      <VRow>
        <VCol>
          <MegaMenu :model="[
              {
                label: project,
                icon: 'pi pi-server',
                items: [[
                    {
                      label: 'Project',
                      items: [
                          ...projectStore.projects.map(
                              project_ => {
                                return {
                                  label: project_,
                                  command: () => RouterService.goToProject(project_)
                                }
                              }
                          )
                      ]
                    }
                ]]
              },
              {
                label: groupId == undefined ? 'Main' : blogGroupStore.getById(Number.parseInt(groupId))?.title,
                icon: 'pi pi-box',
                items: [[
                  {
                    label: 'Group',
                    items:
                      [
                        {
                          label: 'Main',
                          command: () => RouterService.goToProjectGroup(project, -1)
                        },
                        ...blogGroupStore.getGroupByProject(project).map(
                          group => {
                            return {
                              label: group.title,
                              command: () => RouterService.goToProjectGroup(project, group.id)
                            }
                          }
                        )
                      ]
                    }
                  ]]
              },
              {
                label: 'Edit',
                icon: 'pi pi-pencil',
                items: [[
                    {
                      label: 'Group',
                      items: [
                          {
                            label: 'Add group',
                            command: () => createGroup()
                          },
                          ...editGroup()
                      ]
                    },
                    {
                      label: 'Post',
                      items: [
                          {
                            label: 'Add post',
                            command: () => createPost()
                          }
                      ]
                    }
                ]]
              },
              {
                label: 'Variables',
                icon: 'pi pi-server',
                command: () => RouterService.goToProjectVars(project)
              },
              {
                label: 'Status',
                icon: 'pi pi-heart',
                command: () => RouterService.goToProjectStatus(project)
              },
              {
                label: 'Synchronize',
                icon: 'pi pi-sync',
                command: () => projectStore.sync(project)
              },
              {
                label: 'Tables',
                icon: 'pi pi-table',
                items: [[
                    {
                      label: 'Tables Navigation',
                      items: [
                          {
                            label: 'Data',
                            command: () => RouterService.goToProjectTables(project)
                          },
                          {
                            label: 'Edit Tables',
                            command: () => RouterService.goToProjectTableEdit(project)
                          }
                      ]
                    },
                ]]
              },
            ]"/>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          <slot/>
        </VCol>
      </VRow>
    </VContainer>

    <VDialog
        v-model="removeGroupDialog"
        width="auto"
    >
      <VCard
          max-width="400"
          text="Do you want to remove this group?"
          :title="`Remove group #${groupId}`"
      >
        <template v-slot:actions>
          <VBtn
              class="ms-auto"
              text="Ok"
              @click="removeGroupDialog = false; removeGroup()"
          />
          <VBtn
              class="ms-auto"
              text="No"
              @click="removeGroupDialog = false"
          />
        </template>
      </VCard>
    </VDialog>

    <VDialog
        v-model="editGroupDialog"
        max-width="600"
    >
      <VCard
          :title="`Edit group #${groupId}`"
      >
        <VCardText>
          <VTextField v-model="editGroupTitle" density="compact"/>
        </VCardText>
        <template v-slot:actions>
          <VBtn
              class="ms-auto"
              text="Ok"
              @click="editGroupDialog = false; doEditGroup()"
          />
          <VBtn
              class="ms-auto"
              text="No"
              @click="editGroupDialog = false"
          />
        </template>
      </VCard>
    </VDialog>

  </div>
</template>

<style scoped>
</style>