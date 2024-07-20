import {defineStore} from "pinia";
import {
    abstractStoreFactory,
    abstractStoreFactoryGetters,
    abstractStoreFactoryState,
    BaseEntity
} from "../config/abstractStoreFactory.ts";


export interface BlogGroup extends BaseEntity {
    project: string
    title: string
}


export const useBlogGroupStore = defineStore({
    id: 'blogGroup',
    state: () => ({
        ...abstractStoreFactoryState<BlogGroup>()
    }),
    getters: {
        ...abstractStoreFactoryGetters<BlogGroup>(),
        getGroupByProject: state => {
            return (project: string) => {
                return state.entity.filter(e => e.project == project)
            }
        }
    },
    actions: {
        ...abstractStoreFactory<BlogGroup>('blog_group', 'project/')
    }
})