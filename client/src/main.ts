import {createApp} from 'vue'
import './style.css'
import App from './App.vue'
import {installDiff} from "./plugins/diff.ts";
import {installPinia} from "./plugins/pinia.ts";
import {installFortAwesome} from "./plugins/fortawesome.ts";
import {installVuetify} from "./plugins/vuetify.ts";
import {installRouter} from "./plugins/router.ts";
import {installPrimevue} from "./plugins/primevue.ts";
import {installChartJs} from "./plugins/chartjs.ts";


const app = createApp(App)

// Plugins
installDiff(app)
installPinia(app)
installFortAwesome(app)
installVuetify(app)
installRouter(app)
installPrimevue(app)
installChartJs(app)


// Mount
app.mount('#app')
