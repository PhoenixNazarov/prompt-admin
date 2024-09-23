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

export type InputSchema =
    | ItemInputSchema
    | SelectInputSchema
    | ListRowClickInputSchema
    | CreateItemInputSchema
    | DeleteItemInputSchema
