import moment from "moment";

export function dateTimeFormat(input: Date | string | undefined): string {
    if (!input) return ""
    return moment(input).format('MM/DD/YYYY HH:mm')
}


export function dateFormat(input: Date | string | undefined): string {
    if (!input) return ""
    return moment(input).format('DD MMM YYYY')
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

export function hashCode(str: string | number | undefined): number {
    const newStr = String(str)
    let h: number = 0;
    for (let i = 0; i < newStr.length; i++) {
        h = 31 * h + newStr.charCodeAt(i);
    }
    return h & 0xFFFFFFFF
}

export function randomString(length: number = 20) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        counter += 1;
    }
    return result;
}

export function chunk<T>(arr: T[], size: number): T[][] {
    return Array.from({length: Math.ceil(arr.length / size)}, (_: any, i: number) =>
        arr.slice(i * size, i * size + size)
    );
}

