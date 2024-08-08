import {defineStore} from "pinia";
import {
    abstractStoreFactory,
    abstractStoreFactoryGetters,
    abstractStoreFactoryState,
    BaseEntity
} from "./abstractStoreFactory.ts";
import {ApiService} from "../../api/ApiService.ts";

export interface SyncData extends BaseEntity {
    service_model_info: string
    template_context_type: string
    template_context_default: string
    history_context_default: string
    parsed_model_type?: string
    parsed_model_default?: string
    fail_parse_model_strategy?: string

    parsed_model_default_xml?: string
}


export const useSyncDataStore = defineStore({
    id: 'syncData',
    state: () => ({
        ...abstractStoreFactoryState<SyncData>()
    }),
    getters: {
        ...abstractStoreFactoryGetters<SyncData>()
    },
    actions: {
        ...abstractStoreFactory<SyncData>('sync_data'),
        async loadXmlParsedModelDefault(syncData: SyncData | undefined) {
            if (!syncData?.parsed_model_default) return
            syncData.parsed_model_default_xml = await ApiService.post<string>('/api/config/sync_data/convert/xml', {obj: JSON.parse(syncData.parsed_model_default)})
        }
    }
})