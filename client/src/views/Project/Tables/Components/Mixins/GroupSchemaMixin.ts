import {defineComponent, PropType} from "vue";
import ComponentSchemaMixin from "./ComponentSchemaMixin.ts";
import {GroupSchema} from "../../types";

export default defineComponent({
    mixins: [ComponentSchemaMixin],
    props: {
        componentSchema: {
            type: Object as PropType<GroupSchema>,
            required: true
        }
    }
})