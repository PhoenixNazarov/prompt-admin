import {ApiService} from "../../api/ApiService.ts";

export interface BaseEntity {
    id?: number
    time_create?: string
}

export function abstractStoreFactoryState<T>() {
    return {
        entity: [] as T[],
        loadings: {
            loadAll: false
        }
    }
}

export function abstractStoreFactoryGetters<T>() {
    return {
        getById: state => {
            return (id: number | undefined): T | undefined => {
                if (id == undefined) return undefined
                return state.entity.find(e => e.id == id)
            }
        },
        getByIds: state => {
            return (ids: number[]): T[] => {
                const _ids = ids.map(i => Number.parseInt(String(i)))
                return state.entity.filter(e => _ids.includes(e.id))
            }
        }
    }
}

export function abstractStoreFactory<T>(name: string) {
    return {
        async loadAll() {
            this.loadings.loadAll = true
            const result = await ApiService.get<T[]>(`/api/config/${name}/get/all`)
            this.entity = result
            this.loadings.loadAll = false
            return result
        },

        async save(entity: T) {
            const result = await ApiService.post<T>(`/api/config/${name}/save`, entity)
            this.entity = this.entity.filter(e => e.id != result.id)
            this.entity.push(result)
            return result
        },

        async remove(id?: number) {
            if (id == undefined) return
            await ApiService.get<T | undefined>(`/api/config/${name}/remove/${id}`)
            this.entity = this.entity.filter(e => e.id != id)
        }
    }
}