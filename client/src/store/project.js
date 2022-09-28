import { RestStorage } from '@unrest/vue-storage'

export default () => {
  const name = 'schema/project'
  return RestStorage(name, { collection_slug: name })
}
