<template>
  <div :class="css.wrapper">
    <i :class="css.icon" @click="clickActivity(activity)" />
    <div class="task-row__display">
      <div>{{ display_name }}</div>
      <div v-if="display_time">{{ display_time }}</div>
    </div>
    <unrest-dropdown :items="dropdown_items" placement="bottom-end">
      <div class="btn -light">
        <i class="fa fa-ellipsis-v" />
      </div>
    </unrest-dropdown>
    <unrest-form v-if="form" v-bind="form" />
  </div>
</template>

<script>
import { debounce } from 'lodash'

import { format, formatDistanceToNowStrict, formatDistanceStrict } from 'date-fns'

export default {
  props: {
    task: Object,
    activity: Object,
  },
  data() {
    return { tick: 0, edit_task: false }
  },
  computed: {
    dropdown_items() {
      const { activity, task } = this
      const { activity_id } = this.$route.params
      const { openForm } = this.$store.ui
      const actions = [
        activity && {
          text: 'Edit Activity',
          click: () => openForm(`schema/activity/${activity.id}`),
        },
        task?.data.started &&
          !task.completed && {
            text: 'Stop Task',
            click: () => {
              delete task.data.started
              this.$store.task.save(task)
            },
          },
        task && {
          text: 'Edit Task',
          click: () => (this.edit_task = true),
        },
        activity &&
          !activity_id && {
            text: 'View Activity',
            to: `/app/activity/${activity.id}/${activity.slug}/`,
          },
      ]
      return actions.filter(Boolean)
    },
    display_name() {
      return this.task?.name || this.activity?.name
    },
    timer_active() {
      const { task } = this
      return task && task.data.started && !task.completed
    },
    display_time() {
      const { task, timer_active } = this
      if (task && task.data.started && task.completed) {
        const started = new Date(task.data.started)
        const duration = formatDistanceStrict(started, new Date(task.completed))
        return `${duration} on ${format(started, 'yyyy-MM-dd')}`
      }
      if (!timer_active) {
        return null
      }
      const text = formatDistanceToNowStrict(new Date(task.data.started))
      this.watchTime(text)
      return text
    },
    form() {
      if (!this.timer_active && !this.edit_task) {
        return null
      }
      const { task, activity = {} } = this
      const { measurements = [], texts = [] } = activity?.data || []
      const form = {
        state: {},
        schema: { type: 'object', properties: {}, title: null },
        onInput: this.save,
      }
      if (this.edit_task) {
        form.schema.properties.completed = {
          type: 'string',
          format: 'date-time',
          default: task.completed,
        }
        form.schema.properties.started = {
          type: 'string',
          format: 'date-time',
          default: task.data.started,
        }
      }
      texts.forEach((name) => {
        form.schema.properties[name] = { type: 'string', default: task.data[name] }
        form.state[name] = task.data[name]
      })
      measurements.forEach((name) => {
        form.schema.properties[name] = { type: 'number', default: task.data[name] }
        form.state[name] = task.data[name]
      })
      if (Object.keys(form.schema.properties).length === 0) {
        return null
      }
      return form
    },
    css() {
      const { task } = this
      let icon
      if (!task) {
        icon = 'fa-frown-o link'
      } else if (task.completed) {
        icon = 'fa fa-check-square-o'
      } else if (task.data.started) {
        icon = 'fa-spinner fa-spin link'
      } else {
        icon = 'fa-square-o link'
      }
      return {
        wrapper: ['task-row'],
        icon: ['fa fa-2x', icon],
      }
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
      } else if (task.completed) {
        return
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
    save: debounce(function save({ ...state }) {
      const { task } = this
      if (state.completed) {
        task.completed = state.completed
        delete state.completed
      }
      Object.assign(task.data, state)
      this.$store.task.save(task)
    }, 500),
  },
}
</script>
