import {BaseComponentSchema, Column} from "./base.ts";
import {ButtonSchema} from "./button.ts";
import {ListSchema} from "./group.ts";
import {ComponentContextValueType} from "./navigation.ts";


export interface TextSchema extends BaseComponentSchema {
    type: 'text'

    label: string
    text: string

    typography?: 'text-h4' | 'text-h5' | 'text-subtitle-1' | 'text-subtitle-2'
    textCenter?: boolean
    bold?: boolean
}


export interface BaseElementComponentSchema extends BaseComponentSchema {
    disabled?: boolean
}

export interface DataElementComponentSchema extends BaseElementComponentSchema {
    label: string
    reference: string
    hint?: string
    persistentHint?: boolean
    hideDetails?: boolean
    nullable?: boolean
    default?: ComponentContextValueType

    popup?: {
        listSchema: ListSchema,
        targetColumn: Column
    }
}

export interface TextFieldSchema extends DataElementComponentSchema {
    type: 'textField'

    format?: 'text' | 'number'
}

export interface TextAreaSchema extends DataElementComponentSchema {
    type: 'textArea'

    rows?: number
}

export interface CheckboxSchema extends DataElementComponentSchema {
    type: 'checkbox'
}

export interface ItemRowSchema extends DataElementComponentSchema {
    type: 'item-row'

    table: string
    columns: Column[]
}

export interface SelectSchema extends DataElementComponentSchema {
    type: 'select'

    items: string[]
}

export interface ImageSchema extends DataElementComponentSchema {
    type: 'image'

    size: 's' | 'm' | 'l'
}

export interface DateSchema extends DataElementComponentSchema {
    type: 'date'
}


export type ElementSchema =
    | ButtonSchema
    | TextSchema
    | TextFieldSchema
    | TextAreaSchema
    | CheckboxSchema
    | ItemRowSchema
    | SelectSchema
    | ImageSchema
    | DateSchema
