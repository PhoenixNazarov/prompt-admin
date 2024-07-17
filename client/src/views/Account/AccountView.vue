<script lang="ts">
import {defineComponent} from 'vue'
import {useAccountStore} from "../../stores/user.store.ts";
import {RouterService} from "../../plugins/router.ts";
import SettingsEditView from "./SettingsEditView.vue";

export default defineComponent({
  name: "AccountView",
  components: {SettingsEditView},
  setup() {
    const accountStore = useAccountStore()
    return {
      accountStore
    }
  },
  data() {
    const accountStore = useAccountStore()
    return {
      login: accountStore.account?.login,

      loadingLogout: false
    }
  },
  methods: {
    async logout() {
      this.loadingLogout = true
      await this.accountStore.logout()
      this.loadingLogout = false
      await RouterService.goToAuthorization()
    }
  }
})
</script>

<template>
  <VContainer>
    <VCard>
      <VCardTitle>
        Account
      </VCardTitle>
      <VCardText>
        <VRow>
          <VCol>
            <VTextField hide-details v-model="login" label="Login" disabled variant="outlined"/>
          </VCol>
        </VRow>
        <VRow>
          <VCol>
            <VBtn text="Logout" :loading="loadingLogout" @click.prevent="logout"/>
          </VCol>
        </VRow>
        <VRow>
          <VCol>
            <SettingsEditView/>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>
  </VContainer>
</template>

<style scoped>

</style>