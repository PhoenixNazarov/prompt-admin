import {BaseRouter} from "../../api/BaseRouter.ts";

export interface BaseEntity {
    id?: number
    time_create?: string
}

export function abstractStoreFactoryState<T extends BaseEntity>() {
    return {
        entity: [] as T[],
        loadings: {
            loadAll: undefined as undefined | Promise<T[]>
        }
    }
}

export function abstractStoreFactoryGetters<T extends BaseEntity>() {
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

export function abstractStoreFactory<T extends BaseEntity>(name: string, prefix = 'config/') {
    return {
        async loadAll(): Promise<T[]> {
            if (this.loadings.loadAll) return await this.loadings.loadAll
            this.loadings.loadAll = new BaseRouter<T>(`/api/${prefix}${name}`).getAll()
            const result = await this.loadings.loadAll
            this.entity = result
            this.loadings.loadAll = undefined
            return result
        },

        async save(entity: T) {
            const result = await new BaseRouter<T>(`/api/${prefix}${name}`).save(entity)
            this.entity = this.entity.filter(e => e.id != result.id)
            this.entity.push(result)
            return result
        },

        async remove(id?: number) {
            if (id == undefined) return
            await new BaseRouter<T>(`/api/${prefix}${name}`).remove(id)
            this.entity = this.entity.filter(e => e.id != id)
        },

        async findByKey(key: string, value: string | number | boolean) {
            const entities = await new BaseRouter<T>(`/api/${prefix}${name}`).findByKey(key, value)

            entities.forEach(el => {
                if (this.entity.findIndex(el2 => el2.id == el.id) <= -1) {
                    this.entity.push(el)
                }
            })
        }
    }
}