<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {ConsistentReport} from "../../stores/format.store.ts";
import ConsistentReportCase from "./ConsistentReportCase.vue";

export default defineComponent({
  name: "ConsistentReport",
  components: {ConsistentReportCase, FontAwesomeIcon},
  props: {
    report: {
      type: Object as PropType<ConsistentReport>,
    }
  }
})
</script>

<template>
  <div>
    <h1>Consistent report</h1>

    <ConsistentReportCase title="Dump to json" :value="report?.to_dict"/>

    <ConsistentReportCase title="Create an example object" :value="report?.make_example_obj"/>
    <ConsistentReportCase title="Create a schema for an example object" :value="report?.make_example_obj_converse"/>
    <ConsistentReportCase title="Schema for an example object equal origin schema" :value="report?.make_example_obj_converse_equal"/>

    <ConsistentReportCase title="Create an example json object" :value="report?.make_example_json"/>
    <ConsistentReportCase title="Create a schema for an example json object" :value="report?.make_example_json_converse"/>
    <ConsistentReportCase title="Schema for an example json object equal origin schema" :value="report?.make_example_json_converse_equal"/>

    <ConsistentReportCase title="Create an example xml object" :value="report?.make_example_xml"/>
    <ConsistentReportCase title="Create a schema for an example xml object" :value="report?.make_example_xml_converse"/>
    <ConsistentReportCase title="Schema for an example xml object equal origin schema" :value="report?.make_example_xml_converse_equal"/>
  </div>
</template>

<style scoped>
@import '/src/styles/hint.css';

</style>