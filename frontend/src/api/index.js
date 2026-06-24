import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const booksAPI = {
  list: (params) => api.get('/books', { params }),
  get: (id) => api.get(`/books/${id}`),
  create: (data) => api.post('/books', data),
  update: (id, data) => api.put(`/books/${id}`, data),
  delete: (id) => api.delete(`/books/${id}`),
  categories: () => api.get('/books/categories'),
}

export const borrowAPI = {
  borrow: (data) => api.post('/borrow', data),
  return: (id) => api.put(`/borrow/${id}/return`),
  records: (params) => api.get('/borrow/records', { params }),
  my: (params) => api.get('/borrow/my', { params }),
}

export const statsAPI = {
  overview: () => api.get('/stats/overview'),
  topBooks: () => api.get('/stats/top-books'),
  users: () => api.get('/stats/users'),
  my: () => api.get('/stats/my'),
}
