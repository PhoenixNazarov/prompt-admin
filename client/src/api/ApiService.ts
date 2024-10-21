import axios, {AxiosRequestConfig} from "axios";
import NotificationService from "../views/Notifications/NotificationService.ts";

function onError(error: any, method: 'get' | 'post', url: string) {
    let status: number | undefined = error.response?.status
    let code: string | undefined = error.code
    let detail: string | undefined = error.response?.data?.detail
    let message: string | undefined = error.message
    let errorMessage: string | undefined = error.response?.headers?.['error-message']

    if (!status) status = -1
    if (!code) code = 'UNDEFINED'
    if (!detail) detail = ''
    if (!message) message = 'Undefined error'
    if (!errorMessage) errorMessage = ''
    NotificationService.onError(`[API] ${method} ${url} - ${status} [${errorMessage}] ${detail}: ${message} (${code})`)
    throw error
}

export class ApiService {
    private static AXIOS_CONFIG: AxiosRequestConfig = {
        withCredentials: true,
    }

    public static async get<R>(url: string) {
        try {
            return (await axios.get<R>(url, this.AXIOS_CONFIG)).data
        } catch (e) {
            onError(e, 'get', url);
        }
    }


    public static async post<R>(url: string, data: unknown) {
        try {
            return (await axios.post<R>(url, data, this.AXIOS_CONFIG)).data
        } catch (e) {
            onError(e, 'post', url);
        }
    }
}