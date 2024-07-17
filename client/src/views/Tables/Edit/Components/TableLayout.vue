<script lang="ts">
import {defineComponent} from 'vue'
import MainLayout from "../../../../layouts/MainLayout.vue";
import {RouterService} from "../../../../plugins/router.ts";

export default defineComponent({
  name: "TableLayout",
  computed: {
    RouterService() {
      return RouterService
    }
  },
  components: {MainLayout},
  props: {
    list: {
      type: String,
      default: 'mapping'
    }
  },
  data() {
    return {
      tabList: this.list
    }
  }
})
</script>

<template>
  <div class="outer-y" style="height: 100%">
    <VContainer>
      <VRow>
        <VCol sm="2" md="2">
          <VTabs style="color: var(--color-5)"
                 slider-color="var(--color-5)"
                 direction="vertical"
                 v-model="tabList"
          >
            <VTab text="Mapping" value="mapping" @click.prevent="RouterService.goToTableList('mapping')"/>
            <VTab text="Mapping Entity" value="mapping-entity"
                  @click.prevent="RouterService.goToTableList('mapping-entity')"/>
            <VTab text="Output" value="output" @click.prevent="RouterService.goToTableList('output')"/>
            <VTab text="Macro" value="macro" @click.prevent="RouterService.goToTableList('macro')"/>
            <VTab text="Input" value="input" @click.prevent="RouterService.goToTableList('input')"/>
            <VTab text="Prompt" value="prompt" @click.prevent="RouterService.goToTableList('prompt')"/>
          </VTabs>
        </VCol>
        <VCol>
          <RouterView/>
        </VCol>
      </VRow>
    </VContainer>
  </div>
</template>

<style scoped>

</style>