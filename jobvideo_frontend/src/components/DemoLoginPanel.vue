<template>
  <aside class="demo-login-panel">
    <div class="demo-login-panel__header">
      <div>
        <p class="demo-login-panel__eyebrow">演示登录</p>
        <h2>选择一个示例账号直接进入</h2>
      </div>
      <button
        v-if="currentUser"
        class="demo-login-panel__logout"
        type="button"
        @click="$emit('logout')"
      >
        退出登录
      </button>
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
defineProps({
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

.demo-login-panel__logout {
  padding: 8px 12px;
  border: 0;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
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
}
</style>
