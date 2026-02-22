<template>
  <div class="video-item">
    <video
      :src="video.file_path"
      autoplay
      muted
      loop
      playsinline
      controls
    ></video>

    <div class="info">
      <div>{{ video.title }}</div>
      <div v-if="video.target">
        {{ video.target }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  video: Object
})
</script>

<style>
.video-item {
  height: 100vh;
  position: relative;
}

video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info {
  position: absolute;
  bottom: 40px;
  left: 16px;
  color: white;
}
</style>
