import {createApp} from 'vue'
import './style.css'
import App from './App.vue'
import {createPinia} from "pinia";
import {
    faCalculator,
    faCheck,
    faDiagramProject,
    faPen,
    faTable,
    faTerminal,
    faXmark
} from '@fortawesome/free-solid-svg-icons'
import {library} from '@fortawesome/fontawesome-svg-core'
import VueDiff from 'vue-diff';
import 'vue-diff/dist/index.css';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(App)

// Diff

app.use(VueDiff);

// Icons
library.add(
    faDiagramProject,
    faTable,
    faTerminal,
    faPen,
    faCalculator,
    faCheck,
    faXmark
)

// Pinia Store
app.use(pinia)

// Mount
app.mount('#app')
