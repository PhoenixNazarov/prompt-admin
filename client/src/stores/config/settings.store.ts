import {defineStore} from "pinia";


export const useSettingsStore = defineStore({
    id: 'settings',
    state: () => ({
        changelog_folding: false,
        changelog_different_current: false,
        changelog_mode: 'split' as 'split' | 'unified',
        menuOpenedItems: [] as string[],
        editor_line_wrapping: true,
        hint_fold: false,
        menu_fold: false
    }),
    getters: {},
    actions: {},
    persist: true
})