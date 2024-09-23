import {BaseElementComponentSchema} from "./element.ts";
import {
    ApprovedDeleteItemEvent, CloseReferencePopupEvent,
    DeleteItemEvent,
    RenderReferenceEvent,
    RequestProjectEvent,
    SaveItemEvent
} from "./event.ts";


export interface ButtonSchema extends BaseElementComponentSchema {
    type: 'button'
    text: string,
    color?: string

    event: RenderReferenceEvent
        | SaveItemEvent
        | RequestProjectEvent
        | DeleteItemEvent
        | ApprovedDeleteItemEvent
        | CloseReferencePopupEvent
}