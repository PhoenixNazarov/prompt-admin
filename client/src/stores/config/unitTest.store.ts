import {defineStore} from "pinia";
import {
    abstractStoreFactory,
    abstractStoreFactoryGetters,
    abstractStoreFactoryState,
    BaseEntity
} from "./abstractStoreFactory.ts";

export interface UnitTest extends BaseEntity {
    sync_data_id: number
    name: string

    test_status: string
    test_preview?: string
    test_response_model?: string
    test_exception?: string
}


export const useUnitTestStore = defineStore({
    id: 'unitTest',
    state: () => ({
        ...abstractStoreFactoryState<UnitTest>()
    }),
    getters: {
        ...abstractStoreFactoryGetters<UnitTest>(),
        getBySyncDataName: state => {
            return (syncDataId: number, name: string) => state.entity.find(el => el.sync_data_id == syncDataId && el.name == name)
        },
    },
    actions: {
        ...abstractStoreFactory<UnitTest>('unit_test'),
    }
})