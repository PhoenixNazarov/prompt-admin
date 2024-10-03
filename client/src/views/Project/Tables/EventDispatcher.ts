import {
    ComponentContextDict,
    ComponentContextSchema,
    ComponentContextType,
    EventSchema,
    RequestProjectEvent,
} from "./types";
import UtilSchema from "./Components/UtilSchema.ts";
import {useTableStore} from "../../../stores/project/tables/table.store.ts";

class EventDispatcher {

    onContextEvent(event: EventSchema, componentContext: ComponentContextSchema): boolean | undefined {
        switch (event.eventType) {
            case "change-context":
                this.onChangeContext(event.contextKey, event.value, componentContext)
                return true
            case "request-project":
                this.onRequestProjectEvent(event, componentContext)
                return true
        }
    }

    async onRequestProjectEvent(requestProjectEvent: RequestProjectEvent, componentContext: ComponentContextSchema) {
        const tableStore = useTableStore()
        const project = UtilSchema.getProject(componentContext)
        try {
            if (requestProjectEvent.method == 'get') {
                await tableStore.executeGet(project, requestProjectEvent.url)
            } else {
                await tableStore.executePost(project, requestProjectEvent.url, UtilSchema.renderObject(requestProjectEvent.data, componentContext))
            }
        } catch (e) {
            alert('Error on execute: ' + String(requestProjectEvent))
        }
    }

    async onUpdateItemEvent(
        item: ComponentContextDict,
        originItem: ComponentContextDict,
        id: number,
        table: string,
        componentContext: ComponentContextSchema,
    ) {
        const tableStore = useTableStore()
        const updateItems = Object.entries(item).filter(
            el => {
                return originItem[el[0]] != el[1]
            }
        )

        const keys = updateItems.map(
            el => {
                return {
                    key: el[0],
                    value: el[1]
                }
            })
        const project = UtilSchema.getProject(componentContext)
        try {
            await tableStore.updateItem(project, table, id, keys)
        } catch (e) {
            alert('Error, when update item')
        }
    }

    async onCreateItemEvent(
        item: ComponentContextDict,
        table: string,
        componentContext: ComponentContextSchema,
    ): Promise<{ id: number }> {
        const tableStore = useTableStore()
        const project = UtilSchema.getProject(componentContext)
        const items = Object.entries(item).map(
            el => {
                return {
                    key: el[0],
                    value: el[1]
                }
            })

        try {
            return await tableStore.createItem(project, table, items)
        } catch (e) {
            alert('Error, when create item')
            throw new Error('Error, when create item')
        }
    }

    async onDeleteItemEvent(
        table: string,
        id: number,
        componentContext: ComponentContextSchema,
    ) {
        const tableStore = useTableStore()
        const project = UtilSchema.getProject(componentContext)
        await tableStore.deleteItem(project, table, id)
    }

    onChangeContext(contextKey: string, value: ComponentContextType, componentContext: ComponentContextSchema) {
        UtilSchema.setValueByKeyForContext(contextKey, value, componentContext)
    }

}

export default new EventDispatcher()