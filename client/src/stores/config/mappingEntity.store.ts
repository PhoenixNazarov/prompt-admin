import {defineStore} from "pinia";
import {abstractStoreFactory, abstractStoreFactoryState, BaseEntity} from "./abstractStoreFactory.ts";
import {useMacroStore} from "./macro.store.ts";
import {Mapping} from "./mapping.store.ts";
import {Prompt} from "../prompt.store.ts";
import {useOutputStore} from "./output.store.ts";
import {useInputStore} from "./input.store.ts";

export interface MappingEntity extends BaseEntity {
    connection_name?: string
    table?: string
    field?: string
    name?: string
    mapping_id?: number
    entity: string
    entity_id: number
}


function getByFilter(state, connectionName: string, table: string, field: string, nameE: string | undefined, mappingId: number, entity: string): MappingEntity[] {
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
        }
    },
    actions: {
        ...abstractStoreFactory('mapping_entity')
    }
})