<!--
  VideoItem.vue - 视频项组件
  
  功能说明：
    负责单个视频的播放和交互功能，包括点赞、收藏等操作
    采用乐观更新策略，先更新UI再发送API请求，提升用户体验
  
  组件通信：
    - Props: video (视频数据对象)
    - Emits: update-video (通知父组件更新视频数据)
  
  @author JobVideo Platform Team
  @version 1.0.0
-->

<template>
  <div class="video-item">
    <!-- 视频播放器 -->
    <video
      :key="video.id"
      :src="video.file_path"
      autoplay
      muted
      loop
      playsinline
      controls
    ></video>

    <!-- 视频信息：标题和目标 -->
    <div class="info">
      <div>{{ video.title }}</div>
      <div v-if="video.target">
        {{ video.target }}
      </div>
    </div>

    <!-- 交互按钮组：点赞、收藏、分享 -->
    <div class="actions">
      <!-- 点赞按钮 -->
      <div class="action-btn" @click="toggleLike">
        <div 
          class="icon" 
          :class="{ active: video.is_liked_by_me, loading: isLikeLoading }"
        >
          ❤
        </div>
        <div class="count">{{ video.like_count }}</div>
      </div>
      
      <!-- 收藏按钮 -->
      <div class="action-btn" @click="toggleFavorite">
        <div 
          class="icon" 
          :class="{ active: video.is_favorited_by_me, loading: isFavoriteLoading }"
        >
          ★
        </div>
        <div class="count">{{ video.favorite_count }}</div>
      </div>
      
      <!-- 分享按钮 -->
      <div class="action-btn">
        <div class="icon">⤴</div>
        <div class="count">分享</div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * VideoItem 组件脚本
 * 
 * 实现视频播放和交互功能，包括：
 * - 视频自动播放和循环
 * - 点赞/取消点赞功能（乐观更新）
 * - 收藏/取消收藏功能（乐观更新）
 * - 加载状态管理
 */

import { ref } from 'vue'
import { toggleVideoLike, toggleVideoFavorite } from '../api/video'

// ==================== Props 定义 ====================

/**
 * 组件属性
 * @property {Object} video - 视频数据对象
 * @property {number} video.id - 视频ID
 * @property {string} video.file_path - 视频文件路径
 * @property {string} video.title - 视频标题
 * @property {string} video.target - 视频目标（可选）
 * @property {boolean} video.is_liked_by_me - 当前用户是否已点赞
 * @property {number} video.like_count - 点赞总数
 * @property {boolean} video.is_favorited_by_me - 当前用户是否已收藏
 * @property {number} video.favorite_count - 收藏总数
 */
const props = defineProps({
  video: Object
})

// ==================== Emits 定义 ====================

/**
 * 组件事件
 * @event update-video - 通知父组件更新视频数据
 * @param {Object} data - 包含视频ID和需要更新的字段
 */
const emit = defineEmits(['update-video'])

// ==================== 响应式状态 ====================

/** 点赞操作加载状态 */
const isLikeLoading = ref(false)

/** 收藏操作加载状态 */
const isFavoriteLoading = ref(false)

// ==================== 工具函数 ====================

/**
 * 确保计数值有效
 * 
 * @description 验证计数值是否为有效数字，无效时返回0
 * @param {any} count - 待验证的计数值
 * @returns {number} 有效的计数值（0或正整数）
 */
function ensureValidCount(count) {
  return typeof count === 'number' && !isNaN(count) ? count : 0
}

/**
 * 更新视频数据
 * 
 * @description 向父组件发送更新事件，携带视频ID和需要更新的字段
 * @param {Object} data - 需要更新的视频字段
 * @example
 * updateVideo({ is_liked_by_me: true, like_count: 1 })
 */
function updateVideo(data) {
  emit('update-video', { id: props.video.id, ...data })
}

// ==================== 交互功能 ====================

/**
 * 切换点赞状态
 * 
 * @description 实现点赞/取消点赞功能，采用乐观更新策略：
 * 1. 立即更新UI（乐观更新）
 * 2. 发送API请求
 * 3. 成功：用服务器数据确认更新
 * 4. 失败：回滚到原始状态
 * 
 * @fires update-video
 */
function toggleLike() {
  // 防止重复点击
  if (isLikeLoading.value) return
  
  // 保存原始状态（用于失败时回滚）
  const originalLiked = Boolean(props.video.is_liked_by_me)
  const originalCount = ensureValidCount(props.video.like_count)
  
  // 计算新状态
  const newLiked = !originalLiked
  const newCount = newLiked ? originalCount + 1 : Math.max(0, originalCount - 1)
  
  // 乐观更新：立即更新UI
  updateVideo({ is_liked_by_me: newLiked, like_count: newCount })
  isLikeLoading.value = true
  
  // 发送API请求
  toggleVideoLike(props.video.id)
    .then(({ data }) => {
      // 成功：用服务器数据确认更新
      // 注意：Axios响应数据在res.data中，需要解构data
      updateVideo({ 
        is_liked_by_me: data.liked, 
        like_count: data.like_count 
      })
    })
    .catch(err => {
      // 失败：回滚到原始状态
      updateVideo({ is_liked_by_me: originalLiked, like_count: originalCount })
      console.error('点赞失败:', err)
    })
    .finally(() => {
      // 无论成功失败，都重置加载状态
      isLikeLoading.value = false
    })
}

/**
 * 切换收藏状态
 * 
 * @description 实现收藏/取消收藏功能，采用乐观更新策略：
 * 1. 立即更新UI（乐观更新）
 * 2. 发送API请求
 * 3. 成功：用服务器数据确认更新
 * 4. 失败：回滚到原始状态
 * 
 * @fires update-video
 */
function toggleFavorite() {
  // 防止重复点击
  if (isFavoriteLoading.value) return
  
  // 保存原始状态（用于失败时回滚）
  const originalFavorited = Boolean(props.video.is_favorited_by_me)
  const originalCount = ensureValidCount(props.video.favorite_count)
  
  // 计算新状态
  const newFavorited = !originalFavorited
  const newCount = newFavorited ? originalCount + 1 : Math.max(0, originalCount - 1)
  
  // 乐观更新：立即更新UI
  updateVideo({ is_favorited_by_me: newFavorited, favorite_count: newCount })
  isFavoriteLoading.value = true
  
  // 发送API请求
  toggleVideoFavorite(props.video.id)
    .then(({ data }) => {
      // 成功：用服务器数据确认更新
      // 注意：Axios响应数据在res.data中，需要解构data
      updateVideo({ 
        is_favorited_by_me: data.favorited, 
        favorite_count: data.favorite_count 
      })
    })
    .catch(err => {
      // 失败：回滚到原始状态
      updateVideo({ is_favorited_by_me: originalFavorited, favorite_count: originalCount })
      console.error('收藏失败:', err)
    })
    .finally(() => {
      // 无论成功失败，都重置加载状态
      isFavoriteLoading.value = false
    })
}
</script>

<style scoped>
/**
 * 视频项容器样式
 * 占满整个视口高度，作为定位上下文
 */
.video-item {
  height: 100vh;
  position: relative;
}

/**
 * 视频播放器样式
 * 填满容器，保持宽高比裁剪
 */
video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/**
 * 视频信息区域样式
 * 定位在左下角，白色文字
 */
.info {
  position: absolute;
  bottom: 40px;
  left: 16px;
  color: white;
  z-index: 10;
}

/**
 * 交互按钮组容器样式
 * 定位在右下角，垂直排列
 */
.actions {
  position: absolute;
  bottom: 40px;
  right: 16px;
  z-index: 10;
}

/**
 * 单个交互按钮样式
 * 垂直布局，居中对齐
 */
.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
  color: white;
}

/**
 * 图标样式
 * 默认白色，激活时红色，加载时半透明
 */
.icon {
  font-size: 28px;
  transition: all 0.3s ease;
  cursor: pointer;
  user-select: none;
}

.icon.active {
  color: #ff2d55;
  transform: scale(1.2);
}

.icon.loading {
  opacity: 0.5;
  pointer-events: none;
}

/**
 * 计数文字样式
 */
.count {
  font-size: 12px;
  margin-top: 4px;
}
</style>
