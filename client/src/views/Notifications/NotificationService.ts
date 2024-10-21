import {reactive} from "vue";

type NotificationLevel = 'info' | 'debug' | 'error' | 'warning'

const DEFAULT_TIMEOUT = 10000


interface Notification {
    message: string
    level: NotificationLevel,
    timeout: number | undefined
}


export const notifications = reactive([] as Notification[])


class NotificationService {
    doNotify(message: string, level: NotificationLevel) {
        notifications.push({
            message: message,
            level: level,
            timeout: DEFAULT_TIMEOUT
        })
    }

    onError(message: string) {
        this.doNotify(message, 'error')
    }
}

export default new NotificationService()