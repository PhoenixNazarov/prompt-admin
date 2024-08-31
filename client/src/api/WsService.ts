import {useAccountStore} from "../stores/user.store.ts";
import {usePromptStore} from "../stores/prompt.store.ts";

type Handler = (data: any) => Promise<unknown>

class _WsService {
    socket: WebSocket | undefined = undefined
    handlers: Map<String, Handler> = new Map()

    async connect(reconnect = false) {
        if (this.socket && !reconnect) {
            return
        }
        const accountStore = useAccountStore()
        let token
        try {
            token = await accountStore.getWsToken()
        } catch (e) {
            setTimeout(() => WsService.connect(true), 1000)
            return
        }
        if (!token) return
        this.socket = new WebSocket(`/api/ws/${token.token}`)
        this.socket.onmessage = (event: any) => this.onMessage(event, this.handlers)
        this.socket.onclose = () => WsService.connect(true)
    }

    async onMessage(event: any, handlers: Map<String, Handler>) {
        const data: string = event.data
        let dataJson
        try {
            dataJson = JSON.parse(JSON.parse(data))
        } catch (e) {
            return
        }
        if (!dataJson) return
        const type = dataJson["type"]
        const handler = handlers.get(type)
        if (handler) {
            await handler(dataJson)
        }
    }

    addHandler(type: string, f: Handler) {
        this.handlers.set(type, f)
    }
}

export const WsService = new _WsService()

WsService.addHandler('prompt-execute', async (data: any) => {
    const uuid: string = data.uuid
    const text: string = data.text

    const promptStore = usePromptStore()
    promptStore.executeStream(uuid, text)
})
