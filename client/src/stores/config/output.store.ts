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
    getters: {},
    actions: {
        ...abstractStoreFactory('output')
    }
})