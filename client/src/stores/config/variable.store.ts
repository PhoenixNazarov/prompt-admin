import {defineStore} from "pinia";
import {abstractStoreFactory} from "./abstractStoreFactory.ts";

export interface Variable {
    id: number
    time_create: string
    name: string
    description: string
    value: string
    template: boolean
}


export const useVariableStore = defineStore({
    id: 'variable',
    state: () => ({
        entity: [] as Variable[]
    }),
    getters: {},
    actions: {
        ...abstractStoreFactory('variable')
    }
})