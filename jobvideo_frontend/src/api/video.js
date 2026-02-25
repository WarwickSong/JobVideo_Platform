import axios from 'axios'

const api = axios.create({
  baseURL: '/api', // 使用相对路径
  headers: {
    Authorization: 'Bearer test-token'
  }
})

export function fetchVideoFeed() {
  return api.get('/video/feed')
}

export function toggleVideoLike(videoId) {
  return api.post(`/video/${videoId}/like`)
}

export function toggleVideoFavorite(videoId) {
  return api.post(`/video/${videoId}/favorite`)
}
