import {defineStore} from "pinia";
import {
    abstractStoreFactory,
    abstractStoreFactoryGetters,
    abstractStoreFactoryState,
    BaseEntity
} from "./abstractStoreFactory.ts";

export interface Output extends BaseEntity {
    output: string
}


export const useOutputStore = defineStore({
    id: 'output',
    state: () => ({
        ...abstractStoreFactoryState<Output>()
    }),
    getters: {
        ...abstractStoreFactoryGetters<Output>()
    },
    actions: {
        ...abstractStoreFactory<Output>('output')
    }
})