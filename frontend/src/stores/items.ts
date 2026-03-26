import { defineStore } from 'pinia'
import { ref } from 'vue'
import { itemApi } from '@/api'
import type { Item, ItemCreate, ItemUpdate, ItemList } from '@/types/item'

export const useItemStore = defineStore('items', () => {
  const items = ref<Item[]>([])
  const current_item = ref<Item | null>(null)
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(10)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchItems(p = 1, ps = 10, activeOnly = false) {
    loading.value = true
    error.value = null
    try {
      const data: ItemList = await itemApi.getAll(p, ps, activeOnly)
      items.value = data.items
      total.value = data.total
      page.value = data.page
      pageSize.value = data.page_size
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch items'
    } finally {
      loading.value = false
    }
  }

  async function fetchItem(id: number) {
    loading.value = true
    error.value = null
    try {
      current_item.value = await itemApi.getById(id)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch item'
    } finally {
      loading.value = false
    }
  }

  async function createItem(data: ItemCreate) {
    loading.value = true
    error.value = null
    try {
      const newItem = await itemApi.create(data)
      items.value.push(newItem)
      total.value++
      return newItem
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create item'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateItem(id: number, data: ItemUpdate) {
    loading.value = true
    error.value = null
    try {
      const updatedItem = await itemApi.update(id, data)
      const index = items.value.findIndex((i) => i.id === id)
      if (index !== -1) {
        items.value[index] = updatedItem
      }
      return updatedItem
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to update item'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteItem(id: number) {
    loading.value = true
    error.value = null
    try {
      await itemApi.delete(id)
      items.value = items.value.filter((i) => i.id !== id)
      total.value--
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to delete item'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    current_item,
    total,
    page,
    pageSize,
    loading,
    error,
    fetchItems,
    fetchItem,
    createItem,
    updateItem,
    deleteItem
  }
})