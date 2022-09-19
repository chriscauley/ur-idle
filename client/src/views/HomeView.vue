<template>
  <div>
    <div class="list-group task-list">
      <div v-for="task in tasks" :key="task.id" class="list-group-item">
        <i :class="css.task(task)" />
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
  __route: {
    path: '/',
  },
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
        task: (t) => `fa -action fa-${t.completed ? 'check-square-o' : 'square-o'}`,
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
  },
}
</script>
