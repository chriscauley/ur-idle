<template>
  <div :class="css.wrapper">
    <i :class="css.icon" @click="clickActivity(activity)" />
    <div class="task-row__display">
      <div>{{ display_name }}</div>
      <div v-if="display_time">{{ display_time }}</div>
      <unrest-form v-if="form" v-bind="form" />
    </div>
    <unrest-dropdown :items="dropdown_items" placement="bottom-end">
      <div class="btn -light">
        <i class="fa fa-ellipsis-v" />
      </div>
    </unrest-dropdown>
  </div>
</template>

<script>
import { debounce } from 'lodash'

import { formatDistanceToNowStrict } from 'date-fns'

export default {
  props: {
    task: Object,
    activity: Object,
  },
  data() {
    return { tick: 0 }
  },
  computed: {
    dropdown_items() {
      const { activity, task } = this
      const { openForm } = this.$store.ui
      const actions = [
        activity && {
          text: 'Edit Activity',
          click: () => openForm(`schema/activity/${activity.id}`),
        },
        task?.data.started && {
          text: 'Stop Task',
          click: () => {
            delete task.data.started
            this.$store.task.save(task)
          },
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
      if (!timer_active) {
        return null
      }
      const text = formatDistanceToNowStrict(new Date(task.data.started))
      this.watchTime(text)
      return text
    },
    form() {
      if (!this.timer_active) {
        return null
      }
      const { task, activity = {} } = this
      const { measurements = [], texts = [] } = activity?.data || []
      if (measurements.length + texts.length === 0) {
        return null
      }
      const form = {
        state: {},
        schema: { type: 'object', properties: {}, title: null },
        onInput: this.save,
      }
      texts.forEach((name) => {
        form.schema.properties[name] = { type: 'string', default: task.data[name] }
        form.state[name] = task.data[name]
      })
      measurements.forEach((name) => {
        form.schema.properties[name] = { type: 'number', default: task.data[name] }
        form.state[name] = task.data[name]
      })
      return form
    },
    css() {
      const { task } = this
      let icon, wrapper
      if (!task) {
        icon = 'fa-frown-o'
      } else if (task.data.started) {
        icon = 'fa-spinner fa-spin'
        wrapper = '-started'
      } else {
        icon = 'fa-square-o'
      }
      return {
        wrapper: ['task-row', wrapper],
        icon: ['fa fa-2x link', icon],
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
    save: debounce(function save(state) {
      const { task } = this
      Object.assign(task.data, state)
      this.$store.task.save(task)
    }, 500),
  },
}
</script>
