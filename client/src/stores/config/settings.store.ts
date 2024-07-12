import {defineStore} from "pinia";


export const useSettingsStore = defineStore({
    id: 'settings',
    state: () => ({
        changelog_folding: false,
        changelog_different_current: false,
        changelog_mode: 'split' as 'split' | 'unified',
        menuOpenedItems: [] as string[]
    }),
    getters: {},
    actions: {},
    persist: true
})