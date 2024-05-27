import {defineStore} from "pinia";
import {abstractStoreFactory, BaseEntity} from "./abstractStoreFactory.ts";

export interface Output extends BaseEntity{
    output: string
}


export const useOutputStore = defineStore({
    id: 'output',
    state: () => ({
        entity: [] as Output[]
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