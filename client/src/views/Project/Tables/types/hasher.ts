import {InputSchema} from "./input.ts";

export const SEPARATORS = {
    INNER: ':',
    EXTERNAL: '/',
    DOT: ',',
    SP: '(',
    EP: ')'
}

type End = number | string | boolean | undefined | End[]
type EndParsed = string | undefined | EndParsed[]

function compile(obj: End, level = 0): string {
    if (obj == undefined) return ''
    else if (typeof obj == 'number' || typeof obj == 'string')
        return String(obj)
    else if (typeof obj == 'object') {
        const mapped = obj.map(el => compile(el, level + 1)).join(SEPARATORS.DOT)
        if (level == 0) return mapped
        return SEPARATORS.SP + mapped + SEPARATORS.EP
    }
    return ''
}

function decompile(obj: string): EndParsed {
    const result: EndParsed = []
    const stackList = [result]
    let needPushUndefined = true
    let el: string | undefined = undefined
    for (let ind = 0; ind < obj.length; ind++) {
        if (obj[ind] == SEPARATORS.DOT) {
            if (el == undefined && needPushUndefined) {
                stackList[stackList.length - 1].push(el)
            } else if (el) {
                stackList[stackList.length - 1].push(el)
            }
            needPushUndefined = true
            el = undefined
        } else if (obj[ind] == SEPARATORS.SP) {
            stackList.push([])
            el = undefined
            needPushUndefined = true
        } else if (obj[ind] == SEPARATORS.EP) {
            if (el) stackList[stackList.length - 1].push(el)
            const list = stackList.pop()
            stackList[stackList.length - 1].push(list)
            el = undefined
            needPushUndefined = false
        } else {
            el = el ? el + obj[ind] : obj[ind]
            needPushUndefined = true
        }
    }
    return result
}


export function inputToString(input: InputSchema): string {
    let items: End = []
    if (input.inputType == 'item')
        items = ['item', input.id, input.table]
    else if (input.inputType == 'create-item')
        items = ['create-item', input.table]
    else if (input.inputType == 'parameters-list')
        items = [
            'parameters-list',
            input.page,
            input.itemsPerPage,
            input.sortBy?.map(el => [el.key, el.order]),
            input.additionalHeaders?.map(el => [el.title, el.key]),
            input.filters?.map(el => [el.key, el.operator, el.value ? [String(typeof el.value), el.value] : undefined]),
        ]
    return compile(items)
}

const stringTypeCheck = (obj: End) => typeof obj == 'string' ? obj : undefined
const stringTypeCheckNotNull = (obj: End, default_ = '') => typeof obj == 'string' ? obj : default_
const numberTypeCheck = (obj: End) => typeof obj == 'string' ? Number(obj) : undefined
const numberTypeCheckNotNull = (obj: End, default_ = 1) => typeof obj == 'string' ? Number(obj) : default_


export function inputFromString(input_: string): InputSchema | undefined {
    const input = decompile(input_)
    if (!input || typeof input != 'object') return undefined
    if (input[0] == 'item')
        return {
            inputType: 'item',
            id: numberTypeCheckNotNull(input[1]),
            table: stringTypeCheck(input[2])
        }
    else if (input[0] == 'create-item')
        return {
            inputType: 'create-item',
            table: stringTypeCheck(input[2])
        }
    else if (input[0] == 'parameters-list') {
        return {
            inputType: 'parameters-list',
            page: numberTypeCheck(input[1]),
            itemsPerPage: numberTypeCheck(input[2]),
            sortBy: typeof input[3] == 'object' ? input[3].map(el => {
                if (typeof el == 'object')
                    return {
                        key: stringTypeCheckNotNull(el[0], 'id'),
                        order: stringTypeCheckNotNull(el[1], 'desc')
                    }
            }).filter(el => el != undefined) : [],
            additionalHeaders: typeof input[4] == 'object' ? input[4].map(el => {
                if (typeof el == 'object' && typeof el[0] == 'string' && typeof el[1] == 'string')
                    return {
                        title: el[0],
                        key: el[1],
                        sortable: true
                    }
            }).filter(el => el != undefined) : [],
            filters: typeof input[5] == 'object' ? input[5].map(el => {
                if (typeof el == 'object')
                    return {
                        key: el[0],
                        operator: el[1],
                        value: typeof el[2] == 'object' ? (() => {
                            if (el[2][0] == 'number')
                                return numberTypeCheck(el[2][1])
                            else if (el[2][0] == 'string')
                                return stringTypeCheck(el[2][1])
                            else if (el[2][0] == 'boolean' && el[2][1] == 'true')
                                return true
                            else if (el[2][0] == 'boolean' && el[2][1] == 'false')
                                return false
                            return undefined
                        })() : undefined,
                    }
            }).filter(el => el != undefined) : []
        }
    }
    return
}
