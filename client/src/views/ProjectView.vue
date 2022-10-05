<template>
  <div v-if="project">
    <h2>{{ project.name }}</h2>
    <div class="list-group">
      <task-row
        v-for="activity in activities"
        :key="activity.id"
        class="list-group-item"
        :activity="activity"
        :task="activity.task"
      />
      <div class="list-group-item">
        <button class="btn -primary" @click="$store.ui.openForm('schema/activity')">
          <i class="fa fa-plus" />
          Add New Activity
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import TaskRow from '@/components/TaskRow.vue'

export default {
  __route: {
    path: '/project/:project_id/:project_slug/',
  },
  components: { TaskRow },
  computed: {
    project() {
      return this.$store.project.getOne(this.$route.params.project_id)
    },
    activities() {
      const { project_id } = this.$route.params
      const query = { project: project_id }
      const activities =
        this.$store.activity.getPage({ per_page: 0, query })?.items ||
        [].filter((a) => a.project === this.project.id)
      return activities.map(({ ...activity }) => {
        activity.tasks = this.tasks.filter((t) => t.activity === activity.id)
        activity.task = activity.tasks.find((t) => !t.completed)
        return activity
      })
    },
    tasks() {
      const { project_id } = this.$route.params
      const query = { project: project_id }
      return this.$store.task.getPage({ query })?.items || []
    },
  },
}
</script>
