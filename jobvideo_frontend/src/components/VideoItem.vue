<template>
  <div class="video-item">
    <video
      :key="video.id"
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

    <!-- 交互按钮 -->
    <div class="actions">
      <div class="action-btn" @click="toggleLike">
        <div class="icon" :class="{ active: video.is_liked_by_me }">❤</div>
        <div class="count">{{ video.like_count }}</div>
      </div>
      <div class="action-btn" @click="toggleFavorite">
        <div class="icon" :class="{ active: video.is_favorited_by_me }">★</div>
        <div class="count">{{ video.favorite_count }}</div>
      </div>
      <div class="action-btn">
        <div class="icon">⤴</div>
        <div class="count">分享</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { toggleVideoLike, toggleVideoFavorite } from '../api/video'

const props = defineProps({
  video: Object
})

function toggleLike() {
  toggleVideoLike(props.video.id)
    .then(res => {
      // 更新本地状态
      props.video.is_liked_by_me = res.liked
      props.video.like_count = res.like_count
    })
}

function toggleFavorite() {
  toggleVideoFavorite(props.video.id)
    .then(res => {
      // 更新本地状态
      props.video.is_favorited_by_me = res.favorited
      props.video.favorite_count = res.favorite_count
    })
}
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
  z-index: 10;
}

.actions {
  position: absolute;
  bottom: 40px;
  right: 16px;
  z-index: 10;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
  color: white;
}

.icon {
  font-size: 28px;
  margin-bottom: 4px;
}

.icon.active {
  color: #ff4757;
}

.count {
  font-size: 14px;
}
</style>