import {ApiService} from "./ApiService.ts";

export class BaseRouter<T> {
    baseUrl: string

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl
    }

    getAll() {
        return ApiService.get<T[]>(`${this.baseUrl}/get/all`);
    }

    save(entity: T) {
        return ApiService.post<T>(`${this.baseUrl}/save`, entity);
    }

    remove(id: number) {
        return ApiService.get<T[]>(`${this.baseUrl}/remove/${id}`);
    }
}