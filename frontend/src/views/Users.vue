<template>
  <div>
    <h2 class="page-title">用户管理</h2>
    <el-card>
      <el-table :data="users" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column label="角色" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'" size="small">{{ row.role === 'admin' ? '管理员' : '普通用户' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="phone" label="手机号" width="140" />
        <el-table-column prop="created_at" label="注册时间" width="160" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { statsAPI } from '@/api'
import { ElMessage } from 'element-plus'

const users = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try { const res = await statsAPI.users(); users.value = res.data }
  catch (e) { ElMessage.error('加载失败') }
  finally { loading.value = false }
})
</script>

<style scoped>
.page-title { margin-bottom: 16px; font-size: 20px; color: #333; }
</style>
