import {
    BarElement,
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LinearScale,
    LineElement,
    LogarithmicScale,
    PointElement,
    TimeScale,
    Title,
    Tooltip
} from 'chart.js'
import type {App} from "vue";
import 'chartjs-adapter-moment';

export function installChartJs(app: App) {
    ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, TimeScale, LogarithmicScale, LineElement, PointElement)
}

