<template>
  <div>
    <div @click="adding = True" class="btn -primary">
      <i class="fa fa-plus" />
      Add Task
    </div>
    <unrest-form :schema="schema" @submit="submit" />
  </div>
</template>

<script>
import { getClient } from '@unrest/vue-storage'

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
        }
      },
    }
    return { adding: null, schema }
  },
  methods: {
    submit(data) {
      this.$store.task.save(data)
    },
  },
}
</script>
