<template>
  <!-- 已登录且折叠状态：显示迷你用户按钮 -->
  <button
    v-if="currentUser && collapsed"
    class="demo-login-avatar"
    type="button"
    @click="collapsed = false"
  >
    <span class="demo-login-avatar__initial">{{ avatarInitial }}</span>
  </button>

  <!-- 展开状态：显示完整面板 -->
  <aside v-else class="demo-login-panel">
    <div class="demo-login-panel__header">
      <div>
        <p class="demo-login-panel__eyebrow">演示登录</p>
        <h2>选择一个示例账号直接进入</h2>
      </div>
      <div class="demo-login-panel__header-actions">
        <button
          v-if="currentUser"
          class="demo-login-panel__minimize"
          type="button"
          @click="collapsed = true"
        >
          —
        </button>
        <button
          v-if="currentUser"
          class="demo-login-panel__logout"
          type="button"
          @click="$emit('logout')"
        >
          退出登录
        </button>
      </div>
    </div>

    <div v-if="currentUser" class="demo-login-panel__current">
      <div>当前账号：{{ currentUser.username }}</div>
      <div>角色：{{ currentUser.role }}</div>
    </div>

    <div v-if="message" class="demo-login-panel__message" :class="{ error: isError }">
      {{ message }}
    </div>

    <div class="demo-login-panel__accounts">
      <button
        v-for="account in demoAccounts"
        :key="account.username"
        class="demo-login-panel__account"
        type="button"
        :disabled="loading"
        @click="$emit('login', account)"
      >
        <div class="demo-login-panel__account-top">
          <strong>{{ account.label }}</strong>
          <span>{{ account.roleLabel }}</span>
        </div>
        <div>用户名：{{ account.username }}</div>
        <div>密码：{{ account.password }}</div>
      </button>
    </div>

    <p class="demo-login-panel__hint">
      这一阶段采用演示账号模式，先跳过注册流程开发。
    </p>
  </aside>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  currentUser: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  message: {
    type: String,
    default: ''
  },
  isError: {
    type: Boolean,
    default: false
  }
})

defineEmits(['login', 'logout'])

// 面板折叠状态：登录后自动折叠，点击迷你按钮展开
const collapsed = ref(false)

// 监听用户状态：登录成功后自动折叠，退出后恢复展开
watch(() => props.currentUser, (val) => {
  collapsed.value = val ? true : false
})

// 获取用户名的首字符作为头像文字
const avatarInitial = computed(() => {
  if (!props.currentUser) return ''
  return props.currentUser.username.charAt(0).toUpperCase()
})

const demoAccounts = [
  {
    label: '求职者示例 A',
    roleLabel: '求职者',
    username: 'demo_seeker',
    password: 'Demo123456'
  },
  {
    label: '招聘方示例',
    roleLabel: '招聘方',
    username: 'demo_employer',
    password: 'Demo123456'
  },
  {
    label: '求职者示例 B',
    roleLabel: '求职者',
    username: 'demo_seeker_2',
    password: 'Demo123456'
  }
]
</script>

<style scoped>
.demo-login-panel {
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 20;
  width: min(360px, calc(100vw - 32px));
  padding: 18px;
  border-radius: 20px;
  background: rgba(10, 18, 30, 0.78);
  color: #f3f7fb;
  backdrop-filter: blur(16px);
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.28);
}

.demo-login-panel__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.demo-login-panel__header h2 {
  margin: 4px 0 0;
  font-size: 20px;
  line-height: 1.2;
}

.demo-login-panel__eyebrow {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #9dc4ff;
}

.demo-login-panel__header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.demo-login-panel__minimize {
  padding: 8px 10px;
  border: 0;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  color: #9dc4ff;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  transition: background 0.2s ease;
}

.demo-login-panel__minimize:hover {
  background: rgba(255, 255, 255, 0.18);
}

.demo-login-panel__logout {
  padding: 8px 12px;
  border: 0;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  cursor: pointer;
  transition: background 0.2s ease;
}

.demo-login-panel__logout:hover {
  background: rgba(255, 255, 255, 0.22);
}

.demo-login-panel__current,
.demo-login-panel__message {
  margin-top: 14px;
  padding: 10px 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.09);
  font-size: 14px;
}

.demo-login-panel__message.error {
  background: rgba(255, 92, 92, 0.18);
}

.demo-login-panel__accounts {
  display: grid;
  gap: 10px;
  margin-top: 14px;
}

.demo-login-panel__account {
  padding: 14px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.08);
  color: inherit;
  text-align: left;
}

.demo-login-panel__account-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.demo-login-panel__account-top span {
  font-size: 12px;
  color: #b7d3ff;
}

.demo-login-panel__hint {
  margin: 12px 0 0;
  font-size: 12px;
  color: #bfd2ea;
}

/**
 * 折叠状态：迷你用户头像按钮
 * 显示用户名的首字符，点击展开完整面板
 */
.demo-login-avatar {
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 20;
  width: 48px;
  height: 48px;
  border: 0;
  border-radius: 999px;
  background: rgba(10, 18, 30, 0.78);
  backdrop-filter: blur(16px);
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.28);
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
}

.demo-login-avatar:hover {
  background: rgba(20, 32, 48, 0.88);
  transform: scale(1.08);
}

.demo-login-avatar__initial {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  font-size: 20px;
  font-weight: 600;
  color: #9dc4ff;
}

@media (max-width: 640px) {
  .demo-login-panel {
    padding: 14px;
    top: 10px;
    left: 10px;
    width: min(340px, calc(100vw - 20px));
  }

  .demo-login-panel__header {
    flex-direction: column;
  }

  .demo-login-avatar {
    top: 10px;
    left: 10px;
    width: 42px;
    height: 42px;
  }

  .demo-login-avatar__initial {
    font-size: 17px;
  }
}
</style>
