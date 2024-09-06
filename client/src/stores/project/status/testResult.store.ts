import {defineStore} from "pinia";
import {abstractStoreFactoryGetters, abstractStoreFactoryState, BaseEntity} from "../../config/abstractStoreFactory.ts";
import {ApiService} from "../../../api/ApiService.ts";


export interface TestResult extends BaseEntity {
    created: number
    duration: number

    passed: number
    skipped: number
    error: number
    failed: number
    total: number
    collected: number
}


export const useTestResultStore = defineStore({
    id: 'testResult',
    state: () => ({
        ...abstractStoreFactoryState<TestResult>(),
        loaded: false,
        loading: {
            load30: false
        }
    }),
    getters: {
        ...abstractStoreFactoryGetters<TestResult>(),
    },
    actions: {
        async load30Project(project: string) {
            if (this.loaded) return this.entity
            this.loading.load30 = true
            this.entity = await ApiService.get<TestResult[]>(`/api/project/status/test_result/load_30/${project}`)
            this.loading.load30 = false
            return this.entity
        }
    }
})