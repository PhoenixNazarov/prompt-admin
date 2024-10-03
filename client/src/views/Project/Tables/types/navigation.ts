import {BaseComponentSchema} from "./base.ts";
import {GroupSchema} from "./group.ts";


export type ComponentContextType = ComponentContextDict | ComponentContextValueType
export type ComponentContextDict = { [key: string]: ComponentContextType }
export type ComponentContextValueType = number | string | undefined | boolean


export interface ComponentContextSchema {
    componentContext: ComponentContextType
}

export interface ReferenceGroupSchema extends BaseComponentSchema {
    type: 'reference-window'
    mainRefName?: string
    refs: NamedGroup[]
}

export interface NamedGroup {
    name: string
    group: GroupSchema
}

export type NavigationSchema = ReferenceGroupSchema