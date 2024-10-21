<script lang="ts">
import {defineComponent} from 'vue'
import {useAccountStore} from "../../stores/user.store.ts";
import AccountPermission from "./AccountPermission.vue";

export default defineComponent({
  name: "ModeratePermissionsView",
  components: {AccountPermission},
  setup() {
    const accountStore = useAccountStore()
    return {
      accountStore
    }
  },
  mounted() {
    this.accountStore.loadAll()
  },
  methods: {
    access() {
      const permission = this.accountStore.permissions?.find(el => el.key == 'config_accounts')?.value
      return permission && permission > 0
    }
  }
})
</script>

<template>
  <VCard
      v-if="access()">
    <VCardTitle>
      Moderate Accounts
    </VCardTitle>
    <VCardText>
      <VRow>
        <VCol>
          <b>Value</b>
        </VCol>
        <VCol>
          <b>Meaning</b>
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          0
        </VCol>
        <VCol>
          Disable
        </VCol>
      </VRow>
      <VRow>
        <VCol>
          1
        </VCol>
        <VCol>
          Enable, Can read
        </VCol>
      </VRow>
      <VRow class="mb-5">
        <VCol>
          2
        </VCol>
        <VCol>
          Enable, Can read and write (process)
        </VCol>
      </VRow>

      <VVirtualScroll :items="accountStore.entity" :renderless="true">
        <template v-slot:default="{ item }">
          <AccountPermission :account="item"/>
        </template>
      </VVirtualScroll>
    </VCardText>
  </VCard>
</template>

<style scoped>

</style>