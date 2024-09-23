export interface BaseComponentSchema {
// ===== Navigation     =====
    type:
        | 'reference-window'
//  ===== Groups        =====
        | 'row'
        | 'column'
        | 'card'
        | 'list'
        // | 'group-element'
//  ===== Elements      =====
        | 'text'
        | 'textField'
        | 'textArea'
        | 'date-picker'
        | 'checkbox'
        // | 'popup'
        | 'button'
        | 'item-row'
        | 'select'
        | 'image'
}

export interface BaseEventSchema {
    eventType:
        | 'render-reference'
        | 'close-popup-reference'
        | 'set-reference-context'
        | 'change-context'
        | 'request-project'
        | 'list-row-click'
        | 'save-item'
        | 'delete-item'
        | 'approved-delete-item'

    original?: string
}

export interface BaseInputSchema {
    inputType:
        | 'item'
        | 'select'
        | 'list-row-click'
        | 'create-item'
        | 'delete-item'
}

export interface Column {
    title: string
    column: string

    display?: 'text' | 'image'
    imageSize?: 's' | 'm' | 'l'
    ident?: {
        name: string,
        table?: string
    }
}
