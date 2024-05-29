import {defineStore} from "pinia";
import {abstractStoreFactory, BaseEntity} from "./abstractStoreFactory.ts";

export interface Input extends BaseEntity{
    macro: string
    macro_value: string
    description: string
}


export const useInputStore = defineStore({
    id: 'input',
    state: () => ({
        entity: [] as Input[]
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
        ...abstractStoreFactory('input')
    }
})