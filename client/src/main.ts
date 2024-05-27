import {createApp} from 'vue'
import './style.css'
import App from './App.vue'
import {createPinia} from "pinia";

const pinia = createPinia()

const app = createApp(App)

// Plugins
app.use(pinia)

// Mount
app.mount('#app')
