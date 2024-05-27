import {defineStore} from "pinia";
import {ApiService} from "../api/ApiService.ts";

export interface Prompt {
    mapping_id: number
    table: string
    field: string
    id: number
    value: string
    name?: string
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
            this.prompts = await ApiService.post('/api/prompts/save', prompt)
        }
    }
})