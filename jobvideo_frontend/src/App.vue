<template>
  <DemoLoginPanel
    :current-user="currentUser"
    :loading="isLoggingIn"
    :message="loginMessage"
    :is-error="isLoginError"
    @login="handleDemoLogin"
    @logout="handleLogout"
  />
  <Feed />
</template>

<script setup>
import { onMounted, ref } from 'vue'
import DemoLoginPanel from './components/DemoLoginPanel.vue'
import Feed from './views/Feed.vue'
import { fetchCurrentUser, login } from './api/video'

const currentUser = ref(null)
const isLoggingIn = ref(false)
const loginMessage = ref('')
const isLoginError = ref(false)

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return

  try {
    const { data } = await fetchCurrentUser()
    currentUser.value = data
    loginMessage.value = `已登录：${data.username}`
    isLoginError.value = false
  } catch (error) {
    localStorage.removeItem('access_token')
    currentUser.value = null
  }
})

async function handleDemoLogin(account) {
  isLoggingIn.value = true
  loginMessage.value = ''
  isLoginError.value = false

  try {
    const { data } = await login({
      username: account.username,
      password: account.password
    })

    localStorage.setItem('access_token', data.access_token)
    const me = await fetchCurrentUser()
    currentUser.value = me.data
    loginMessage.value = `登录成功：${me.data.username}`
  } catch (error) {
    currentUser.value = null
    localStorage.removeItem('access_token')
    loginMessage.value = error?.response?.data?.detail || '登录失败，请先在后端创建演示账号'
    isLoginError.value = true
  } finally {
    isLoggingIn.value = false
  }
}

function handleLogout() {
  localStorage.removeItem('access_token')
  currentUser.value = null
  loginMessage.value = '已退出登录'
  isLoginError.value = false
}
</script>
