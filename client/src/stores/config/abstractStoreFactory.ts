import {ApiService} from "../../api/ApiService.ts";

export interface BaseEntity {
    id: number
    time_create: string
}

export function abstractStoreFactoryState<T>() {
    return {
        entity: [] as T[],
        loadings: {
            getAll: false
        }
    }
}

export function abstractStoreFactory(name: string) {
    return {
        async getAll() {
            this.loadings.getAll = true
            this.entity = await ApiService.get('/api/config/' + name + '/get/all')
            this.loadings.getAll = false
        }
    }
}