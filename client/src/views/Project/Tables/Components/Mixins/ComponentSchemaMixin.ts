import {defineComponent, PropType} from "vue";
import {ComponentContextSchema, ComponentSchema, EventSchema, InputSchema} from "../../types";
import UtilSchema from "../UtilSchema.ts";

export default defineComponent({
    emits: ['event-schema'],
    props: {
        componentSchema: {
            type: Object as PropType<ComponentSchema>,
            required: true
        },
        componentContext: {
            type: Object as PropType<ComponentContextSchema>,
            default: undefined
        },
        inputSchema: {
            type: Object as PropType<InputSchema>
        }
    },
    computed: {
        CONST_SCHEMA_COMPONENT() {
            return {
                change_color: 'orange',
                error_color: 'red',

                image_size: {
                    's': '30px',
                    'm': '45px',
                    'l': '100px',
                },
                image_size_default: '30px'
            }
        },
        PROJECT() {
            return UtilSchema.getProject(this.componentContext)
        }
    },
    methods: {
        doEmitEventSchema(event: EventSchema) {
            this.$emit('event-schema', event)
        },
        doRenderReference(reference: string) {
            return UtilSchema.renderReference(reference, this.componentContext)
        },
        doRenderContextText(text: string | undefined): string | undefined {
            if (!text) return undefined
            const result = this.doRenderReference(text)
            if (result == undefined) return result
            return String(result)
        }
    }
})