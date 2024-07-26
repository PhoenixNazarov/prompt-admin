import {defineStore} from "pinia";
import {ApiService} from "../../api/ApiService.ts";

export const useProjectStore = defineStore({
    id: 'project',
    state: () => ({
        projects: [] as string[]
    }),
    getters: {},
    actions: {
        async loadProjects() {
            this.projects = await ApiService.get<string[]>('/api/project/main/get')
        }
    }
})