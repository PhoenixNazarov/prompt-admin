import {defineStore} from "pinia";
import {ApiService} from "../api/ApiService.ts";
import {PromptAudit} from "./config/promptAudit.store.ts";
import {SyncData} from "./config/syncData.store.ts";
import {UnitTest} from "./config/unitTest.store.ts";

export interface PromptExecuteAnthropic {
    origin_message: object
    raw_text: string
    parsed_model?: string
}

export interface PromptExecute {
    response_model: PromptExecuteAnthropic
    parsed_model_error: boolean
    messages: object
}


export interface Prompt {
    mapping_id: number
    table: string
    field: string
    id: number
    value: string
    name?: string
    preview?: boolean
    sort_value?: any

    auditData?: {
        audit: PromptAudit,
        prevAudit?: PromptAudit
    }

    previewData?: {
        history: object | undefined
        value: string
        executeData?: PromptExecute
    }

    unitTestData?: {
        unitTest: UnitTest
    }

    templateData?: {
        key: string,
        project: string
    }
}


export const usePromptStore = defineStore({
    id: 'prompt',
    state: () => ({
        prompts: [] as Prompt[],
        loadings: {
            loadAll: false,
            connectionsLoadAll: false
        },
        connections: [] as string[]
    }),
    getters: {
        promptsByMapping: state => {
            return (mappingId: number) => state.prompts.filter(p => p.mapping_id == mappingId)
        }
    },
    actions: {
        async loadAll() {
            this.loadings.loadAll = true
            this.prompts = await ApiService.get<Prompt[]>('/api/prompts/load_all')
            this.loadings.loadAll = false
        },
        async savePrompt(prompt: Prompt) {
            await ApiService.post('/api/prompts/save', prompt)
        },
        async previewPrompt(prompt: Prompt, context: object | undefined = undefined, connection: string | undefined = undefined) {
            const result = await ApiService.post<string>('/api/prompts/preview', {
                prompt: prompt,
                context: context,
                connection: connection
            })
            const previewPrompt = {...prompt}
            previewPrompt.previewData = {value: result, history: undefined}
            return previewPrompt
        },
        async execute(prompt: Prompt, syncData: SyncData) {
            if (!prompt.previewData) return
            prompt.previewData.executeData = await ApiService.post<PromptExecute>('/api/prompts/execute', {
                service_model_info: JSON.parse(syncData.service_model_info),
                history: JSON.parse(syncData.history_context_default),
                prompt: prompt.previewData.value,
                parsed_model_type: syncData.parsed_model_type ? JSON.parse(syncData.parsed_model_type) : undefined
            })
        },
        async connectionsLoadAll() {
            if (this.connections.length > 0) return
            this.loadings.connectionsLoadAll = true
            const result = await ApiService.get<string[]>('/api/prompts/connections/get_all')
            this.loadings.connectionsLoadAll = false
            this.connections = result
        }
    }
})