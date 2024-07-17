import {defineStore} from "pinia";
import {
    abstractStoreFactory,
    abstractStoreFactoryGetters,
    abstractStoreFactoryState,
    BaseEntity
} from "./abstractStoreFactory.ts";

export interface Mapping extends BaseEntity {
    table: string
    field: string

    description: string
    field_name: string
    connection_name: string
}


export const useMappingStore = defineStore({
    id: 'mapping',
    state: () => ({
        ...abstractStoreFactoryState<Mapping>()
    }),
    getters: {
        getConnections(state) {
            const result = new Map<string, Map<string, Mapping[]>>

            state.entity.forEach(
                e => {
                    const connection = e.connection_name
                    const key = e.table
                    let connectionMap = result.get(connection)
                    if (connectionMap == undefined) {
                        connectionMap = new Map()
                        result.set(connection, connectionMap)
                    }
                    const alreadyList = connectionMap.get(key)
                    if (alreadyList != undefined) {
                        alreadyList.push(e)
                    } else {
                        const keyList = [e]
                        connectionMap.set(key, keyList)
                    }
                }
            )
            return result
        },
        getByTableField: state => {
            return (table: string, field: string) => state.entity.find(e => e.table == table && e.field == field)
        },
        ...abstractStoreFactoryGetters<Mapping>()
    },
    actions: {
        ...abstractStoreFactory<Mapping>('mapping')
    }
})