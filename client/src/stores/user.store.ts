import {defineStore} from "pinia";
import {ApiService} from "../api/ApiService.ts";
import {BaseEntity} from "./config/abstractStoreFactory.ts";
import {WsService} from "../api/WsService.ts";


export interface Account extends BaseEntity {
    login: string
}

export const useAccountStore = defineStore({
    id: 'account',
    state: () => ({
        auth: false,
        account: undefined as undefined | Account,
        entity: [] as Account[],
        loadings: {
            loadMe: undefined as undefined | Promise<Account | undefined>
        }
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
            if (this.loadings.loadMe) return await this.loadings.loadMe
            if (this.account) return this.account
            this.loadings.loadMe = ApiService.get<Account | undefined>('/api/auth/me')
            this.account = await this.loadings.loadMe
            this.loadings.loadMe = undefined
            this.auth = this.account != null
            return this.account
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
                WsService.connect(true).then()
            } catch (e) {
                this.auth = false
            }
        },
        async loadAll() {
            this.entity = await ApiService.get('/api/config/account/get/all')
        },
        async logout() {
            await ApiService.get('/api/auth/logout')
        },
        async getWsToken() {
            await this.loadMe()
            return await ApiService.get<{ token: string }>('/api/auth/ws/token')
        }
    }
})