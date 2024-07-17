import moment from "moment";

export function dateFormat(input: Date): string {
    return moment(input).format('MM/DD/YYYY HH:mm')
}

export function cropText(input: string, size = 100): string {
    if (input.length > size) {
        return input.substring(0, size - 3) + '...'
    }
    return input
}
