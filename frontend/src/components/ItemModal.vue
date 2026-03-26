<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import type { Item, ItemCreate, ItemUpdate } from '@/types/item'

const props = defineProps<{
  show: boolean
  item?: Item | null
}>()

const emit = defineEmits<{
  close: []
  save: [data: ItemCreate | ItemUpdate]
}>()

const title = ref('')
const description = ref('')
const isActive = ref(true)

const isEditing = computed(() => !!props.item)
const modalTitle = computed(() => isEditing.value ? 'Editar Item' : 'Novo Item')

watch(() => props.item, (newItem) => {
  if (newItem) {
    title.value = newItem.title
    description.value = newItem.description || ''
    isActive.value = newItem.is_active
  } else {
    title.value = ''
    description.value = ''
    isActive.value = true
  }
}, { immediate: true })

const handleSubmit = () => {
  const data: ItemCreate | ItemUpdate = isEditing.value
    ? {
        title: title.value,
        description: description.value || null,
        is_active: isActive.value
      }
    : {
        title: title.value,
        description: description.value || undefined,
        is_active: isActive.value
      }
  
  emit('save', data)
}

const handleClose = () => {
  emit('close')
}
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity" @click="handleClose"></div>
          
          <div class="relative bg-white rounded-2xl shadow-xl max-w-md w-full p-6 transform transition-all">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-2xl font-bold text-gray-900">{{ modalTitle }}</h2>
              <button
                @click="handleClose"
                class="text-gray-400 hover:text-gray-600 transition"
              >
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <form @submit.prevent="handleSubmit" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Título <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="title"
                  type="text"
                  required
                  placeholder="Digite o título"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Descrição
                </label>
                <textarea
                  v-model="description"
                  rows="3"
                  placeholder="Digite a descrição (opcional)"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition resize-none"
                ></textarea>
              </div>

              <div class="flex items-center">
                <input
                  v-model="isActive"
                  type="checkbox"
                  id="isActive"
                  class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <label for="isActive" class="ml-2 text-sm text-gray-700">
                  Item ativo
                </label>
              </div>

              <div class="flex gap-3 pt-4">
                <button
                  type="button"
                  @click="handleClose"
                  class="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition font-medium"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
                >
                  {{ isEditing ? 'Salvar' : 'Criar' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>