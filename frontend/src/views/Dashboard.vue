<template>
  <div class="dashboard">
    <h2 class="page-title">{{ auth.isAdmin ? '首页概览' : '我的借阅' }}</h2>

    <el-row :gutter="20" v-if="auth.isAdmin">
      <el-col :span="6" v-for="(card, i) in cards" :key="i">
        <div class="stat-card" :style="{ background: card.color }">
          <el-icon class="stat-icon"><component :is="card.icon" /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ card.value }}</div>
            <div class="stat-label">{{ card.label }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" v-else>
      <el-col :span="6" v-for="(card, i) in myCards" :key="i">
        <div class="stat-card" :style="{ background: card.color }">
          <el-icon class="stat-icon"><component :is="card.icon" /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ card.value }}</div>
            <div class="stat-label">{{ card.label }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12" v-if="auth.isAdmin">
        <el-card>
          <template #header><span>借阅排行榜 Top 10</span></template>
          <el-table :data="topBooks" stripe>
            <el-table-column prop="title" label="书名" />
            <el-table-column prop="author" label="作者" width="120" />
            <el-table-column prop="borrow_count" label="借阅次数" width="100" align="center" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header><span>快捷操作</span></template>
          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/books')">查看图书</el-button>
            <el-button v-if="auth.isAdmin" type="success" @click="$router.push('/borrow')">借阅管理</el-button>
            <el-button type="warning" @click="$router.push('/my-borrow')">我的借阅</el-button>
            <el-button v-if="auth.isAdmin" type="danger" @click="$router.push('/users')">用户管理</el-button>
          </div>
          <el-divider />
          <p style="color:#666; font-size:14px;">{{ auth.isAdmin ? '系统公告：图书超期将自动标记为逾期，请及时归还。' : '温馨提醒：请按时归还图书，逾期将影响您的借阅权限。' }}</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { statsAPI } from '@/api'
import { Reading, UserFilled, Collection, WarningFilled } from '@element-plus/icons-vue'

const auth = useAuthStore()
const cards = ref([])
const topBooks = ref([])
const myCards = ref([])

onMounted(async () => {
  if (auth.isAdmin) {
    try {
      const res = await statsAPI.overview()
      cards.value = [
        { label: '图书总数', value: res.data.total_copies, icon: Reading, color: 'linear-gradient(135deg, #667eea, #764ba2)' },
        { label: '在架数量', value: res.data.in_stock, icon: Collection, color: 'linear-gradient(135deg, #11998e, #38ef7d)' },
        { label: '已借出', value: res.data.borrowed, icon: UserFilled, color: 'linear-gradient(135deg, #fc4a1a, #f7b733)' },
        { label: '逾期未还', value: res.data.overdue_count, icon: WarningFilled, color: 'linear-gradient(135deg, #eb3349, #f45c43)' },
      ]
    } catch (e) { console.error(e) }

    try {
      const res = await statsAPI.topBooks()
      topBooks.value = res.data
    } catch (e) { console.error(e) }
  } else {
    try {
      const res = await statsAPI.my()
      myCards.value = [
        { label: '累计借阅', value: res.data.total, icon: Reading, color: 'linear-gradient(135deg, #667eea, #764ba2)' },
        { label: '当前借出', value: res.data.borrowed, icon: Collection, color: 'linear-gradient(135deg, #11998e, #38ef7d)' },
        { label: '已逾期', value: res.data.overdue, icon: WarningFilled, color: 'linear-gradient(135deg, #eb3349, #f45c43)' },
        { label: '已归还', value: res.data.returned, icon: UserFilled, color: 'linear-gradient(135deg, #fc4a1a, #f7b733)' },
      ]
    } catch (e) { console.error(e) }
  }
})
</script>

<style scoped>
.page-title { margin-bottom: 20px; font-size: 20px; color: #333; }
.stat-card { border-radius: 12px; padding: 24px; color: white; display: flex; align-items: center; gap: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.stat-icon { font-size: 40px; opacity: 0.9; }
.stat-value { font-size: 32px; font-weight: bold; }
.stat-label { font-size: 14px; opacity: 0.85; }
.quick-actions { display: flex; gap: 10px; flex-wrap: wrap; }
</style>
