import { RestStorage } from '@unrest/vue-storage'

export default () => {
  const name = 'schema/task'
  return RestStorage(name, { collection_slug: name })
}
