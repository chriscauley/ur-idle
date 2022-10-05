<template>
  <div class="app-wrapper">
    <site-nav />
    <router-view class="app-content" />
    <unrest-ui />
    <unrest-modal
      v-if="form"
      :hide_actions="true"
      :title="form.title"
      @close="$store.ui.openForm(null)"
    >
      <unrest-schema-form :form_name="form.name" :prepSchema="prepSchema" @success="success" />
    </unrest-modal>
  </div>
</template>

<script>
import { startCase } from 'lodash'

import SiteNav from '@/components/SiteNav'

export default {
  components: { SiteNav },
  computed: {
    form() {
      const { modal_form } = this.$store.ui.state
      if (!modal_form) {
        return null
      }
      const [_, model_name, id] = modal_form.split('/')
      let title = `${id ? 'Edit' : 'Add'} ${startCase(model_name)}`
      return { title, model_name, id, name: modal_form }
    },
  },
  methods: {
    prepSchema(schema) {
      delete schema.properties.data
      const { project_id } = this.$route.params
      if (schema.properties.project && project_id) {
        schema.properties.project.default = parseInt(project_id)
        schema.properties.project.format = 'hidden'
      }
      return schema
    },
    success() {
      const { model_name } = this.form
      this.$store[model_name].api.markStale()
      this.$store[model_name].getPage()?.items
      const query = { ...this.$route.query }
      delete query.modal_form
      this.$store.ui.openForm(null)
    },
  },
}
</script>
