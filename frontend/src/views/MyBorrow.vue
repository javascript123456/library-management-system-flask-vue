<template>
  <div>
    <h2 class="page-title">我的借阅</h2>
    <el-card>
      <el-table :data="records" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="book_title" label="书名" min-width="160" />
        <el-table-column prop="borrow_date" label="借书日期" width="110" />
        <el-table-column prop="due_date" label="应还日期" width="110" />
        <el-table-column prop="return_date" label="实际归还" width="110" />
        <el-table-column label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 'returned' ? 'success' : row.status === 'overdue' ? 'danger' : 'warning'" size="small">
              {{ row.status === 'borrowed' ? '借出中' : row.status === 'overdue' ? '已逾期' : '已归还' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination style="margin-top:16px;" v-model:current-page="page" v-model:page-size="perPage"
        :total="total" layout="total,prev,pager,next"
        @current-change="loadRecords" @size-change="loadRecords" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { borrowAPI } from '@/api'
import { ElMessage } from 'element-plus'

const records = ref([])
const loading = ref(false)
const page = ref(1)
const perPage = ref(10)
const total = ref(0)

const loadRecords = async () => {
  loading.value = true
  try {
    const res = await borrowAPI.my({ page: page.value, per_page: perPage.value })
    records.value = res.data.items
    total.value = res.data.total
  } catch (e) { ElMessage.error('加载失败') }
  finally { loading.value = false }
}

onMounted(() => loadRecords())
</script>

<style scoped>
.page-title { margin-bottom: 16px; font-size: 20px; color: #333; }
</style>
