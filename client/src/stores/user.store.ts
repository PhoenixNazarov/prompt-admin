import {defineStore} from "pinia";
import {ApiService} from "../api/ApiService.ts";
import {BaseEntity} from "./config/abstractStoreFactory.ts";
import {WsService} from "../api/WsService.ts";


export interface Account extends BaseEntity {
    login: string
}


export interface Permission extends BaseEntity {
    account_id: number

    key: string
    value: number
    project?: string
}

export const useAccountStore = defineStore({
    id: 'account',
    state: () => ({
        auth: false,
        account: undefined as undefined | Account,
        entity: [] as Account[],
        permissions: undefined as undefined | Permission[],

        projects: undefined as undefined | string[],

        loadings: {
            loadMe: undefined as undefined | Promise<Account | undefined>,
            loadPermissions: false
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
            if (this.auth) this.loadPermissions().then()
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
        },
        async loadPermissions() {
            if (this.loadings.loadPermissions) return
            this.loadings.loadPermissions = true
            this.permissions = await ApiService.get<Permission[]>('/api/permission/get')

            const permissionValue = this.permissions.find(el => el.key == 'config_accounts')?.value
            if (permissionValue && permissionValue > 0) {
                this.loadProjects().then()
            }
            this.loadings.loadPermissions = false
        },
        async loadPermission(accountId: number) {
            return await ApiService.post<Permission[]>('/api/permission/get/user', {account_id: accountId})
        },
        async loadProjects() {
            if (this.projects) return
            this.projects = await ApiService.get<string[]>('/api/permission/get/projects')
        },
        async setPermission(
            account_id: number,
            key: string,
            value: number,
            project: string | undefined
        ) {
            await ApiService.post('/api/permission/set/user', {
                account_id: account_id,
                key: key,
                value: value,
                project: project
            })
        }
    }
})