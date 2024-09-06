import {defineStore} from "pinia";
import {BaseEntity} from "../../config/abstractStoreFactory.ts";
import {ApiService} from "../../../api/ApiService.ts";


export interface TestCase extends BaseEntity {
    test_result_id: number

    nodeid: string
    lineno: number
    outcome: string

    metadata_url: string
    metadata_scenario?: string

    setup_duration: number
    setup_outcome: string

    call_duration?: number
    call_outcome?: string

    teardown_duration: number
    teardown_outcome: string
}


export const useTestCaseStore = defineStore({
    id: 'testCase',
    state: () => ({
        entity: new Map<number, TestCase[]>,
        loaded: new Map<number, boolean>,
    }),
    getters: {
        getByTestResultId: state => {
            return (id: number) => {
                const alreadyTestCases = state.entity.get(id)
                if (alreadyTestCases) {
                    return alreadyTestCases.sort(function compare(a, b) {
                        if (a.metadata_url === b.metadata_url) {
                            return 0
                        }
                        if (a.metadata_url == null) return 1
                        if (b.metadata_url == null) return -1
                        return a.metadata_url < b.metadata_url ? -1 : 1;
                    })
                }
                return []
            }
        },
    },
    actions: {
        async loadTestResult(id: number) {
            const alreadyTestCases = this.entity.get(id)
            if (alreadyTestCases) return alreadyTestCases
            this.loaded.set(id, true)
            const testCases = await ApiService.get<TestCase[]>(`/api/project/status/test_case/load/test_result/${id}`)
            this.entity.set(id, testCases)
            this.loaded.set(id, false)
            return testCases
        }
    }
})