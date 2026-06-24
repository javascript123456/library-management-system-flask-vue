<template>
  <div>
    <h2 class="page-title">借阅管理</h2>
    <el-card>
      <div class="toolbar">
        <el-select v-model="statusFilter" placeholder="状态筛选" clearable style="width:140px;" @change="loadRecords">
          <el-option label="借出中" value="borrowed" />
          <el-option label="已归还" value="returned" />
          <el-option label="已逾期" value="overdue" />
        </el-select>
        <el-button type="primary" @click="dialogBorrow = true">办理借书</el-button>
      </div>

      <el-table :data="records" stripe style="margin-top:16px;" v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="book_title" label="书名" min-width="160" />
        <el-table-column prop="username" label="借阅人" width="100" />
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
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button v-if="row.status !== 'returned'" type="success" size="small" @click="handleReturn(row)">归还</el-button>
            <span v-else style="color:#999;">-</span>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination style="margin-top:16px;" v-model:current-page="page" v-model:page-size="perPage"
        :total="total" layout="total,prev,pager,next"
        @current-change="loadRecords" @size-change="loadRecords" />
    </el-card>

    <el-dialog v-model="dialogBorrow" title="办理借书" width="480px">
      <el-form :model="borrowForm" ref="borrowRef" label-width="80px">
        <el-form-item label="用户" prop="user_id">
          <el-select v-model="borrowForm.user_id" placeholder="请选择用户" filterable style="width:100%;">
            <el-option v-for="u in users" :key="u.id" :label="u.username + ' (' + u.role + ')'" :value="u.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="图书" prop="book_id">
          <el-select v-model="borrowForm.book_id" placeholder="请选择图书" filterable style="width:100%;">
            <el-option v-for="b in availableBooks" :key="b.id" :label="b.title + ' - ' + b.author + ' (库存:' + b.stock + ')'" :value="b.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogBorrow=false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleBorrow">确认借书</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { borrowAPI, booksAPI, statsAPI } from '@/api'
import { ElMessage } from 'element-plus'

const records = ref([])
const users = ref([])
const availableBooks = ref([])
const loading = ref(false)
const dialogBorrow = ref(false)
const saving = ref(false)
const page = ref(1)
const perPage = ref(10)
const total = ref(0)
const statusFilter = ref('')
const borrowRef = ref()
const borrowForm = reactive({ user_id: null, book_id: null })

const loadRecords = async () => {
  loading.value = true
  try {
    const res = await borrowAPI.records({ page: page.value, per_page: perPage.value, status: statusFilter.value })
    records.value = res.data.items
    total.value = res.data.total
  } catch (e) { ElMessage.error('加载失败') }
  finally { loading.value = false }
}

const loadUsers = async () => {
  try { const res = await statsAPI.users(); users.value = res.data } catch(e) {}
}

const loadAvailableBooks = async () => {
  try {
    const res = await booksAPI.list({ per_page: 1000 })
    availableBooks.value = res.data.items.filter(b => b.stock > 0)
  } catch(e) {}
}

const handleBorrow = async () => {
  await borrowRef.value.validate()
  saving.value = true
  try {
    await borrowAPI.borrow(borrowForm)
    ElMessage.success('借书成功')
    dialogBorrow.value = false
    loadRecords()
    loadAvailableBooks()
  } catch (e) { ElMessage.error(e.response?.data?.error || '借书失败') }
  finally { saving.value = false }
}

const handleReturn = async (row) => {
  try {
    await borrowAPI.return(row.id)
    ElMessage.success('归还成功')
    loadRecords()
    loadAvailableBooks()
  } catch (e) { ElMessage.error(e.response?.data?.error || '归还失败') }
}

onMounted(() => { loadRecords(); loadUsers(); loadAvailableBooks() })
</script>

<style scoped>
.page-title { margin-bottom: 16px; font-size: 20px; color: #333; }
.toolbar { display: flex; gap: 12px; align-items: center; }
</style>
