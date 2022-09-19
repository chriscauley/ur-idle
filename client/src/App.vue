<template>
  <div class="app-wrapper">
    <site-nav />
    <router-view class="app-content" />
    <unrest-ui />
  </div>
</template>

<script>
import SiteNav from '@/components/SiteNav'

export default {
  components: { SiteNav },
}
</script>
