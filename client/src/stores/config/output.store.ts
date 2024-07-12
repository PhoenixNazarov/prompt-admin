import {defineStore} from "pinia";
import {abstractStoreFactory, abstractStoreFactoryState, BaseEntity} from "./abstractStoreFactory.ts";

export interface Output extends BaseEntity{
    output: string
}


export const useOutputStore = defineStore({
    id: 'output',
    state: () => ({
        ...abstractStoreFactoryState<Output>()
    }),
    getters: {
        getById: state => {
            return (id: number) => state.entity.find(e => e.id == id)
        }
    },
    actions: {
        ...abstractStoreFactory('output')
    }
})