import {defineStore} from "pinia";
import {BaseEntity} from "./config/abstractStoreFactory.ts";
import {ApiService} from "../api/ApiService.ts";

export interface HealthTarget extends BaseEntity {
    url: string
    title: string
}

export interface HealthDay extends BaseEntity {
    date: string
    count_response_time: number
    sum_response_time: number
    fall_times: number

    health_target_id: number
}

export interface HealthUnit {
    request_datetime: number
    status: boolean
    response_time: number
}

export const useHealthCheckStore = defineStore({
        id: 'healthCheck',
        state: () => ({
            targets: undefined as HealthTarget[] | undefined,
            days: new Map<number, HealthDay[]>,
            units: new Map<number, HealthUnit[]>,
            loadings: {
                targets: false
            }
        }),
        getters: {
            getDays: state => {
                return (healthTarget: HealthTarget) => {
                    if (healthTarget.id == undefined) return undefined
                    return state.days.get(healthTarget.id)
                }
            },
            getUnits: state => {
                return (healthTarget: HealthTarget) => {
                    if (healthTarget.id == undefined) return undefined
                    return state.units.get(healthTarget.id)
                }
            },
            getLastUnit: state => {
                return (healthTarget: HealthTarget) => {
                    if (healthTarget.id == undefined) return undefined
                    const sorted = state.units.get(healthTarget.id)?.sort((a, b) => (new Date(b.request_datetime)).getTime() - (new Date(a.request_datetime)).getTime())
                    if (sorted)
                        return sorted[0]
                }
            },
        },
        actions: {
            async loadTargets() {
                if (this.loadings.targets) return
                this.loadings.targets = true
                this.targets = await ApiService.get<HealthTarget[]>(`/api/healthcheck/targets/load`)
                if (this.targets) {
                    await Promise.all(
                        [
                            this.loadDays(this.targets),
                        ]
                    )
                }
                this.loadings.targets = false
            },
            async loadDays(healthTargets: HealthTarget[]) {
                const days = await ApiService.post<HealthDay[]>(`/api/healthcheck/days/load`, {targets_ids: healthTargets.map(el => el.id)})
                if (days == undefined) return
                days.forEach(
                    el => {
                        const hDays = this.days.get(el.health_target_id) || []
                        hDays.push(el)
                        this.days.set(el.health_target_id, hDays)
                    }
                )
            },
            async loadUnits(healthTarget: HealthTarget) {
                if (healthTarget.id == undefined) return
                const units = await ApiService.post<[number, boolean, number][]>(`/api/healthcheck/units/load`, {targets_id: healthTarget.id})
                if (units == undefined) return
                const hDays = this.units.get(healthTarget.id) || []
                units.forEach(
                    el => {
                        hDays.push(
                            {
                                request_datetime: el[2] * 1000,
                                status: el[1],
                                response_time: el[0],
                            }
                        )
                    }
                )
                this.units.set(healthTarget.id, hDays)
                return hDays
            }
        }
    }
)