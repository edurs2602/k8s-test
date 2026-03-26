<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Item } from '@/types/item'

const props = defineProps<{
  items: Item[]
  loading: boolean
}>()

const emit = defineEmits<{
  edit: [item: Item]
  delete: [id: number]
}>()

const searchQuery = ref('')
const filterActive = ref<boolean | null>(null)

const filteredItems = computed(() => {
  let result = props.items
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(item => 
      item.title.toLowerCase().includes(query) ||
      item.description?.toLowerCase().includes(query)
    )
  }
  
  if (filterActive.value !== null) {
    result = result.filter(item => item.is_active === filterActive.value)
  }
  
  return result
})

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<template>
  <div class="item-list">
    <div class="mb-6 flex flex-col sm:flex-row gap-4">
      <div class="flex-1">
        <label class="block text-sm font-medium text-gray-700 mb-1">Buscar</label>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar itens..."
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
        />
      </div>
      
      <div class="sm:w-48">
        <label class="block text-sm font-medium text-gray-700 mb-1">Filtrar</label>
        <select
          v-model="filterActive"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
        >
          <option :value="null">Todos</option>
          <option :value="true">Ativos</option>
          <option :value="false">Inativos</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <div v-else-if="filteredItems.length === 0" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">Nenhum item encontrado</h3>
      <p class="mt-1 text-sm text-gray-500">Tente ajustar seus filtros de busca.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="item in filteredItems"
        :key="item.id"
        class="bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-200 border border-gray-200 overflow-hidden"
      >
        <div class="p-6">
          <div class="flex items-start justify-between mb-3">
            <h3 class="text-lg font-semibold text-gray-900 line-clamp-1">
              {{ item.title }}
            </h3>
            <span
              :class="[
                'px-2.5 py-0.5 rounded-full text-xs font-medium',
                item.is_active 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              ]"
            >
              {{ item.is_active ? 'Ativo' : 'Inativo' }}
            </span>
          </div>
          
          <p v-if="item.description" class="text-gray-600 text-sm mb-4 line-clamp-2">
            {{ item.description }}
          </p>
          <p v-else class="text-gray-400 text-sm mb-4 italic">
            Sem descrição
          </p>
          
          <div class="flex items-center text-xs text-gray-500 mb-4">
            <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ formatDate(item.created_at) }}
          </div>
          
          <div class="flex gap-2">
            <button
              @click="emit('edit', item)"
              class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium text-sm"
            >
              Editar
            </button>
            <button
              @click="emit('delete', item.id)"
              class="px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition font-medium text-sm border border-red-200"
            >
              Excluir
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>