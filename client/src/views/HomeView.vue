<template>
  <task-list />
</template>

<script>
import TaskList from '@/components/TaskList.vue'

export default {
  components: { TaskList },
  __route: {
    path: '/',
  },
}
</script>
