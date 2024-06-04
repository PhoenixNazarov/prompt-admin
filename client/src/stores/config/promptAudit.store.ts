import {defineStore} from "pinia";
import {BaseEntity} from "./abstractStoreFactory.ts";
import {Prompt} from "../prompt.store.ts";
import {ApiService} from "../../api/ApiService.ts";

export interface PromptAudit extends BaseEntity {
    mapping_id: number
    table: string
    field: string
    prompt_id?: number
    value: string
    name?: string
    account_id?: number
}


const key = (prompt: Prompt) => prompt.mapping_id + prompt.table + prompt.field + prompt.id

export const usePromptAuditStore = defineStore({
    id: 'promptAudit',
    state: () => ({
        entity: new Map<string, PromptAudit[]>()
    }),
    getters: {
        getByPrompt: state => {
            return (prompt: Prompt) => state.entity.get(key(prompt))
        }
    },
    actions: {
        async loadForPrompt(prompt: Prompt) {
            const res = this.entity.get(key(prompt))
            if (res) return res
            const out = await ApiService.post<PromptAudit[]>('/api/config/prompt_audit/get', prompt)
            this.entity.set(key(prompt), out)
            return out
        }
    }
})