import axios, {AxiosRequestConfig} from "axios";
import NotificationService from "../views/Notifications/NotificationService.ts";

export class ApiService {
    private static AXIOS_CONFIG: AxiosRequestConfig = {
        withCredentials: true,
    }

    public static async get<R>(url: string) {
        try {
            return (await axios.get<R>(url, this.AXIOS_CONFIG)).data
        } catch (e) {
            NotificationService.onError(`[API] get ${url}: Undefined error`)
            throw e
        }
    }


    public static async post<R>(url: string, data: unknown) {
        try {
            return (await axios.post<R>(url, data, this.AXIOS_CONFIG)).data
        } catch (e) {
            NotificationService.onError(`[API] post ${url}: Undefined error`)
            throw e
        }
    }
}