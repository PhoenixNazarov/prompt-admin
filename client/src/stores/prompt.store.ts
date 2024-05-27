import {defineStore} from "pinia";
import axios from 'axios'

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
            const out = await axios.get<Prompt[]>(
                '/api/prompts/load_all'
            )
            this.prompts = out.data
        }
    }
})