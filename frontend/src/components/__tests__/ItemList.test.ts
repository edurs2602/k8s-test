import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ItemList from '@/components/ItemList.vue'
import type { Item } from '@/types/item'

describe('ItemList', () => {
  const mockItems: Item[] = [
    {
      id: 1,
      title: 'Test Item 1',
      description: 'Description 1',
      is_active: true,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    },
    {
      id: 2,
      title: 'Test Item 2',
      description: 'Description 2',
      is_active: false,
      created_at: '2024-01-02T00:00:00Z',
      updated_at: '2024-01-02T00:00:00Z',
    },
  ]

  it('renders empty state when no items', () => {
    const wrapper = mount(ItemList, {
      props: {
        items: [],
        loading: false,
      },
    })

    expect(wrapper.find('.text-center').exists()).toBe(true)
    expect(wrapper.text()).toContain('Nenhum item encontrado')
  })

  it('renders loading state', () => {
    const wrapper = mount(ItemList, {
      props: {
        items: [],
        loading: true,
      },
    })

    expect(wrapper.find('.animate-spin').exists()).toBe(true)
  })

  it('renders items correctly', () => {
    const wrapper = mount(ItemList, {
      props: {
        items: mockItems,
        loading: false,
      },
    })

    const cards = wrapper.findAll('.bg-white.rounded-xl')
    expect(cards.length).toBe(2)
  })

  it('displays active status correctly', () => {
    const wrapper = mount(ItemList, {
      props: {
        items: mockItems,
        loading: false,
      },
    })

    const badges = wrapper.findAll('span.rounded-full')
    expect(badges[0].text()).toBe('Ativo')
    expect(badges[1].text()).toBe('Inativo')
  })

  it('emits edit event when edit button clicked', async () => {
    const wrapper = mount(ItemList, {
      props: {
        items: mockItems,
        loading: false,
      },
    })

    const editButtons = wrapper.findAll('button')
    const editButton = editButtons.find((btn) => btn.text() === 'Editar')

    await editButton?.trigger('click')

    expect(wrapper.emitted('edit')).toBeTruthy()
    expect(wrapper.emitted('edit')![0]).toEqual([mockItems[0]])
  })

  it('emits delete event when delete button clicked', async () => {
    const wrapper = mount(ItemList, {
      props: {
        items: mockItems,
        loading: false,
      },
    })

    const deleteButtons = wrapper.findAll('button')
    const deleteButton = deleteButtons.find((btn) => btn.text() === 'Excluir')

    await deleteButton?.trigger('click')

    expect(wrapper.emitted('delete')).toBeTruthy()
    expect(wrapper.emitted('delete')![0]).toEqual([1])
  })

  it('filters items by search query', async () => {
    const wrapper = mount(ItemList, {
      props: {
        items: mockItems,
        loading: false,
      },
    })

    const searchInput = wrapper.find('input[type="text"]')
    await searchInput.setValue('Test Item 1')

    const cards = wrapper.findAll('.bg-white.rounded-xl')
    expect(cards.length).toBe(1)
  })
})