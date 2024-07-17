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
        account: undefined as undefined | Account,
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
            this.account = await ApiService.get<Account | undefined>('/api/auth/me')
            this.auth = this.account != null
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
        },
        async logout() {
            await ApiService.get('/api/auth/logout')
        }
    }
})