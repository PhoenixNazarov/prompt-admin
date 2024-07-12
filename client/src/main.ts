import {createApp} from 'vue'
import './style.css'
import App from './App.vue'
import {installDiff} from "./plugins/diff.ts";
import {installPinia} from "./plugins/pinia.ts";
import {installFortAwesome} from "./plugins/fortawesome.ts";
import {installVuetify} from "./plugins/vuetify.ts";


const app = createApp(App)

// Plugins
installDiff(app)
installPinia(app)
installFortAwesome(app)
installVuetify(app)

// Mount
app.mount('#app')
