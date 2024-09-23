import {defineComponent, PropType} from "vue";
import {ChangeContextEvent, ComponentContextType, DataElementComponentSchema} from "../../types";
import ComponentSchemaMixin from "./ComponentSchemaMixin.ts";
import UtilSchema from "../UtilSchema.ts";

export default defineComponent({
    mixins: [ComponentSchemaMixin],
    props: {
        componentSchema: {
            type: Object as PropType<DataElementComponentSchema>,
            required: true
        }
    },
    data() {
        return {
            model: undefined as ComponentContextType | undefined,
            originModel: undefined as ComponentContextType | undefined
        }
    },
    methods: {
        doWrite(newModel: string | undefined) {
            const event: ChangeContextEvent = {
                eventType: 'change-context',
                contextKey: this.componentSchema.reference,
                value: newModel
            }
            this.doEmitEventSchema(event)
        },
        changeColor() {
            if (this.componentSchema.nullable == false && this.model == undefined) return this.CONST_SCHEMA_COMPONENT.error_color
            return this.originModel != this.model ? this.CONST_SCHEMA_COMPONENT.change_color : undefined
        },
        initDefault() {
            const originModel = this.doRenderReference(this.componentSchema.reference)
            let model = this.doRenderReference(this.componentSchema.reference)
            if (!model && this.componentSchema.default != undefined) {
                model = this.componentSchema.default
                const event: ChangeContextEvent = {
                    eventType: 'change-context',
                    contextKey: this.componentSchema.reference,
                    value: model
                }
                this.doEmitEventSchema(event)
            }
            this.model = model
            this.originModel = originModel
        }
    },
    mounted() {
        this.initDefault()
    },
    watch: {
        componentContext: {
            handler() {
                const newModel = this.doRenderReference(this.componentSchema.reference)
                if (!newModel) {
                    this.model = newModel
                    return
                }
                const type = (newModel as any)._type
                if (type == 'update') {
                    const value = (newModel as any).value
                    this.model = value
                    this.originModel = value
                    UtilSchema.setValueByKeyForContext(this.componentSchema.reference, value, this.componentContext)
                } else {
                    this.model = newModel
                }
            },
            deep: true
        }
    }
})
