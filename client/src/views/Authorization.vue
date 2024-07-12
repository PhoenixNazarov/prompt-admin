<script lang="ts">
import {defineComponent} from 'vue'
import {useAccountStore} from "../stores/user.store.ts";

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
      this.loading = false
    }
  }
})
</script>

<template>
  <VSheet class="mx-auto" max-width="300">
    <VForm>
      <VTextField
          v-model="form.login"
          type="login"
          label="Login"
      ></VTextField>
      <VTextField
          v-model="form.password"
          type="password"
          label="Password"
      ></VTextField>

      <v-btn
          :loading="loading"
          text="Submit"
          type="submit"
          @click.prevent="login"
          block
      ></v-btn>
    </VForm>
  </VSheet>
</template>

<style scoped>
.form {
  color: var(--color-5);
  padding: 2rem;
}
</style>