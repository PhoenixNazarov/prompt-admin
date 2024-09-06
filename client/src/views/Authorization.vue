<script lang="ts">
import {defineComponent} from 'vue'
import {useAccountStore} from "../stores/user.store.ts";
import {RouterService} from "../plugins/router.ts";

export default defineComponent({
  name: "Authorization",
  setup() {
    const accountStore = useAccountStore()
    return {
      accountStore
    }
  },
  data() {
    return {
      form: {
        login: '',
        password: ''
      },
      formValid: false,
      loading: false
    }
  },
  methods: {
    async login() {
      this.loading = true
      await this.accountStore.login(this.form.login, this.form.password)
      await RouterService.goToWorkplace()
      this.loading = false
    }
  }
})
</script>

<template>
  <VContainer>
    <VRow>
      <VCol style="width: 100vh">
        <VCard class="mx-auto authorization" title="Prompt-Admin" variant="flat">
          <VCardText>
            <VTextField
                v-model="form.login"
                type="login"
                label="Login"
                variant="outlined"
            />
            <VTextField
                v-model="form.password"
                type="password"
                label="Password"
                variant="outlined"
            />

            <VBtn
                :loading="loading"
                text="Submit"
                type="submit"
                @click.prevent="login"
                block
            />
          </VCardText>
        </VCard>
      </VCol>
    </VRow>
  </VContainer>
</template>

<style scoped>

.authorization {
  width: 300px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>