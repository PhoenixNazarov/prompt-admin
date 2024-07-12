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
        entity: new Map<string, PromptAudit[]>(),
        entityCount: new Map<string, number>()
    }),
    getters: {
        getByPrompt: state => {
            return (prompt: Prompt) => state.entity.get(key(prompt))?.sort((a, b) => a.id - b.id)
        },
        getByPromptCount: state => {
            return (prompt: Prompt) => state.entityCount.get(key(prompt))
        },
    },
    actions: {
        async loadForPrompt(prompt: Prompt, itemPerPage: number, page: number) {
            return await Promise.all([
                this.loadForPromptFind(prompt, itemPerPage, page),
                this.loadForPromptCount(prompt),
            ])
        },
        async loadForPromptFind(prompt: Prompt, itemPerPage: number, page: number) {
            const out = await ApiService.post<PromptAudit[]>('/api/config/prompt_audit/get', {
                item_per_page: itemPerPage,
                page: page,
                prompt: prompt
            })
            let prompts = this.entity.get(key(prompt))
            prompts ? prompts.push(...out.filter(p => prompts?.find(p2 => p2.id == p.id) == undefined)) : prompts = out
            this.entity.set(key(prompt), prompts.sort((a, b) => a.id - b.id))
            return out
        },
        async loadForPromptCount(prompt: Prompt): Promise<number> {
            const count = await ApiService.post<number>('/api/config/prompt_audit/get/count', {
                item_per_page: 2000,
                page: 0,
                prompt: prompt
            })
            this.entityCount.set(key(prompt), count)
            return count
        }
    }
})