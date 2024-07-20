import type {App} from "vue";

import PrimeVue from "primevue/config";
import Aura from '@primevue/themes/aura';

export function installPrimevue(app: App) {
    app.use(PrimeVue, {
        theme: {
            preset: Aura,
            options: {
                prefix: 'p',
                darkModeSelector: 'white',
                cssLayer: false
            }
        }
    });
}