<template>
  <div>
    <h2 class="page-title">图书管理</h2>
    <el-card>
      <div class="toolbar">
        <el-input v-model="keyword" placeholder="搜索书名/作者/ISBN" style="width:260px;" clearable @clear="loadBooks" @keyup.enter="loadBooks">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-select v-model="categoryFilter" placeholder="分类筛选" clearable style="width:160px;" @change="loadBooks">
          <el-option v-for="c in categories" :key="c" :label="c" :value="c" />
        </el-select>
        <el-button type="primary" @click="openAdd">新增图书</el-button>
      </div>

      <el-table :data="books" stripe style="margin-top:16px;" v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="title" label="书名" min-width="160" />
        <el-table-column prop="author" label="作者" width="120" />
        <el-table-column prop="isbn" label="ISBN" width="140" />
        <el-table-column prop="category" label="分类" width="100" />
        <el-table-column prop="stock" label="库存/总册" width="110" align="center">
          <template #default="{ row }">
            <el-tag :type="row.stock > 0 ? 'success' : 'danger'" size="small">{{ row.stock }}/{{ row.total_copies }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publisher" label="出版社" width="130" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="auth.isAdmin" type="primary" size="small" @click="openEdit(row)">编辑</el-button>
            <el-button v-if="auth.isAdmin" type="danger" size="small" @click="handleDelete(row)">删除</el-button>
            <el-button v-if="!auth.isAdmin && row.stock > 0" type="success" size="small" @click="handleBorrow(row)">借书</el-button>
            <span v-if="!auth.isAdmin && row.stock === 0" style="color:#999; font-size:12px;">暂无库存</span>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination style="margin-top:16px;" v-model:current-page="page" v-model:page-size="perPage"
        :total="total" :page-sizes="[10,20,50]" layout="total,sizes,prev,pager,next"
        @current-change="loadBooks" @size-change="loadBooks" />
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑图书' : '新增图书'" width="600px">
      <el-form :model="form" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="ISBN" prop="isbn">
          <el-input v-model="form.isbn" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="书名" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="form.author" />
        </el-form-item>
        <el-form-item label="出版社">
          <el-input v-model="form.publisher" />
        </el-form-item>
        <el-form-item label="分类">
          <el-input v-model="form.category" placeholder="如: 计算机, 文学, 历史" />
        </el-form-item>
        <el-form-item label="总册数" prop="total_copies">
          <el-input-number v-model="form.total_copies" :min="1" />
        </el-form-item>
        <el-form-item label="当前库存" prop="stock">
          <el-input-number v-model="form.stock" :min="0" :max="form.total_copies" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { booksAPI, borrowAPI } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

const auth = useAuthStore()

const books = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const saving = ref(false)
const categories = ref([])
const formRef = ref()
const page = ref(1)
const perPage = ref(10)
const total = ref(0)
const keyword = ref('')
const categoryFilter = ref('')

const form = reactive({ isbn:'', title:'', author:'', publisher:'', category:'', stock:1, total_copies:1, description:'' })
const formRules = {
  isbn: [{ required: true, message: '请输入ISBN', trigger: 'blur' }],
  title: [{ required: true, message: '请输入书名', trigger: 'blur' }],
  author: [{ required: true, message: '请输入作者', trigger: 'blur' }],
}

const loadBooks = async () => {
  loading.value = true
  try {
    const res = await booksAPI.list({ page: page.value, per_page: perPage.value, keyword: keyword.value, category: categoryFilter.value })
    books.value = res.data.items
    total.value = res.data.total
  } catch (e) { ElMessage.error('加载失败') }
  finally { loading.value = false }
}

const loadCategories = async () => {
  try { const res = await booksAPI.categories(); categories.value = res.data } catch(e) {}
}

const openAdd = () => { isEdit.value = false; Object.assign(form, { isbn:'', title:'', author:'', publisher:'', category:'', stock:1, total_copies:1, description:'' }); dialogVisible.value = true }
const openEdit = (row) => { isEdit.value = true; Object.assign(form, { ...row, stock: row.stock, total_copies: row.total_copies }); dialogVisible.value = true }

const handleSave = async () => {
  await formRef.value.validate()
  saving.value = true
  try {
    if (isEdit.value) {
      await booksAPI.update(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await booksAPI.create(form)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    loadBooks()
  } catch (e) { ElMessage.error(e.response?.data?.error || '保存失败') }
  finally { saving.value = false }
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定删除《${row.title}》吗？`, '提示', { type: 'warning' })
    .then(async () => { await booksAPI.delete(row.id); ElMessage.success('删除成功'); loadBooks() })
    .catch(() => {})
}

const handleBorrow = async (row) => {
  try {
    await borrowAPI.borrow({ book_id: row.id })
    ElMessage.success(`《${row.title}》借书成功！`)
    loadBooks()
  } catch (e) {
    ElMessage.error(e.response?.data?.error || '借书失败')
  }
}

onMounted(() => { loadBooks(); loadCategories() })
</script>

<style scoped>
.page-title { margin-bottom: 16px; font-size: 20px; color: #333; }
.toolbar { display: flex; gap: 12px; align-items: center; }
</style>
