import {defineStore} from "pinia";
import {BaseEntity} from "../../config/abstractStoreFactory.ts";
import {ApiService} from "../../../api/ApiService.ts";


export interface TestCaseInfo extends BaseEntity {
    test_case_id: number

    setup_longrepr?: string

    call_crash_path?: string
    call_crash_lineno?: number
    call_crash_message: string

    request?: string
    response?: string
}


export const useTestCaseInfoStore = defineStore({
    id: 'testCaseInfo',
    state: () => ({
        entity: new Map<number, TestCaseInfo>,
        loaded: new Map<number, boolean>,
    }),
    getters: {},
    actions: {
        async loadTestCase(id: number) {
            const alreadyTestCaseInfo = this.entity.get(id)
            if (alreadyTestCaseInfo) return alreadyTestCaseInfo
            this.loaded.set(id, true)
            const testCaseInfo = await ApiService.get<TestCaseInfo>(`/api/project/status/test_case_info/load/test_case/${id}`)
            this.entity.set(id, testCaseInfo)
            this.loaded.set(id, false)
            return testCaseInfo
        }
    }
})