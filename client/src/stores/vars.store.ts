import {defineStore} from "pinia";
import {ApiService} from "../api/ApiService.ts";

export interface Variable {
    key: string
    value: string
}


export const useVarsStore = defineStore({
    id: 'vars',
    state: () => ({
        vars: new Map<string, Variable[]>,
        loadings: {
            load: false
        }
    }),
    getters: {
        getByProject: state => {
            return (project: string) => {
                const vars = state.vars.get(project)
                return vars ? vars : []
            }
        },
    },
    actions: {
        async load(project: string | undefined) {
            if (!project) return {}
            const vars = this.vars.get(project)
            if (vars) {
                return vars
            }
            this.loadings.load = true
            const loadVars = await ApiService.post<Variable[]>('/api/vars/load', {project: project})
            this.vars.set(project, loadVars)
            this.loadings.load = false
            return loadVars
        },
        async change(project: string, key: string, value: string) {
            await ApiService.post('/api/vars/change', {project: project, key: key, value: value})
            let projectVars = this.vars.get(project)
            if (!projectVars) return
            projectVars = projectVars.map(v => {
                if (v.key == key) {
                    v.value = value
                    return v
                }
                return v
            })
            this.vars.set(project, projectVars)
        },
        async remove(project: string, key: string) {
            await ApiService.post('/api/vars/remove', {project: project, key: key})
            let projectVars = this.vars.get(project)
            if (!projectVars) return
            projectVars = projectVars.filter(v => v.key != key)
            this.vars.set(project, projectVars)
        },
        async create(project: string, key: string, value: string) {
            await ApiService.post('/api/vars/create', {project: project, key: key, value: value})
            this.vars.get(project)?.push({key: key, value: value})
        }
    }
})