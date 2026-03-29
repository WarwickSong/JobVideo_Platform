/**
 * video.js - 视频相关API接口
 * 
 * 功能说明：
 *   封装所有与视频相关的HTTP请求，包括视频列表获取、点赞、收藏等操作
 *   使用Axios作为HTTP客户端，统一管理API请求配置
 * 
 * API列表：
 *   - fetchVideoFeed: 获取视频流列表
 *   - toggleVideoLike: 切换视频点赞状态
 *   - toggleVideoFavorite: 切换视频收藏状态
 * 
 * @author JobVideo Platform Team
 * @version 1.0.0
 */

import axios from 'axios'

// ==================== Axios实例配置 ====================

/**
 * Axios API实例
 * 
 * 配置说明：
 * - baseURL: '/api' - 使用相对路径，便于开发和生产环境切换
 * - headers.Authorization - 携带认证令牌，用于身份验证
 * 
 * 注意：当前使用测试令牌，生产环境应从localStorage或Vuex/Pinia获取真实令牌
 */
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api'

const api = axios.create({
  baseURL: apiBaseUrl
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ==================== API接口函数 ====================

/**
 * 获取视频流列表
 * 
 * @description 从后端获取视频列表数据，用于Feed页面展示
 * @returns {Promise<AxiosResponse>} Axios响应对象
 * 
 * @example
 * const res = await fetchVideoFeed()
 * const videos = res.data // 视频列表数据
 * 
 * 响应数据结构：
 * {
 *   data: [
 *     {
 *       id: 1,
 *       title: '视频标题',
 *       file_path: '/videos/xxx.mp4',
 *       like_count: 10,
 *       is_liked_by_me: false,
 *       favorite_count: 5,
 *       is_favorited_by_me: false
 *     },
 *     ...
 *   ]
 * }
 */
export function fetchVideoFeed() {
  return api.get('/video/feed')
}

/**
 * 切换视频点赞状态
 * 
 * @description 对视频进行点赞或取消点赞操作（toggle逻辑）
 * @param {number} videoId - 视频ID
 * @returns {Promise<AxiosResponse>} Axios响应对象
 * 
 * @example
 * const res = await toggleVideoLike(123)
 * const { liked, like_count } = res.data
 * 
 * 响应数据结构：
 * {
 *   data: {
 *     liked: true,        // 当前用户是否已点赞
 *     like_count: 11      // 视频总点赞数
 *   }
 * }
 * 
 * 注意：
 * - 响应数据在res.data中，需要通过解构获取
 * - liked字段为boolean类型，表示当前点赞状态
 * - like_count字段为number类型，表示总点赞数
 */
export function toggleVideoLike(videoId) {
  return api.post(`/video/${videoId}/like`)
}

/**
 * 切换视频收藏状态
 * 
 * @description 对视频进行收藏或取消收藏操作（toggle逻辑）
 * @param {number} videoId - 视频ID
 * @returns {Promise<AxiosResponse>} Axios响应对象
 * 
 * @example
 * const res = await toggleVideoFavorite(123)
 * const { favorited, favorite_count } = res.data
 * 
 * 响应数据结构：
 * {
 *   data: {
 *     favorited: true,      // 当前用户是否已收藏
 *     favorite_count: 6     // 视频总收藏数
 *   }
 * }
 * 
 * 注意：
 * - 响应数据在res.data中，需要通过解构获取
 * - favorited字段为boolean类型，表示当前收藏状态
 * - favorite_count字段为number类型，表示总收藏数
 */
export function toggleVideoFavorite(videoId) {
  return api.post(`/video/${videoId}/favorite`)
}

export function login(payload) {
  return api.post('/auth/login', payload)
}

export function fetchCurrentUser() {
  return api.get('/auth/me')
}
