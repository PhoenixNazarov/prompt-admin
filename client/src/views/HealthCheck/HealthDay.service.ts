import {HealthDay, HealthTarget, useHealthCheckStore} from "../../stores/healthcheck.store.ts";
import {equalDate} from "../Utils.ts";

export class HealthDayService {
    private healthDay: HealthDay | undefined

    constructor(healthDay: HealthDay | undefined) {
        this.healthDay = healthDay
    }

    static fromDay(healthTarget: HealthTarget, d: number) {
        const healthCheckStore = useHealthCheckStore()
        const date = this.showDate(d)
        const healthDay = healthCheckStore.getDays(healthTarget)?.find(el => {
            const day = new Date(el.date)
            return equalDate(date, day)
        })
        return new HealthDayService(healthDay)
    }

    static showDate(d: number) {
        const date = new Date();
        date.setDate(date.getDate() - d + 1);
        return date
    }

    getStatus() {
        const fallTimes = this.getFallTimes()
        if (fallTimes == undefined) return 'Lost'
        if (fallTimes > 0) {
            return 'Downtime'
        }
        return `Operational`
    }

    getDescription() {
        const fallTimes = this.getFallTimes()
        const lostTimes = this.getLostTimes()
        let res = ''
        if (fallTimes != undefined && fallTimes > 0) {
            res += `Down for ${fallTimes} minutes`
        }
        if (lostTimes != undefined && lostTimes > 0) {
            res += `<br>Lost for ${lostTimes} minutes`
        }
        return res;
    }

    getPercentage() {
        if (this.healthDay == undefined) return
        const fallTimes = this.getFallTimes()
        const lostTimes = this.getLostTimes()
        if (!fallTimes) return undefined
        return (fallTimes / this.healthDay.count_response_time) * 100 + (lostTimes / (60 * 24)) * 30
    }

    getFallTimes() {
        if (!this.healthDay) return
        return this.healthDay.fall_times
    }

    getLostTimes() {
        const maxTimes = this.getMaxTimes()
        const responseTime = this.healthDay?.count_response_time
        if (responseTime == undefined) return 0
        const lostTimes = maxTimes - responseTime
        return lostTimes > 30 ? lostTimes : 0
    }

    getMaxTimes() {
        let maxTimes = 60 * 24
        if (this.isToday()) {
            const now = new Date()
            return now.getHours() * 24 + now.getMinutes()
        }
        return maxTimes
    }

    isToday() {
        if (!this.healthDay) return
        return equalDate(new Date(), new Date(this.healthDay.date))
    }
}