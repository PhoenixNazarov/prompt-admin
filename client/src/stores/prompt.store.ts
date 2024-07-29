import {defineStore} from "pinia";
import {ApiService} from "../api/ApiService.ts";
import {PromptAudit} from "./config/promptAudit.store.ts";

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

    llmData?: {
        response: string
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
        async previewPrompt(prompt: Prompt, context: object | undefined = undefined) {
            const result = await ApiService.post<string>('/api/prompts/preview', {prompt: prompt, context: context})
            const previewPrompt = {...prompt}
            previewPrompt.value = result
            previewPrompt.preview = true
            return previewPrompt
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