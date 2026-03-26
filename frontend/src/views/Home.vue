<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useItemStore } from '@/stores/items'
import ItemList from '@/components/ItemList.vue'
import ItemModal from '@/components/ItemModal.vue'
import DeleteModal from '@/components/DeleteModal.vue'
import type { Item, ItemCreate, ItemUpdate } from '@/types/item'

const itemStore = useItemStore()

const showModal = ref(false)
const showDeleteModal = ref(false)
const editingItem = ref<Item | null>(null)
const deletingItemId = ref<number | null>(null)

const deletingItemName = ref('')

onMounted(() => {
  itemStore.fetchItems()
})

const handleCreateNew = () => {
  editingItem.value = null
  showModal.value = true
}

const handleEdit = (item: Item) => {
  editingItem.value = item
  showModal.value = true
}

const handleSave = async (data: ItemCreate | ItemUpdate) => {
  try {
    if (editingItem.value) {
      await itemStore.updateItem(editingItem.value.id, data as ItemUpdate)
    } else {
      await itemStore.createItem(data as ItemCreate)
    }
    showModal.value = false
    editingItem.value = null
  } catch (error) {
    console.error('Error saving item:', error)
  }
}

const handleDelete = (id: number) => {
  const item = itemStore.items.find(i => i.id === id)
  if (item) {
    deletingItemId.value = id
    deletingItemName.value = item.title
    showDeleteModal.value = true
  }
}

const confirmDelete = async () => {
  if (deletingItemId.value) {
    try {
      await itemStore.deleteItem(deletingItemId.value)
      showDeleteModal.value = false
      deletingItemId.value = null
      deletingItemName.value = ''
    } catch (error) {
      console.error('Error deleting item:', error)
    }
  }
}

const closeModals = () => {
  showModal.value = false
  editingItem.value = null
  showDeleteModal.value = false
  deletingItemId.value = null
  deletingItemName.value = ''
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-extrabold text-gray-900 sm:text-5xl">
          <span class="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
            Gerenciador de Itens
          </span>
        </h1>
        <p class="mt-3 text-lg text-gray-600">
          Organize e gerencie seus itens de forma simples e eficiente
        </p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
          <div class="flex items-center">
            <div class="p-3 rounded-lg bg-blue-100">
              <svg class="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Total</p>
              <p class="text-2xl font-bold text-gray-900">{{ itemStore.total }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
          <div class="flex items-center">
            <div class="p-3 rounded-lg bg-green-100">
              <svg class="w-6 h-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Ativos</p>
              <p class="text-2xl font-bold text-gray-900">
                {{ itemStore.items.filter(i => i.is_active).length }}
              </p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
          <div class="flex items-center">
            <div class="p-3 rounded-lg bg-red-100">
              <svg class="w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Inativos</p>
              <p class="text-2xl font-bold text-gray-900">
                {{ itemStore.items.filter(i => !i.is_active).length }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Add Button -->
      <div class="flex justify-end mb-6">
        <button
          @click="handleCreateNew"
          class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
        >
          <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Novo Item
        </button>
      </div>

      <!-- Error Message -->
      <div v-if="itemStore.error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-sm text-red-600">{{ itemStore.error }}</p>
      </div>

      <!-- Item List -->
      <ItemList
        :items="itemStore.items"
        :loading="itemStore.loading"
        @edit="handleEdit"
        @delete="handleDelete"
      />

      <!-- Item Modal -->
      <ItemModal
        :show="showModal"
        :item="editingItem"
        @close="closeModals"
        @save="handleSave"
      />

      <!-- Delete Modal -->
      <DeleteModal
        :show="showDeleteModal"
        :item-name="deletingItemName"
        @close="closeModals"
        @confirm="confirmDelete"
      />
    </div>
  </div>
</template>