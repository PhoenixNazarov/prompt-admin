import {defineStore} from "pinia";
import {ApiService} from "../api/ApiService.ts";


export const useAccountStore = defineStore({
    id: 'account',
    state: () => ({
        auth: false
    }),
    getters: {
        logged(state) {
            return state.auth
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
        }
    }
})