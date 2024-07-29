import {defineStore} from "pinia";
import {ApiService} from "../api/ApiService.ts";

export const useVarsStore = defineStore({
    id: 'vars',
    state: () => ({
        vars: new Map<string, Map<string, string>>,
        loadings: {}
    }),
    getters: {},
    actions: {
        async load(project: string | undefined) {
            if (!project) return {}
            const vars = this.vars.get(project)
            if (vars) {
                return vars
            }
            const loadVars = await ApiService.post<Map<string, string>>('/api/vars/load', {project: project})
            this.vars.set(project, loadVars)
            return loadVars
        }
    }
})