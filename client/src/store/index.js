import task from './task'

const store = {}

const modules = { task }

export default {
  install(app) {
    app.config.globalProperties.$store = store
    store._app = app

    Object.entries(modules).forEach(([name, module]) => {
      this[name] = store[name] = module({ store })
    })
  },
}
