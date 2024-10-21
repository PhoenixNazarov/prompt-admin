import {Prompt, usePromptStore} from "../../../stores/prompt.store.ts";
import {Mapping, useMappingStore} from "../../../stores/config/mapping.store.ts";
import {chunk, hashCode, randomString} from "../../Utils.ts";
import {useVarsStore} from "../../../stores/vars.store.ts";
import {useMappingEntityStore} from "../../../stores/config/mappingEntity.store.ts";
import {reactive} from 'vue'

interface BaseItem {
    type: 'group' | 'prompt' | 'button' | 'promise' | 'element'
    name: string | undefined
    tab: number
    tags: string[]
}

interface GroupItem extends BaseItem {
    type: 'group'
    tag?: string
    preIcon?: 'diagram-project' | 'table' | 'table-columns' | 'eye-slash' | 'file' | 'plus'
    caret: boolean

    meta?: string
    metaData?: any
}

interface PromptItem extends BaseItem {
    type: 'prompt'
    prompt: Prompt
}

interface PromiseItem extends BaseItem {
    type: 'promise'
    promise: () => Promise<ListItem[]>
    ident: string
}

export type ListItem = GroupItem | PromptItem | PromiseItem


const DEL = '|'

export const ITEMS: ListItem[] = reactive([])

const addTag = (tag: string, currentTag: string, tags: string[]): [string, string[]] => {
    currentTag += currentTag != '' ? `${DEL}${tag}` : tag
    const ntags = [...tags]
    ntags.push(currentTag)
    return [currentTag, ntags]
}
const removeTag = (tag: string, currentTag: string, tags: string[]): [string, string[]] => {
    const index = tags.indexOf(currentTag)
    if (index > -1) {
        tags.splice(index, 1)
    }
    if (currentTag.substring(currentTag.length - tag.length, currentTag.length)) {
        currentTag = currentTag.substring(0, currentTag.length - tag.length)
    }
    if (currentTag[currentTag.length - 1] == DEL) {
        currentTag = currentTag.substring(0, currentTag.length - 1)
    }
    return [currentTag, tags]
}


export class ListItemBuilder {
    async build() {
        ITEMS.push({
            type: 'promise',
            name: 'Loading projects',
            tab: 0,
            tags: [],
            ident: randomString(),
            promise: this.buildProjects
        })
        const results = await this.buildProjects()
        ITEMS.splice(0, ITEMS.length, ...results)
        while (true) {
            const promises = ITEMS.filter(el => el.type == 'promise') as PromiseItem[]
            if (promises.length <= 0) {
                break
            }

            for (let els of chunk(promises, 2)) {
                await Promise.all(els.map(el => this.promiseItemResolve(el)))
            }
        }
    }

    async promiseItemResolve(promiseItem: PromiseItem) {
        const resultItems = await promiseItem.promise()
        const indexItem = ITEMS.findIndex(el => el.type == 'promise' && el.ident == promiseItem.ident)
        if (indexItem <= -1) {
            return
        }
        ITEMS.splice(indexItem, 1, ...resultItems.map(el => {
            el.tags = [...promiseItem.tags, ...el.tags];
            el.tab = el.tab + promiseItem.tab
            return el
        }))
    }

    async buildProjects(): Promise<ListItem[]> {
        const mappingStore = useMappingStore()
        const promptStore = usePromptStore()
        await mappingStore.loadAll()

        const result: ListItem[] = []
        for (let [connection, mappingsTable] of mappingStore.getConnections) {
            if (!promptStore.connections.includes(connection)) continue
            let [currentTag, tags] = addTag(connection, '', [])
            result.push({
                type: 'group',
                name: connection,
                preIcon: 'diagram-project',
                tab: 0,
                tag: currentTag,
                tags: [],
                caret: true
            })

            result.push({
                type: 'promise',
                name: 'Loading templates',
                tab: 1,
                tags: tags,
                ident: randomString(),
                promise: () => this.buildTemplate(currentTag, connection)
            })

            for (let [mappingTableName, mappings] of mappingsTable) {
                result.push({
                    type: 'promise',
                    name: 'Loading Mappings',
                    tab: 1,
                    tags: tags,
                    ident: randomString(),
                    promise: () => this.buildMapping(currentTag, mappingTableName, mappings)
                })
            }
        }

        return result
    }

    async buildTemplate(currentTag_: string, connection: string): Promise<ListItem[]> {
        const [currentTag, tags] = addTag('template', currentTag_, [])
        const result: ListItem[] = []
        result.push({
            type: 'group',
            name: 'Templates',
            preIcon: 'file',
            tab: 0,
            tag: currentTag,
            tags: [],
            caret: true
        })
        result.push({
            type: 'group',
            name: 'Create',
            preIcon: 'plus',
            tab: 1,
            tags: tags,
            caret: false,
            meta: 'create-template',
            metaData: {
                project: connection
            }
        })
        result.push({
            type: 'promise',
            name: 'Templates',
            tags: tags,
            tab: 1,
            ident: randomString(20),
            promise: async () => {
                const varsStore = useVarsStore()
                await varsStore.load(connection)
                const newResult: ListItem[] = []
                for (let template of varsStore.getTemplateByProject(connection)) {
                    newResult.push({
                        type: 'group',
                        name: template.key,
                        caret: false,
                        tab: 0,
                        tags: [],
                        meta: 'template',
                        metaData: {
                            value: template.value,
                            key: template.key,
                            project: connection
                        }
                    })
                }
                return newResult
            }
        })
        return result
    }

    async buildMapping(currentTag_: string, mappingTableName: string, mappings: Mapping[]): Promise<ListItem[]> {
        const [currentTag, tags] = addTag(mappingTableName, currentTag_, [])
        const result: ListItem[] = []
        result.push({
            type: 'group',
            name: mappingTableName,
            preIcon: 'table',
            tab: 0,
            tag: currentTag,
            tags: [],
            caret: true
        })
        for (let mapping of mappings) {
            if (mapping.id) {
                result.push({
                    type: 'promise',
                    name: 'Loading prompts',
                    tab: 1,
                    tags: tags,
                    ident: randomString(),
                    promise: () => this.buildFieldPrompts(currentTag_, mapping)
                })
            }
        }
        return result
    }

    sortPrompts(mapping: Mapping, prompts: Prompt[]) {
        if (!mapping.field_order) {
            return prompts.sort((a, b) => {
                return hashCode(a.name) - hashCode(b.name)
            })
        }
        return prompts.sort((a, b) => {
            if (mapping.desc) {
                return hashCode(b.sort_value) - hashCode(a.sort_value)
            } else {
                return hashCode(a.sort_value) - hashCode(b.sort_value)
            }
        })
    }

    isDisable(mapping: Mapping, prompt: Prompt) {
        const mappingEntityStore = useMappingEntityStore()
        return mappingEntityStore.entity.find(
            el =>
                el.connection_name == mapping.connection_name &&
                el.table == mapping.table &&
                el.field == mapping.field &&
                el.name == prompt.name &&
                el.entity == 'disable'
        )
    }

    async buildFieldPrompts(currentTag_: string, mapping: Mapping): Promise<ListItem[]> {
        if (mapping.id == undefined) {
            return []
        }
        const [currentTag, tags] = addTag(mapping.field + mapping.id, currentTag_, [])
        const result: ListItem[] = []
        const promptStore = usePromptStore()
        if (promptStore.prompts.length == 0) {
            await promptStore.loadAll()
        }
        const prompts = this.sortPrompts(mapping, promptStore.promptsByMapping(mapping.id))
        result.push({
            type: 'group',
            name: mapping.field,
            preIcon: 'table-columns',
            tab: 0,
            tag: currentTag,
            tags: [],
            caret: prompts.length > 0
        })
        const activePrompt: Prompt[] = []
        const disablePrompt: Prompt[] = []
        prompts.forEach(prompt => {
            if (this.isDisable(mapping, prompt)) {
                disablePrompt.push(prompt)
            } else {
                activePrompt.push(prompt)
            }
        })
        if (disablePrompt.length > 0) {
            const [currentTag1, tags1] = addTag('disable', currentTag, tags)
            result.push({
                type: 'group',
                name: 'Disabled',
                preIcon: 'eye-slash',
                tab: 1,
                tag: currentTag1,
                tags: tags,
                caret: true
            })
            for (let prompt of disablePrompt) {
                result.push({
                    type: 'prompt',
                    name: prompt.name,
                    tab: 2,
                    prompt: prompt,
                    tags: tags1
                })
            }
        }

        for (let prompt of activePrompt) {
            result.push({
                type: 'prompt',
                name: prompt.name,
                tab: 1,
                prompt: prompt,
                tags: tags
            })
        }

        return result
    }
}