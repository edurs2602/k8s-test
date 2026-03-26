import axios from 'axios'
import type { Item, ItemCreate, ItemUpdate, ItemList } from '@/types/item'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

export const itemApi = {
  async getAll(page = 1, pageSize = 10, activeOnly = false): Promise<ItemList> {
    const response = await api.get<ItemList>('/items/', {
      params: { page, page_size: pageSize, active_only: activeOnly }
    })
    return response.data
  },

  async getById(id: number): Promise<Item> {
    const response = await api.get<Item>(`/items/${id}`)
    return response.data
  },

  async create(data: ItemCreate): Promise<Item> {
    const response = await api.post<Item>('/items/', data)
    return response.data
  },

  async update(id: number, data: ItemUpdate): Promise<Item> {
    const response = await api.patch<Item>(`/items/${id}`, data)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/items/${id}`)
  }
}

export default api