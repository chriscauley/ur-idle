import activity from './activity'
import project from './project'
import task from './task'
import ui from './ui'

const store = {}

const modules = { activity, project, task, ui }

export default {
  install(app) {
    app.config.globalProperties.$store = store
    store._app = app

    Object.entries(modules).forEach(([name, module]) => {
      this[name] = store[name] = module({ store })
    })
  },
}
