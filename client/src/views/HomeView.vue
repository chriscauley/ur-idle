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
        <button class="btn -primary" @click="$store.ui.openForm('schema/project')">
          <i class="fa fa-plus" />
          Add New Project
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  __route: {
    path: '/',
  },
  computed: {
    projects() {
      return this.$store.project.getPage()?.items
    },
  },
}
</script>
