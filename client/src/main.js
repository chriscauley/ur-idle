import { createApp } from 'vue'

import unrest from '@unrest/vue'
import auth from '@unrest/vue-auth'
import form from '@unrest/vue-form'
import '@unrest/tailwind/dist.css'

import App from './App.vue'
import router from './router'

createApp(App)
  .use(unrest.plugin)
  .use(unrest.ui)
  .use(form)
  .use(router)
  .use(auth.plugin)
  .mount('#app')
