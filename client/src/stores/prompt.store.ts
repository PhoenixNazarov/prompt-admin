import {defineStore} from "pinia";
import {ApiService} from "../api/ApiService.ts";
import {PromptAudit} from "./config/promptAudit.store.ts";
import {SyncData} from "./config/syncData.store.ts";
import {UnitTest} from "./config/unitTest.store.ts";
import {randomString} from "../views/Utils.ts";

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
    originValue: string
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
        executeData?: PromptExecute,
        executeStream?: string
    }

    unitTestData?: {
        unitTest: UnitTest
    }

    templateData?: {
        key: string,
        project: string
    }

    validate?: {
        errors: JinjaError[]
    }
}


interface ValidationResponse {
    j2lint?: {
        ERRORS: JinjaError[]
    }
}

export interface JinjaError {
    message: string,
    line_number: number,
    severity: string
}


export const usePromptStore = defineStore({
    id: 'prompt',
    state: () => ({
        prompts: [] as Prompt[],
        loadings: {
            loadAll: undefined as undefined | Promise<Prompt[]>,
            connectionsLoadAll: false
        },
        connections: [] as string[],
        executionStream: new Map<string, Prompt>
    }),
    getters: {
        promptsByMapping: state => {
            return (mappingId: number) => state.prompts.filter(p => p.mapping_id == mappingId)
        },
        promptByMappingName: state => {
            return (mappingId: number, name: string) => state.prompts.find(p => p.mapping_id == mappingId && p.name == name)
        }
    },
    actions: {
        async loadAll() {
            if (this.loadings.loadAll) return await this.loadings.loadAll
            this.loadings.loadAll = ApiService.get<Prompt[]>('/api/prompts/load_all')
            this.prompts = await this.loadings.loadAll
            this.prompts.forEach(p => p.originValue = p.value)
            this.loadings.loadAll = undefined
            return this.prompts
        },
        async savePrompt(prompt: Prompt) {
            await ApiService.post('/api/prompts/save', prompt)
            prompt.originValue = prompt.value
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
            const uuid = randomString(20)
            this.executionStream.set(uuid, prompt)
            prompt.previewData.executeStream = undefined
            prompt.previewData.executeData = undefined
            prompt.previewData.executeData = await ApiService.post<PromptExecute>('/api/prompts/execute', {
                service_model_info: JSON.parse(syncData.service_model_info),
                history: JSON.parse(syncData.history_context_default),
                prompt: prompt.previewData.value,
                parsed_model_type: syncData.parsed_model_type ? JSON.parse(syncData.parsed_model_type) : undefined,
                uuid: uuid
            })
        },
        executeStream(uuid: string, text: string) {
            const prompt = this.executionStream.get(uuid)
            if (!prompt || !prompt.previewData) return
            if (!prompt.previewData.executeStream) {
                prompt.previewData.executeStream = text
            } else {
                prompt.previewData.executeStream += text
            }
        },
        async connectionsLoadAll() {
            if (this.connections.length > 0) return
            this.loadings.connectionsLoadAll = true
            const result = await ApiService.get<string[]>('/api/prompts/connections/get_all')
            this.loadings.connectionsLoadAll = false
            this.connections = result
        },
        async validate(prompt: Prompt) {
            const result = await ApiService.post<ValidationResponse>('/api/prompts/validate', {prompt: prompt.value})
            if (result.j2lint) prompt.validate = {errors: result.j2lint.ERRORS}
        }
    }
})