<script setup lang="ts">
import type { TicketStatus, TicketPriority } from '~/types/Ticket'

const props = defineProps<{
  status: TicketStatus | null
  priority: TicketPriority | null
}>()

const emit = defineEmits<{
  (e: 'changeFilters', status: TicketStatus | null, priority: TicketPriority | null): void
}>()

const statusOptions: TicketStatus[] = ['open', 'in_progress', 'closed']
const priorityOptions: TicketPriority[] = ['low', 'medium', 'high']

const handleStatusChange = (event: Event) => {
  const value = (event.target as HTMLSelectElement).value || null
  emit('changeFilters', value as TicketStatus | null, props.priority)
}

const handlePriorityChange = (event: Event) => {
  const value = (event.target as HTMLSelectElement).value || null
  emit('changeFilters', props.status, value as TicketPriority | null)
}
</script>

<template>
  <section class="filters">
    <div>
      <label>Status</label>
      <select :value="status ?? ''" @change="handleStatusChange">
        <option :value="''">Todos</option>
        <option v-for="s in statusOptions" :key="s" :value="s">
          {{ s }}
        </option>
      </select>
    </div>

    <div>
      <label>Priority</label>
      <select :value="priority ?? ''" @change="handlePriorityChange">
        <option :value="''">Todas</option>
        <option v-for="p in priorityOptions" :key="p" :value="p">
          {{ p }}
        </option>
      </select>
    </div>
  </section>
</template>

<style scoped>
.filters {
  display: flex;
  gap: 1.5rem;
  align-items: flex-end;
  margin-bottom: 1.5rem;
}

.filters > div {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

label {
  font-size: 0.9rem;
  font-weight: 600;
}

select {
  padding: 0.4rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
