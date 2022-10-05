<template>
  <div class="task-row">
    <i :class="icon" @click="clickActivity(activity)" />
    <div class="flex-grow">
      <div>{{ display_name }}</div>
      <div v-if="display_time">{{ display_time }}</div>
    </div>
    <div></div>
  </div>
</template>

<script>
import { formatDistanceToNowStrict } from 'date-fns'

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
  props: {
    task: Object,
    activity: Object,
  },
  data() {
    return { tick: 0 }
  },
  computed: {
    display_name() {
      return this.task?.name || this.activity?.name
    },
    display_time() {
      const { task } = this
      if (!task || !task.data.started || task.completed) {
        return null
      }
      const text = formatDistanceToNowStrict(new Date(this.task.data.started))
      this.watchTime(text)
      return text
    },
    icon() {
      return ['fa fa-2x link', getTaskIcon(this.task)]
    },
  },
  methods: {
    watchTime(text) {
      this.tick // eslint-disable-line
      const next = text.includes('second') ? 1 : 60
      setTimeout(() => (this.tick += 1), next * 1000)
    },
    clickActivity() {
      const { task, activity } = this
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
        name: activity.name,
      }
      this.$store.task.save(new_task)
    },
  },
}
</script>
