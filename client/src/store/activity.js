import { RestStorage } from '@unrest/vue-storage'

export default () => {
  const name = 'schema/activity'
  return RestStorage(name, { collection_slug: name })
}
