import {defineStore} from "pinia";
import {ApiService} from "../api/ApiService.ts";

export interface Prompt {
    mapping_id: number
    table: string
    field: string
    id: number
    value: string
    name?: string
    preview?: boolean
}


export const usePromptStore = defineStore({
    id: 'prompt',
    state: () => ({
        prompts: [] as Prompt[]
    }),
    getters: {
        promptsByMapping: state => {
            return (mappingId: number) => state.prompts.filter(p => p.mapping_id == mappingId)
        }
    },
    actions: {
        async loadAll() {
            this.prompts = await ApiService.get<Prompt[]>('/api/prompts/load_all')
        },
        async savePrompt(prompt: Prompt) {
            await ApiService.post('/api/prompts/save', prompt)
        },
        async previewPrompt(prompt: Prompt) {
            const result = await ApiService.post<string>('/api/prompts/preview', prompt)
            const previewPrompt = {...prompt}
            previewPrompt.value = result
            previewPrompt.preview = true
            return previewPrompt
        }
    }
})