<template>
  <div>
    <div class="list-group task-list">
      <div v-for="task in tasks" :key="task.id" class="list-group-item">
        <i :class="css.task(task)" @click="click(task)" />
        <div class="flex-grow">{{ task.name }}</div>
      </div>
    </div>
    <unrest-form v-if="adding" :schema="schema" @submit="submit" />
    <div v-else>
      <div @click="adding = true" class="btn -primary">
        <i class="fa fa-plus" />
        Add Task
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    const schema = {
      type: 'object',
      properties: {
        name: {
          type: 'string',
        },
        add_activity: {
          type: 'boolean',
        },
      },
    }
    return { adding: null, schema }
  },
  computed: {
    css() {
      return {
        task: (task) => {
          let icon = task.completed ? 'check-square-o' : 'square-o'
          if (task.data.started) {
            icon = 'spinner fa-spin'
          }
          return `fa -action fa-${icon}`
        },
      }
    },
    tasks() {
      return this.$store.task.getPage()?.items
    },
  },
  methods: {
    submit(data) {
      this.$store.task.save(data)
    },
    click(task) {
      if (!task.data.started) {
        task.data.started = new Date()
      } else {
        delete task.data.started
        task.completed = new Date()
      }
      this.$store.task.save(task)
    },
  },
}
</script>
