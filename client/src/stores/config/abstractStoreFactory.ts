import {ApiService} from "../../api/ApiService.ts";

export interface BaseEntity {
    id: number
    time_create: string
}

export function abstractStoreFactory(name: string) {
    return {
        async getAll() {
            this.entity = await ApiService.get('/api/config/' + name + '/get/all')
        }
    }
}