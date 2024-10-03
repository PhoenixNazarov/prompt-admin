import {createRouter, createWebHistory} from "vue-router";
import type {App} from "vue";
import {useAccountStore} from "../stores/user.store.ts";
import {useMappingStore} from "../stores/config/mapping.store.ts";
import {useMappingEntityStore} from "../stores/config/mappingEntity.store.ts";
import {useOutputStore} from "../stores/config/output.store.ts";
import {usePromptStore} from "../stores/prompt.store.ts";
import {useMacroStore} from "../stores/config/macro.store.ts";
import {useInputStore} from "../stores/config/input.store.ts";
import {useVarsStore} from "../stores/vars.store.ts";
import {WsService} from "../api/WsService.ts";


function tableIdProp(id: string): number | undefined {
    const number = Number.parseInt(id)
    return number == -1 ? undefined : number
}


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            name: 'MainGroup',
            path: '',
            redirect: '/authorization',
            children: [
                {
                    name: 'NoAuthGroup',
                    path: '/authorization',
                    component: () => import('../views/Authorization.vue'),
                    async beforeEnter(_to, _from, next) {
                        const accountStore = useAccountStore()
                        await accountStore.loadMe()
                        if (accountStore.logged) {
                            next('/workplace')
                        } else {
                            next()
                        }
                    },
                },
                {
                    name: 'AuthGroup',
                    path: '',
                    component: () => import('../layouts/MainLayout.vue'),
                    async beforeEnter(_to, _from, next) {
                        const accountStore = useAccountStore()
                        await accountStore.loadMe()
                        WsService.connect().then()
                        if (!accountStore.logged) {
                            next('/authorization')
                        } else {
                            next()
                        }
                    },
                    children: [
                        {
                            name: 'AuthGroupDefault',
                            path: '',
                            redirect: '/workplace'
                        },
                        {
                            name: 'Workplace',
                            path: '/workplace',
                            component: () => import('../views/Workplace/WorkplaceView.vue')
                        },
                        {
                            name: 'Format',
                            path: '/format',
                            component: () => import('../views/Format/FormatView.vue')
                        },
                        {
                            name: 'Account',
                            path: '/account',
                            component: () => import('../views/Account/AccountView.vue')
                        },
                        {
                            name: 'Table',
                            path: '/table',
                            redirect: '/table/mapping',
                            async beforeEnter() {
                                const mappingStore = useMappingStore()
                                const mappingEntityStore = useMappingEntityStore()
                                const outputStore = useOutputStore()
                                const promptStore = usePromptStore()
                                const macroStore = useMacroStore()
                                const inputStore = useInputStore()

                                await Promise.all([
                                    mappingStore.loadAll(),
                                    mappingEntityStore.loadAll(),
                                    outputStore.loadAll(),
                                    macroStore.loadAll(),
                                    inputStore.loadAll()
                                ])
                                promptStore.loadAll().then()
                            },
                            component: () => import('../views/Tables/Edit/Components/TableLayout.vue'),
                            props: route => {
                                return {list: route.meta.list as string}
                            },
                            children: [
                                {
                                    name: 'MappingTable',
                                    path: 'mapping',
                                    meta: {list: 'mapping'},
                                    children: [
                                        {
                                            name: 'MappingList',
                                            path: '',
                                            component: () => import('../views/Tables/Edit/MappingList.vue'),
                                        },
                                        {
                                            name: 'MappingItem',
                                            path: ':id',
                                            component: () => import('../views/Tables/Edit/MappingItem.vue'),
                                            props: route => {
                                                return {id: tableIdProp(route.params.id as string)}
                                            }
                                        },
                                    ]
                                },
                                {
                                    name: 'MappingEntityTable',
                                    path: 'mapping-entity',
                                    meta: {list: 'mapping-entity'},
                                    children: [
                                        {
                                            name: 'MappingEntityList',
                                            path: '',
                                            component: () => import('../views/Tables/Edit/MappingEntityList.vue'),
                                        },
                                        {
                                            name: 'MappingEntityItem',
                                            path: ':id',
                                            component: () => import('../views/Tables/Edit/MappingEntityItem.vue'),
                                            props: route => {
                                                let args = {}
                                                try {
                                                    args = JSON.parse(route.hash.substring(1))
                                                } catch (e) {

                                                }
                                                return {id: tableIdProp(route.params.id as string), ...args}
                                            }
                                        }
                                    ]
                                },
                                {
                                    name: 'MacroTable',
                                    path: 'macro',
                                    meta: {list: 'macro'},
                                    children: [
                                        {
                                            name: 'MacroList',
                                            path: '',
                                            component: () => import('../views/Tables/Edit/MacroList.vue')
                                        },
                                        {
                                            name: 'MacroItem',
                                            path: ':id',
                                            component: () => import('../views/Tables/Edit/MacroItem.vue'),
                                            props: route => {
                                                return {id: tableIdProp(route.params.id as string)}
                                            }
                                        }
                                    ]
                                },
                                {
                                    name: 'InputTable',
                                    path: 'input',
                                    meta: {list: 'input'},
                                    children: [
                                        {
                                            name: 'InputList',
                                            path: '',
                                            component: () => import('../views/Tables/Edit/InputList.vue')
                                        },
                                        {
                                            name: 'InputItem',
                                            path: ':id',
                                            component: () => import('../views/Tables/Edit/InputItem.vue'),
                                            props: route => {
                                                return {id: tableIdProp(route.params.id as string)}
                                            }
                                        }
                                    ]
                                },
                                {
                                    name: 'OutputTable',
                                    path: 'output',
                                    meta: {list: 'output'},
                                    children: [
                                        {
                                            name: 'OutputList',
                                            path: '',
                                            component: () => import('../views/Tables/Edit/OutputList.vue'),
                                        },
                                        {
                                            name: 'OutputItem',
                                            path: ':id',
                                            component: () => import('../views/Tables/Edit/OutputItem.vue'),
                                            props: route => {
                                                return {id: tableIdProp(route.params.id as string)}
                                            }
                                        },
                                    ]
                                },
                                {
                                    name: 'PromptTable',
                                    path: 'prompt',
                                    meta: {list: 'prompt'},
                                    children: [
                                        {
                                            name: 'PromptList',
                                            path: '',
                                            component: () => import('../views/Tables/Edit/PromptList.vue'),
                                        }
                                    ]
                                },
                            ]
                        },
                        {
                            name: 'Project',
                            path: '/project',
                            children: [
                                {
                                    name: 'ProjectMain',
                                    path: ':project',
                                    props: route => {
                                        return {project: route.params.project as string}
                                    },
                                    redirect: to => {
                                        return {path: `/project/${to.params.project}/group/-1`}
                                    },
                                    children: [
                                        {
                                            name: 'ProjectBlog',
                                            path: 'group/:groupId',
                                            component: () => import('../views/Project/BlogView.vue'),
                                            props: route => {
                                                return {
                                                    project: route.params.project as string,
                                                    groupId: Number.parseInt(route.params.groupId as string)
                                                }
                                            }
                                        },
                                        {
                                            name: 'ProjectVars',
                                            path: 'vars',
                                            component: () => import('../views/Project/ProjectVarView.vue'),
                                            props: route => {
                                                useVarsStore().load(route.params.project as string)
                                                return {
                                                    project: route.params.project as string,
                                                }
                                            }
                                        },
                                        {
                                            name: 'ProjectStatus',
                                            path: 'status',
                                            component: () => import('../views/Project/Status/ProjectStatus.vue'),
                                            props: route => {
                                                return {
                                                    project: route.params.project as string,
                                                }
                                            }
                                        },
                                        {
                                            name: 'ProjectTables',
                                            path: 'tables/:pathMatch(.*)*',
                                            component: () => import('../views/Project/Tables/ProjectTableView.vue'),
                                            props: route => {
                                                return {
                                                    project: route.params.project as string,
                                                    hash: typeof route.params.pathMatch == 'string' ? [] : route.params.pathMatch
                                                }
                                            }
                                        },
                                        {
                                            name: 'ProjectTablesEdit',
                                            path: 'edit_tables',
                                            component: () => import('../views/Project/Tables/EditTableView.vue'),
                                            props: route => {
                                                return {
                                                    project: route.params.project as string,
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            path: '/:pathMatch(.*)*',
            name: 'NotFound',
            redirect: '/authorization'
        }
    ]
});

export class RouterService {
    static async goToAuthorization() {
        await router.push('/authorization')
    }

    static async goToWorkplace() {
        await router.push('/workplace')
    }

    static async goToFormat() {
        await router.push('/format')
    }

    static async goToTableList(name = 'mapping') {
        await router.push(`/table/${name}`)
    }

    static async goToAccount() {
        await router.push('/account')
    }

    static async goToTableItem(name = 'mapping', id = -1, preSet: Object = {}) {
        await router.push(`/table/${name}/${id}#${JSON.stringify(preSet)}`)
    }

    static async goToProject(project: string) {
        await router.push(`/project/${project}`)
    }

    static async goToProjectGroup(project: string, groupId: number | undefined) {
        await router.push(`/project/${project}/group/${groupId == undefined ? -1 : groupId}`)
    }

    static async goToProjectVars(project: string) {
        await router.push(`/project/${project}/vars`)
    }

    static async goToProjectStatus(project: string) {
        await router.push(`/project/${project}/status`)
    }

    static async goToProjectTables(project: string) {
        await router.push(`/project/${project}/tables`)
    }

    static async goToProjectTableEdit(project: string) {
        await router.push(`/project/${project}/edit_tables`)
    }
}


export function installRouter(app: App) {
    app.use(router)
}
