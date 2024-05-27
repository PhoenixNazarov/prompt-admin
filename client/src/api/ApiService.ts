import axios, {AxiosRequestConfig} from "axios";

export class ApiService {
    private static AXIOS_CONFIG: AxiosRequestConfig = {
        withCredentials: true,
    }

    public static async get<R>(url: string) {
        return (await axios.get<R>(url, this.AXIOS_CONFIG)).data
    }


    public static async post<R>(url: string, data: unknown) {
        return (await axios.post<R>(url, data, this.AXIOS_CONFIG)).data
    }
}