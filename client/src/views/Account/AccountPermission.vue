<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {Account, Permission, useAccountStore} from "../../stores/user.store.ts";
import AccountPermissionValue from "./AccountPermissionValue.vue";

export default defineComponent({
  name: "AccountPermission",
  components: {AccountPermissionValue},
  setup() {
    const accountStore = useAccountStore()
    return {
      accountStore
    }
  },
  props: {
    account: {
      type: Object as PropType<Account>,
      required: true
    }
  },
  data() {
    return {
      inline: true,
      permissions: undefined as undefined | Permission[]
    }
  },
  methods: {
    async toggle() {
      if (this.inline) {
        if (this.permissions == undefined && this.account.id) {
          this.permissions = await this.accountStore.loadPermission(this.account.id)
        }
        this.inline = false
      } else {
        this.inline = true
      }
    },
    projects() {
      if (!this.permissions) return []
      return Object.entries(this.permissions).filter(el => el[0] == 'project').map(el => el[1])
    },
    getValue(key: string, project: string | undefined = undefined, default_: number | undefined = undefined) {
      const val = this.permissions?.find(el => el.key == key && el.project == project)?.value
      return val != undefined ? val : default_
    },
    setProjectAccess(project: string, value: boolean) {
      this.permissions = this.permissions?.filter(el => el.key != 'project' || el.project != project)
      this.permissions?.push({
        account_id: 0,
        key: 'project',
        value: value ? 2 : 0,
        project: project
      })
      this.updateModel('project', value ? 2 : 0, project)
    },
    updateModel(key: string, value: number, project: string | undefined) {
      if (this.account.id)
        this.accountStore.setPermission(this.account.id, key, value, project)
    }
  }
})
</script>

<template>
  <VCard variant="outlined">
    <VCardTitle @click.prevent="toggle" class="pointer">
      {{ account.login }}
    </VCardTitle>
    <VCardText v-if="!inline && permissions">
      <AccountPermissionValue
          label="config_tables"
          :value="getValue('config_tables', undefined, 1)"
          hint="Edit config mappings, mappings entity and etc"
          @updateModel="el => updateModel('config_tables', el, undefined)"/>
      <AccountPermissionValue
          label="config_accounts"
          :value="getValue('config_accounts', undefined, 1)"
          hint="Edit account permissions configs"
          @updateModel="el => updateModel('config_accounts', el, undefined)"/>
      <AccountPermissionValue
          label="healthcheck"
          :value="getValue('healthcheck', undefined, 1)"
          hint="Access to monitor healthcheck and add new check endpoints"
          @updateModel="el => updateModel('healthcheck', el, undefined)"/>

      <div v-for="proj in accountStore.projects">
        <div style="display: flex; align-items: center;">
          <h3 class="mr-5">
            {{ proj }}
          </h3>
          <VSwitch label="Access" density="compact" :hide-details="true" color="primary"
                   :model-value="getValue('project', proj, 0)! > 0"
                   @update:model-value="val => setProjectAccess(proj, val)"
          />
        </div>

        <div v-if="getValue('project', proj, 0)! > 0">
          <AccountPermissionValue
              label="project_prompt"
              :value="getValue('project_prompt', proj, 1)"
              hint="Access to view or edit in workplace prompts"
              @updateModel="el => updateModel('project_prompt', el, proj)"/>
          <AccountPermissionValue
              label="project_blog"
              :value="getValue('project_blog', proj, 1)"
              hint="Access to view or edit project`s blog"
              @updateModel="el => updateModel('project_blog', el, proj)"/>
          <AccountPermissionValue
              label="project_variables"
              :value="getValue('project_variables', proj, 1)"
              hint="Access to view or edit project`s variables"
              @updateModel="el => updateModel('project_variables', el, proj)"/>
          <AccountPermissionValue
              label="project_status"
              :value="getValue('project_status', proj, 1)"
              hint="Access to view project status and run unit status"
              @updateModel="el => updateModel('project_status', el, proj)"/>
          <AccountPermissionValue
              label="project_synchronize"
              :value="getValue('project_synchronize', proj, 0)"
              hint="Access to manual synchronize"
              @updateModel="el => updateModel('project_synchronize', el, proj)"/>
          <AccountPermissionValue
              label="project_tables_upload"
              :value="getValue('project_tables_upload', proj, 1)"
              hint="Access to manual change tables schema"
              @updateModel="el => updateModel('project_tables_upload', el, proj)"/>
          <AccountPermissionValue
              label="project_tables"
              :value="getValue('project_tables', proj, 1)"
              hint="Access to write or edit project`s tables"
              @updateModel="el => updateModel('project_tables', el, proj)"/>
        </div>
      </div>
    </VCardText>
  </VCard>
</template>

<style scoped>

</style>