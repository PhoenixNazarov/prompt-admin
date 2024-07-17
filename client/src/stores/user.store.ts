import {defineStore} from "pinia";
import {ApiService} from "../api/ApiService.ts";
import {BaseEntity} from "./config/abstractStoreFactory.ts";


export interface Account extends BaseEntity {
    login: string
}

export const useAccountStore = defineStore({
    id: 'account',
    state: () => ({
        auth: false,
        entity: [] as Account[]
    }),
    getters: {
        logged(state) {
            return state.auth
        },
        getById: state => {
            return (id: number) => {
                return state.entity.find(e => e.id == id)
            }
        },
        getLoginById: state => {
            return (id: number | undefined) => {
                return state.entity.find(e => e.id == id)?.login
            }
        }
    },
    actions: {
        async loadMe() {
            this.auth = await ApiService.get<{ login: string } | null>('/api/auth/me') != null
        },
        async login(login: string, password: string) {
            try {
                await ApiService.post<{ login: string } | null>(
                    '/api/auth/login',
                    {
                        login: login,
                        password: password
                    }
                )
                this.auth = true
            } catch (e) {
                this.auth = false
            }
        },
        async loadAll() {
            this.entity = await ApiService.get('/api/config/account/get/all')
        }
    }
})