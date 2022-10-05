<template>
  <div v-if="project">
    <h2>{{ project.name }}</h2>
    <div class="list-group">
      <div
        v-for="activity in activities"
        :key="activity.id"
        class="list-group-item">
        <i :class="activity.icon" @click="clickActivity(activity)" />
        <span class="flex-grow">{{ activity.name }}</span>
      </div>
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

const getTaskIcon = (task) => {
  if (!task) {
    return 'fa-frown-o'
  } else if (task.data.started) {
    return 'fa-spinner fa-spin'
  } else {
    return 'fa-square-o'
  }
}

export default {
  __route: {
    path: '/project/:project_id/:project_slug/'
  },
  computed: {
    project() {
      return this.$store.project.getOne(this.$route.params.project_id)
    },
    activities() {
      const { project_id } = this.$route.params
      const query = { project: project_id }
      const activities = this.$store.activity
            .getPage({per_page: 0, query})?.items || []
            .filter(a => a.project === this.project.id)
      return activities.map(({ ...activity }) => {
        activity.tasks = this.tasks.filter(t => t.activity === activity.id)
        activity.task = activity.tasks.find(t => !t.completed)
        activity.icon = ['fa fa-2x link', getTaskIcon(activity.task)]
        return activity
      })
    },
    tasks() {
      const { project_id } = this.$route.params
      const query = { project: project_id }
      return this.$store.task.getPage({ query })?.items || []
    }
  },
  methods: {
    clickActivity(activity) {
      const { task } = activity
      if (!task) {
        this.makeNextTask(activity)
      } else if (!task.data.started) {
        this.$store.task.save({
          ...task,
          data: {
            ...task.data,
            started: new Date(),
          },
        })
      } else {
        this.$store.task.save({
          ...task,
          completed: new Date(),
        })
      }
    },
    makeNextTask(activity) {
      const new_task = {
        activity: activity.id,
        project: activity.project,
        name: activity.name
      }
      this.$store.task.save(new_task)
    }
  }
}
</script>
