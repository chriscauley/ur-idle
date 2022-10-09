<template>
  <div v-if="activity">
    <h2>Activity: {{ activity.name }}</h2>
    <div class="list-group">
      <task-row
        v-for="task in tasks"
        :key="task.id"
        :activity="activity"
        :task="task"
        class="list-group-item"
      />
    </div>
  </div>
</template>

<script>
import TaskRow from '@/components/TaskRow'

export default {
  __route: {
    path: '/app/activity/:activity_id/:activity_slug/',
  },
  components: { TaskRow },
  computed: {
    activity() {
      return this.$store.activity.getOne(this.$route.params.activity_id)
    },
    tasks() {
      const { activity_id } = this.$route.params
      const query = { per_page: 0, activity_id }
      return this.$store.task.getPage({ query })?.items
    },
  },
}
</script>
