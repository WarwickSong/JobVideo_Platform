<template>
  <div class="feed">
    <VideoItem
      v-if="videos.length"
      :video="videos[currentIndex]"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchVideoFeed } from '../api/video'
import VideoItem from '../components/VideoItem.vue'

const videos = ref([])
const currentIndex = ref(0)

onMounted(async () => {
  const res = await fetchVideoFeed()
  videos.value = res.data
})
</script>

<style>
.feed {
  height: 100vh;
  overflow: hidden;
}
</style>
