import {BaseEventSchema, Column} from "./base.ts";
import {ComponentContextType} from "./navigation.ts";
import {InputSchema} from "./input.ts";


export interface RenderReferenceEvent extends BaseEventSchema {
    eventType: 'render-reference',

    name: string
    overlay: 'set' | 'overlapping' | 'popup' | 'close'
    inputSchema?: InputSchema
}

export interface CloseReferencePopupEvent extends BaseEventSchema {
    eventType: 'close-popup-reference'
}

/**
 * Set context for last reference in navigation
 */
export interface SetReferenceContextEvent extends BaseEventSchema {
    eventType: 'set-reference-context',

    keySuffix?: string
    value: ComponentContextType
}

/**
 * Set key value in context
 */
export interface ChangeContextEvent extends BaseEventSchema {
    eventType: 'change-context',

    contextKey: string
    value: ComponentContextType
}


export interface SaveItemEvent extends BaseEventSchema {
    eventType: 'save-item',
    table?: string,
}

export interface RequestProjectEvent extends BaseEventSchema {
    eventType: 'request-project'
    method: 'get' | 'post'
    url: string,
    data?: ComponentContextType
}

export interface ListRowClickEvent extends BaseEventSchema {
    eventType: 'list-row-click',

    row: {
        column: Column,
        value: any
    }[]
}


export interface DeleteItemEvent extends BaseEventSchema {
    eventType: 'delete-item'
    name: string
}

export interface ApprovedDeleteItemEvent extends BaseEventSchema {
    eventType: 'approved-delete-item'
}


export type EventSchema =
    | RenderReferenceEvent
    | CloseReferencePopupEvent
    | SetReferenceContextEvent
    | ChangeContextEvent
    | SaveItemEvent
    | RequestProjectEvent
    | ListRowClickEvent
    | DeleteItemEvent
    | ApprovedDeleteItemEvent
