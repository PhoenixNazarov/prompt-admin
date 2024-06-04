import {createApp} from 'vue'
import './style.css'
import App from './App.vue'
import {createPinia} from "pinia";
import { faDiagramProject, faTable, faTerminal } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import VueDiff from 'vue-diff';
import 'vue-diff/dist/index.css';

const pinia = createPinia()

const app = createApp(App)

// Diff

app.use(VueDiff);

// Icons
library.add(
    faDiagramProject,
    faTable,
    faTerminal
)

// Pinia Store
app.use(pinia)

// Mount
app.mount('#app')
