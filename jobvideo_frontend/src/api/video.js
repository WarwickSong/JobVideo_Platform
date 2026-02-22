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
