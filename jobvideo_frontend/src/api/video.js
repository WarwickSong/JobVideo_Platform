import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000', // 改成你的后端地址
  headers: {
    Authorization: 'Bearer test-token'
  }
})

export function fetchVideoFeed() {
  return api.get('/video/feed')
}
