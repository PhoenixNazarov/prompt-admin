import type { App } from 'vue'

import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles/main.sass'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export function installVuetify(app: App) {
  const vuetify = createVuetify({
    components,
    directives
  })

  app.use(vuetify)
}
