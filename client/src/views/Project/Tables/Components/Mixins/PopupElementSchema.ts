import {defineComponent} from "vue";
import {ChangeContextEvent, EventSchema, ListRowClickInputSchema} from "../../types";
import DataElementSchemaMixin from "./DataElementSchemaMixin.ts";

export default defineComponent({
    mixins: [DataElementSchemaMixin],
    data() {
        const popupInputSchema: ListRowClickInputSchema | undefined = this.componentSchema.popup ? {
            inputType: 'list-row-click',
        } : undefined
        return {
            popupShow: false,
            popupInputSchema: popupInputSchema
        }
    },
    methods: {
        doPopup() {
            this.popupShow = true
        },
        doPopupEvent(event: EventSchema) {
            if (event.eventType == 'list-row-click') {
                this.popupShow = false
                const targetTable = event.row.find(el => el.column.column == this.componentSchema.popup?.targetColumn.column)
                if (!targetTable) return
                this.model = targetTable.value
                const newEvent: ChangeContextEvent = {
                    eventType: 'change-context',
                    contextKey: this.componentSchema.reference,
                    value: targetTable.value
                }
                this.doEmitEventSchema(newEvent)
            } else {
                this.doEmitEventSchema(event)
            }
        }
    }
})