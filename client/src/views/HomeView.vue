<template>
  <div>
    <div class="list-group project-list">
      <router-link
        :to="`/project/${project.id}/${project.slug}`"
        v-for="project in projects"
        :key="project.id"
        class="list-group-item link"
      >
        {{ project.name }}
      </router-link>
      <div class="list-group-item">
        <button type="button" class="btn -primary" @click="adding = true">
          <i class="fa fa-plus" />
          Add New Project
        </button>
      </div>
    </div>
    <unrest-modal v-if="adding" :hide_actions="true" title="Add Project">
      <unrest-schema-form form_name="schema/project" :prepSchema="prepSchema" @success="success" />
    </unrest-modal>
  </div>
</template>

<script>
export default {
  __route: {
    path: '/',
  },
  data() {
    return { adding: null }
  },
  computed: {
    projects() {
      return this.$store.project.getPage()?.items
    },
  },
  methods: {
    prepSchema(schema) {
      delete schema.properties.data
      return schema
    },
    success() {
      this.$store.project.api.markStale()
      this.$store.project.getPage()?.items
      this.adding = false
    },
  },
}
</script>
