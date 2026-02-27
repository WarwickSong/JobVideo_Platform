<!--
  Feed.vue - 视频流页面
  
  功能说明：
    主页面组件，负责展示视频流，实现上下滑动切换视频的功能
    支持触摸手势导航，管理视频列表状态
  
  核心功能：
    - 视频列表加载和展示
    - 上下滑动切换视频
    - 视频状态同步更新
    - 平滑过渡动画
  
  @author JobVideo Platform Team
  @version 1.0.0
-->

<template>
  <div
    class="feed"
    @touchstart="onTouchStart"
    @touchend="onTouchEnd"
  >
    <!-- 视频切换过渡动画 -->
    <transition name="slide" mode="out-in">
      <VideoItem
        v-if="videos.length"
        :key="videos[currentIndex].id"
        :video="videos[currentIndex]"
        @update-video="updateVideo"
      />
    </transition>
  </div>
</template>

<script setup>
/**
 * Feed 页面脚本
 * 
 * 实现视频流的核心功能：
 * - 加载视频列表数据
 * - 处理触摸手势
 * - 管理当前视频索引
 * - 同步视频状态更新
 */

import { ref, onMounted } from 'vue'
import { fetchVideoFeed } from '../api/video'
import VideoItem from '../components/VideoItem.vue'

// ==================== 响应式状态 ====================

/** 视频列表数据 */
const videos = ref([])

/** 当前显示的视频索引 */
const currentIndex = ref(0)

// ==================== 触摸手势状态 ====================

/** 触摸开始时的Y坐标 */
let startY = 0

/** 触摸开始时的X坐标 */
let startX = 0

/** 触摸结束时的Y坐标 */
let endY = 0

/** 触摸结束时的X坐标 */
let endX = 0

// ==================== 生命周期钩子 ====================

/**
 * 组件挂载时加载视频列表
 * 
 * @description 从后端API获取视频数据并填充到videos数组
 */
onMounted(async () => {
  const res = await fetchVideoFeed()
  videos.value = res.data
})

// ==================== 触摸事件处理 ====================

/**
 * 触摸开始事件处理
 * 
 * @description 记录触摸起始位置
 * @param {TouchEvent} e - 触摸事件对象
 */
function onTouchStart(e) {
  startY = e.touches[0].clientY
  startX = e.touches[0].clientX
}

/**
 * 触摸结束事件处理
 * 
 * @description 记录触摸结束位置，触发滑动处理
 * @param {TouchEvent} e - 触摸事件对象
 */
function onTouchEnd(e) {
  endY = e.changedTouches[0].clientY
  endX = e.changedTouches[0].clientX
  handleSwipe()
}

/**
 * 处理滑动手势
 * 
 * @description 判断滑动方向和距离，执行视频切换
 * 
 * 滑动检测逻辑：
 * 1. 计算垂直和水平滑动距离
 * 2. 判断是否为垂直滑动（垂直距离 > 水平距离）
 * 3. 判断滑动方向（上滑/下滑）
 * 4. 判断是否超过阈值（50px）
 * 5. 执行视频切换
 */
function handleSwipe() {
  // 计算滑动距离
  const distanceY = startY - endY
  const distanceX = startX - endX
  
  // 滑动阈值：超过50px才触发切换
  const threshold = 50

  // 判断是否为垂直滑动（垂直距离 > 水平距离）
  if (Math.abs(distanceY) > Math.abs(distanceX)) {
    if (distanceY > threshold) {
      // 上滑：切换到下一个视频
      if (currentIndex.value < videos.value.length - 1) {
        currentIndex.value++
      }
    } else if (distanceY < -threshold) {
      // 下滑：切换到上一个视频
      if (currentIndex.value > 0) {
        currentIndex.value--
      }
    }
  }
}

// ==================== 状态更新 ====================

/**
 * 更新视频数据
 * 
 * @description 接收子组件的更新事件，同步更新视频列表中的数据
 * 
 * 实现原理：
 * - 使用map创建新数组，确保Vue检测到变化
 * - 通过id匹配找到需要更新的视频
 * - 使用展开运算符合并更新数据
 * 
 * @param {Object} updatedVideo - 包含视频ID和需要更新的字段
 * @example
 * updateVideo({ id: 1, is_liked_by_me: true, like_count: 1 })
 */
function updateVideo(updatedVideo) {
  const index = videos.value.findIndex(v => v.id === updatedVideo.id)
  if (index !== -1) {
    // 创建新数组以确保Vue检测到变化
    // 使用map方法替换指定索引的视频数据
    videos.value = videos.value.map((v, i) => 
      i === index ? { ...v, ...updatedVideo } : v
    )
  }
}
</script>

<style scoped>
/**
 * 视频流容器样式
 * 占满整个视口高度，隐藏溢出内容
 */
.feed {
  height: 100vh;
  overflow: hidden;
}

/**
 * 视频切换动画 - 进入和离开的过渡效果
 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

/**
 * 视频切换动画 - 进入起始状态
 * 从下方淡入
 */
.slide-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

/**
 * 视频切换动画 - 离开结束状态
 * 向上方淡出
 */
.slide-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}
</style>
