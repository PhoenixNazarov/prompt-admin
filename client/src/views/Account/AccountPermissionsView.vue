<script lang="ts">
import {defineComponent} from 'vue'
import {useAccountStore} from "../../stores/user.store.ts";

export default defineComponent({
  name: "AccountPermissionsView",
  setup() {
    const accountStore = useAccountStore()
    return {
      accountStore
    }
  }
})
</script>

<template>
  <VCard>
    <VCardTitle>
      AccountPermissions
    </VCardTitle>
    <VCardText>
      <VCard variant="tonal">
        <VCardText :loading="accountStore.loadings.loadPermissions" v-if="accountStore.permissions">
          <p v-for="permission of accountStore.permissions">
            {{ permission.key }}: {{ permission.value }} ({{ permission.project }})
          </p>
        </VCardText>
      </VCard>
    </VCardText>
  </VCard>
</template>

<style scoped>

</style>