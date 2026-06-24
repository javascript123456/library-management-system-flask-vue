<template>
  <el-container class="layout">
    <el-aside width="220px">
      <div class="logo">图书管理系统</div>
      <el-menu :default-active="$route.path" router background-color="#1a1a2e" text-color="#ccc" active-text-color="#fff">
        <el-menu-item index="/">
          <el-icon><Odometer /></el-icon>
          <span>首页概览</span>
        </el-menu-item>
        <el-menu-item index="/books">
          <el-icon><Reading /></el-icon>
          <span>图书管理</span>
        </el-menu-item>
        <el-menu-item v-if="auth.isAdmin" index="/borrow">
          <el-icon><Tickets /></el-icon>
          <span>借阅管理</span>
        </el-menu-item>
        <el-menu-item index="/my-borrow">
          <el-icon><Document /></el-icon>
          <span>我的借阅</span>
        </el-menu-item>
        <el-menu-item v-if="auth.isAdmin" index="/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <span class="greeting">欢迎，{{ auth.user?.username }} ({{ auth.isAdmin ? '管理员' : '普通用户' }})</span>
        <el-button type="danger" size="small" @click="handleLogout">退出登录</el-button>
      </el-header>
      <el-main><router-view /></el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { Odometer, Reading, Tickets, Document, User } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'

const auth = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  ElMessageBox.confirm('确定退出登录吗？', '提示', { type: 'warning' })
    .then(() => { auth.logout(); router.push('/login') })
    .catch(() => {})
}
</script>

<style scoped>
.layout { height: 100vh; }
.el-aside { background: #1a1a2e; }
.logo { color: white; font-size: 16px; font-weight: bold; text-align: center; padding: 20px 0; border-bottom: 1px solid #333; }
.el-header { background: white; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.greeting { font-weight: bold; color: #333; }
.el-main { padding: 20px; }
</style>
