<template>
  <div
    class="feed"
    @touchstart="onTouchStart"
    @touchend="onTouchEnd"
  >
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

let startY = 0
let endY = 0

onMounted(async () => {
  const res = await fetchVideoFeed()
  videos.value = res.data
})

function onTouchStart(e) {
  startY = e.touches[0].clientY
}

function onTouchEnd(e) {
  endY = e.changedTouches[0].clientY
  handleSwipe()
}

function handleSwipe() {
  const distance = startY - endY

  // 向上滑（看下一个）
  if (distance > 50) {
    if (currentIndex.value < videos.value.length - 1) {
      currentIndex.value++
    }
  }

  // 向下滑（看上一个）
  if (distance < -50) {
    if (currentIndex.value > 0) {
      currentIndex.value--
    }
  }
}
</script>

<style>
.feed {
  height: 100vh;
  overflow: hidden;
}
</style>