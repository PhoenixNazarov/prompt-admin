import moment from "moment";

export function dateFormat(input: Date): String {
    return moment(input).format('MM/DD/YYYY HH:mm')
}