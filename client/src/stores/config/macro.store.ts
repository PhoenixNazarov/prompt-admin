import {defineStore} from "pinia";
import {
    abstractStoreFactory,
    abstractStoreFactoryGetters,
    abstractStoreFactoryState,
    BaseEntity
} from "./abstractStoreFactory.ts";

export interface Macro extends BaseEntity {
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
        ...abstractStoreFactoryGetters<Macro>(),
    },
    actions: {
        ...abstractStoreFactory<Macro>('macro')
    }
})