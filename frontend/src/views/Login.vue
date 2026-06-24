<template>
  <div class="login-page">
    <div class="login-box">
      <h2 class="title">图书管理系统</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="0" size="large">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" :prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" :prefix-icon="Key" show-password @keyup.enter="handleLogin" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="btn-block" :loading="loading" @click="handleLogin">登 录</el-button>
        </el-form-item>
        <div class="switch-mode">
          还没有账号？<el-link type="primary" @click="mode = 'register'">立即注册</el-link>
        </div>
      </el-form>

      <el-divider v-if="mode === 'register'" />

      <template v-if="mode === 'register'">
        <h3 class="subtitle">用户注册</h3>
        <el-form ref="regRef" :model="regForm" :rules="regRules" label-width="0" size="large">
          <el-form-item prop="username">
            <el-input v-model="regForm.username" placeholder="用户名" :prefix-icon="User" />
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="regForm.password" type="password" placeholder="密码" :prefix-icon="Key" show-password />
          </el-form-item>
          <el-form-item prop="email">
            <el-input v-model="regForm.email" placeholder="邮箱" :prefix-icon="Message" />
          </el-form-item>
          <el-form-item>
            <el-button type="success" class="btn-block" :loading="loading" @click="handleRegister">注 册</el-button>
          </el-form-item>
          <div class="switch-mode">
            已有账号？<el-link type="primary" @click="mode = 'login'">返回登录</el-link>
          </div>
        </el-form>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { User, Key, Message } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const auth = useAuthStore()
const mode = ref('login')
const loading = ref(false)
const formRef = ref()
const regRef = ref()

const form = reactive({ username: '', password: '' })
const regForm = reactive({ username: '', password: '', email: '' })

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}
const regRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  email: [{ type: 'email', message: '请输入正确邮箱', trigger: 'blur' }],
}

const handleLogin = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    await auth.login(form.username, form.password)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (e) {
    ElMessage.error(e.response?.data?.error || '登录失败')
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  await regRef.value.validate()
  loading.value = true
  try {
    await auth.register(regForm)
    ElMessage.success('注册成功')
    router.push('/')
  } catch (e) {
    ElMessage.error(e.response?.data?.error || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page { display: flex; justify-content: center; align-items: center; min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.login-box { background: white; padding: 40px; border-radius: 12px; width: 400px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
.title { text-align: center; color: #333; margin-bottom: 30px; font-size: 24px; }
.subtitle { text-align: center; color: #333; margin: 20px 0 15px; font-size: 18px; }
.btn-block { width: 100%; }
.switch-mode { text-align: center; color: #999; font-size: 14px; }
</style>
