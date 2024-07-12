import {defineStore} from "pinia";
import {abstractStoreFactory, abstractStoreFactoryState, BaseEntity} from "./abstractStoreFactory.ts";

export interface Macro extends BaseEntity{
    macro: string
    macro_value: string
    description: string
}


export const useMacroStore = defineStore({
    id: 'macro',
    state: () => ({
        ...abstractStoreFactoryState<Macro>()
    }),
    getters: {
        getById: state => {
            return (id: number) => {
                return state.entity.find(e => e.id == id)
            }
        },
        getByIds: state => {
            return (ids: number[]) => {
                return state.entity.filter(e => ids.includes(e.id))
            }
        }
    },
    actions: {
        ...abstractStoreFactory('macro')
    }
})