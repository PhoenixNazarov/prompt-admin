<script lang="ts">
import {defineComponent} from 'vue'
import {useAccountStore} from "../stores/user.store.ts";
import PaButton from "../components/PaButton.vue";

export default defineComponent({
  name: "Authorization",
  components: {PaButton},
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
      }
    }
  },
  methods: {
    login() {
      this.accountStore.login(this.form.login, this.form.password)
    }
  }
})
</script>

<template>
  <div class="form">
    <div>
      Login
      <input v-model="form.login" type="text"/>
    </div>
    <div>
      Password
      <input v-model="form.password" type="password"/>
    </div>
    <PaButton text="Login" @click.prevent="login"/>
  </div>
</template>

<style scoped>
.form {
  color: var(--color-5);
  padding: 2rem;
}
</style>