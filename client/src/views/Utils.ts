import moment from "moment";

export function dateFormat(input: Date | string | undefined): string {
    if (!input) return ""
    return moment(input).format('MM/DD/YYYY HH:mm')
}

export function cropText(input: string, size = 100): string {
    if (input.length > size) {
        return input.substring(0, size - 3) + '...'
    }
    return input
}


export function parseJson(input: string | undefined) {
    if (!input) return
    try {
        return JSON.parse(input)
    } catch (e) {
    }
    return
}