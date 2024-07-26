import {defineStore} from "pinia";
import {
    abstractStoreFactory,
    abstractStoreFactoryGetters,
    abstractStoreFactoryState,
    BaseEntity
} from "./abstractStoreFactory.ts";
import {useMacroStore} from "./macro.store.ts";
import {Mapping, useMappingStore} from "./mapping.store.ts";
import {Prompt, usePromptStore} from "../prompt.store.ts";
import {useOutputStore} from "./output.store.ts";
import {useInputStore} from "./input.store.ts";
import {useSyncDataStore} from "./syncData.store.ts";

export interface MappingEntity extends BaseEntity {
    connection_name?: string
    table?: string
    field?: string
    name?: string
    mapping_id?: number
    entity: string
    entity_id: number
}


function getByFilter(state, connectionName: string, table: string, field: string, nameE: string | undefined, mappingId: number | undefined, entity: string): MappingEntity[] {
    return state.entity.filter(
        e =>
            (e.connection_name == undefined || e.connection_name == connectionName) &&
            (e.table == undefined || e.table == table) &&
            (e.field == undefined || e.field == field) &&
            (e.name == undefined || e.name == nameE) &&
            (e.mapping_id == undefined || e.mapping_id == mappingId) &&
            (e.entity == entity)
    )
}

export const useMappingEntityStore = defineStore({
    id: 'mappingEntity',
    state: () => ({
        ...abstractStoreFactoryState<MappingEntity>()
    }),
    getters: {
        ...abstractStoreFactoryGetters<MappingEntity>(),
        getInputsByFilter: state => {
            return (mapping: Mapping, prompt: Prompt) => {
                const supportEntity = getByFilter(state, mapping.connection_name, mapping.table, mapping.field, prompt.name, mapping.id, 'input')
                const macroStore = useInputStore()
                return macroStore.getByIds(supportEntity.map(se => se.entity_id))
            }
        },
        getOutputByFilter: state => {
            return (mapping: Mapping, prompt: Prompt) => {
                const supportEntity = getByFilter(state, mapping.connection_name, mapping.table, mapping.field, prompt.name, mapping.id, 'output')
                const outputStore = useOutputStore()
                if (supportEntity.length <= 0) return
                return outputStore.getById(supportEntity[0].entity_id)
            }
        },
        getMacroByFilter: state => {
            return (mapping: Mapping, prompt: Prompt) => {
                const supportEntity = getByFilter(state, mapping.connection_name, mapping.table, mapping.field, prompt.name, mapping.id, 'macro')
                const macroStore = useMacroStore()
                return macroStore.getByIds(supportEntity.map(se => se.entity_id))
            }
        },
        getSyncDataByFilter: state => {
            return (mapping: Mapping, prompt: Prompt) => {
                const supportEntity = getByFilter(state, mapping.connection_name, mapping.table, mapping.field, prompt.name, mapping.id, 'sync_data')
                const syncDataStore = useSyncDataStore()
                if (supportEntity.length <= 0) return
                return syncDataStore.getById(supportEntity[0].entity_id)
            }
        },
        getPromptsByMappingEntity: _ => {
            return (mappingEntity: MappingEntity) => {
                const promptStore = usePromptStore()
                const mappingStore = useMappingStore()
                return promptStore.prompts.filter(
                    e => {
                        const mapping = mappingStore.getById(e.mapping_id)
                        if (!mapping) return false
                        return (mappingEntity.connection_name == undefined || mappingEntity.connection_name == mapping.connection_name) &&
                            (mappingEntity.table == undefined || mappingEntity.table == e.table) &&
                            (mappingEntity.field == undefined || mappingEntity.field == e.field) &&
                            (mappingEntity.name == undefined || mappingEntity.name == e.name) &&
                            (mappingEntity.mapping_id == undefined || mappingEntity.mapping_id == mapping.id)
                    }
                )
            }
        },
        getMappingEntityByEntity: state => {
            return (entity: string, entityId: number | undefined) => {
                if (entityId == undefined) return []
                return state.entity.filter(e => e.entity == entity && e.entity_id == entityId)
            }
        },
        getMappingEntityByMapping: state => {
            return (connectionName: string | undefined, table: string | undefined, field: string | undefined) => {
                return state.entity.filter(
                    e =>
                        (e.connection_name == undefined || e.connection_name == connectionName) &&
                        (e.table == undefined || e.table == table) &&
                        (e.field == undefined || e.field == field)
                )
            }
        }
    },
    actions: {
        ...abstractStoreFactory<MappingEntity>('mapping_entity')
    }
})