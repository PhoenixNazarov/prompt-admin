import {defineStore} from "pinia";
import {ApiService} from "../../../api/ApiService.ts";

export const useTableStore = defineStore({
    id: 'table',
    state: () => ({
        schemas: new Map<string, any>()
    }),
    getters: {
        schemaByProject: state => {
            return (project: string) => state.schemas.get(project)
        },
    },
    actions: {
        async loadSchema(project: string) {
            const alreadyProject = this.schemas.get(project)
            if (alreadyProject) {
                return alreadyProject
            }
            const result = (await ApiService.post<{
                table_schema: any
            } | undefined>('/api/project/tables/main/schema/download',
                {
                    project: project,
                }
            ))?.table_schema
            this.schemas.set(project, result)
            return result
        },
        async uploadSchema(project: string, schema: any) {
            await ApiService.post('/api/project/tables/main/schema/upload',
                {
                    project: project,
                    table_schema: schema
                }
            )
        },
        async listLoad(
            project: string,
            table: string,
            columns: string[],
            page: number,
            count: number,
            orderBy: {
                key: string,
                order: 'ask' | 'desc'
            }[] | undefined = undefined,
            filters: {
                key: string,
                value?: string | number | boolean | undefined,
                operator: string
            }[] | undefined = undefined,
            joins: {
                table: string
                pseudo?: string
                condition: string
            }[] | undefined = undefined
        ) {
            return await ApiService.post<any[]>('/api/project/tables/list/load',
                {
                    project: project,
                    table: table,
                    columns: columns,
                    page: page - 1,
                    count: count,
                    order_by: orderBy,
                    filter: filters,
                    joins: joins
                }
            )
        },
        async listCount(
            project: string,
            table: string,
            columns: string[],
            filters: {
                key: string,
                value?: string | number | boolean | undefined,
                operator: string
            }[] | undefined = undefined,
            joins: {
                table: string
                pseudo?: string
                condition: string
            }[] | undefined = undefined
        ) {
            return await ApiService.post<{ count: number }>('/api/project/tables/list/count',
                {
                    project: project,
                    table: table,
                    columns: columns,
                    filter: filters,
                    joins: joins
                }
            )
        },
        async fetchColumns(
            project: string,
            table: string
        ) {
            return await ApiService.post<{
                column_name: string,
                data_type: string
            }[]>('/api/project/tables/list/fetch_columns',
                {
                    project: project,
                    table: table,
                }
            )
        },
        async loadItem(project: string, table: string, id: number) {
            return await ApiService.post<any>('/api/project/tables/item/load',
                {
                    project: project,
                    table: table,
                    id: id,
                }
            )
        },
        async updateItem(project: string, table: string, id: number, columns: { key: string, value: any }[]) {
            return await ApiService.post<any>('/api/project/tables/item/update',
                {
                    project: project,
                    table: table,
                    id: id,
                    columns: columns
                }
            )
        },
        async createItem(project: string, table: string, columns: { key: string, value: any }[]) {
            return await ApiService.post<{ id: number }>('/api/project/tables/item/create',
                {
                    project: project,
                    table: table,
                    columns: columns
                }
            )
        },
        async deleteItem(project: string, table: string, id: number) {
            return await ApiService.post('/api/project/tables/item/delete',
                {
                    project: project,
                    table: table,
                    id: id
                }
            )
        },
        async executeGet(project: string, url: string) {
            return await ApiService.post('/api/project/tables/execute/get',
                {
                    project: project,
                    url: url
                }
            )
        },
        async executePost(project: string, url: string, data: any) {
            return await ApiService.post('/api/project/tables/execute/post',
                {
                    project: project,
                    url: url,
                    data: data
                }
            )
        }
    }
})