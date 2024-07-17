import {defineStore} from "pinia";
import {
    abstractStoreFactory,
    abstractStoreFactoryGetters,
    abstractStoreFactoryState,
    BaseEntity
} from "./abstractStoreFactory.ts";

export interface Input extends BaseEntity {
    macro: string
    macro_value: string
    description: string

    default_type: string
    default: string
}


export const useInputStore = defineStore({
    id: 'input',
    state: () => ({
        ...abstractStoreFactoryState<Input>()
    }),
    getters: {
        ...abstractStoreFactoryGetters<Input>()
    },
    actions: {
        ...abstractStoreFactory<Input>('input')
    }
})