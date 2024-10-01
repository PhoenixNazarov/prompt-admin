import {BaseComponentSchema, Column} from "./base.ts";
import {GroupElementSchema} from "./index.ts";


export interface RowSchema extends BaseComponentSchema {
    type: 'row'

    wrapInColumn?: boolean
    components: GroupElementSchema[]
}

export interface ColumnSchema extends BaseComponentSchema {
    type: 'column'

    components: GroupElementSchema[]

    rowReverse?: boolean
}

export interface CardSchema extends BaseComponentSchema {
    type: 'card'
    title: string

    components: GroupElementSchema[]

    table?: string
    reference?: string
}

export interface Filter {
    key: string
    value: string | number | boolean | undefined
    operator: '=' | '!=' | '>' | '>=' | '<' | '<=' | 'like%' | '%like' | '%like%' | 'is'
}

export interface ListSchema extends BaseComponentSchema {
    type: 'list'

    title: string
    table: string
    columns: Column[]

    filter?: {
        columns?: {
            key: string
            like?: boolean
        }[] // DEPRECATED
        startFilters?: Filter[]
        hideFilterField?: boolean
    }

    joins?: {
        table: string
        pseudo?: string
        condition: string
    }[]

    hideBottom?: boolean
    border?: boolean
    itemsPerPage?: number
    editElementName?: string
    createElementName?: string
    deleteElementName?: string

    fetchColumn?: {
        filter?: boolean                // Default True
        headers?: boolean              // Default True
    }
}


export type GroupSchema =
    | RowSchema
    | ColumnSchema
    | CardSchema
    | ListSchema
