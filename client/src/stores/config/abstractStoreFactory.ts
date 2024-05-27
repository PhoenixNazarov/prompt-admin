import axios from "axios";

export interface BaseEntity {
    id: number
    time_create: string
}

export function abstractStoreFactory(name: string) {
    return {
        async getAll() {
            const out = await axios.get(
                '/api/config/' + name + '/get/all'
            )
            this.entity = out.data
        }
    }
}