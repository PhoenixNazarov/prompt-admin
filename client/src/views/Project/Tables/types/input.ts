import {BaseInputSchema, Column} from "./base.ts";

export interface ItemInputSchema extends BaseInputSchema {
    inputType: 'item'
    id: number
    table?: string | undefined
}

export interface CreateItemInputSchema extends BaseInputSchema {
    inputType: 'create-item'
    table?: string | undefined
}

// Deprecated
export interface SelectInputSchema extends BaseInputSchema {
    inputType: 'select'
    reference: string

    targetColumn?: Column
}

export interface ListRowClickInputSchema extends BaseInputSchema {
    inputType: 'list-row-click'
}

export interface DeleteItemInputSchema extends BaseInputSchema {
    inputType: 'delete-item'

    table: string
    id: number
    closeReferenceAfter?: boolean
}

export interface ParametersListInput extends BaseInputSchema {
    inputType: 'parameters-list'
    page?: number
    itemsPerPage?: number

    sortBy?: { key: string, order: 'ask' | 'desc' }[]
    filters?: { key?: string, value?: string | number | boolean, operator?: string }[]
    additionalHeaders?: { title: string, key: string, sortable: boolean }[]
}

export interface HistoryInput extends BaseInputSchema {
    inputType: 'history'
    history: { name: string, input?: InputSchema }[]
}


export type InputSchema =
    | ItemInputSchema
    | SelectInputSchema
    | ListRowClickInputSchema
    | CreateItemInputSchema
    | DeleteItemInputSchema
    | ParametersListInput
    | HistoryInput
