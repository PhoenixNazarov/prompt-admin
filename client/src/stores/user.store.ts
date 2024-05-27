import {defineStore} from "pinia";
import axios from 'axios'


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
            const out = await axios.get<{ login: string } | null>(
                '/api/auth/me'
            )
            this.auth = out.data != null
        },
        async login(login: string, password: string) {
            try {
                await axios.post<{ login: string } | null>(
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