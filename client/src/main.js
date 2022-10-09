import { createApp } from 'vue'
import unrest from '@unrest/vue'
import auth from '@unrest/vue-auth'
import form from '@unrest/vue-form'
import Datepicker from '@vuepic/vue-datepicker'

import '@unrest/tailwind/dist.css'
import '@vuepic/vue-datepicker/dist/main.css'

import App from './App.vue'
import router from './router'
import store from './store'
import './css/index.css'

createApp(App)
  .component('date-picker', Datepicker)
  .use(unrest.plugin)
  .use(unrest.ui)
  .use(form)
  .use(router)
  .use(auth.plugin)
  .use(store)
  .mount('#app')
