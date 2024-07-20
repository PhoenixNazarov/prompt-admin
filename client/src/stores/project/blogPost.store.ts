import {defineStore} from "pinia";
import {
    abstractStoreFactory,
    abstractStoreFactoryGetters,
    abstractStoreFactoryState,
    BaseEntity
} from "../config/abstractStoreFactory.ts";


export interface BlogPost extends BaseEntity {
    project: string
    title: string
    content: string
    group_id?: number
}


export const useBlogPostStore = defineStore({
    id: 'blogPost',
    state: () => ({
        ...abstractStoreFactoryState<BlogPost>()
    }),
    getters: {
        ...abstractStoreFactoryGetters<BlogPost>(),
        getPostByGroup: state => {
            return (project: string, groupId: number | undefined) => {
                return state.entity.filter(e => e.project == project && e.group_id == groupId)
            }
        }
    },
    actions: {
        ...abstractStoreFactory<BlogPost>('blog_post', 'project/')
    }
})