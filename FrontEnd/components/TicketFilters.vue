<script setup lang="ts">
import type { TicketStatus, TicketPriority } from '~/types/Ticket'
import { statusLabels, priorityLabels } from '~/utils/ticketLabels'

// Props para recibir los filtros de estado y prioridad desde el padre
const props = defineProps<{
  status: TicketStatus | null
  priority: TicketPriority | null
}>()

// Emit para enviar los filtros actualizados al padre
const emit = defineEmits<{
  (e: 'changeFilters', status: TicketStatus | null, priority: TicketPriority | null): void
}>()

// Opciones de estado y prioridad para los selectores
const statusOptions: TicketStatus[] = ['open', 'in_progress', 'closed']
const priorityOptions: TicketPriority[] = ['low', 'medium', 'high']

// Maneja el cambio de estado y emite el evento al padre
const handleStatusChange = (event: Event) => {
  const value = (event.target as HTMLSelectElement).value || null
  emit('changeFilters', value as TicketStatus | null, props.priority)
}

// Maneja el cambio de prioridad y emite el evento al padre
const handlePriorityChange = (event: Event) => {
  const value = (event.target as HTMLSelectElement).value || null
  emit('changeFilters', props.status, value as TicketPriority | null)
}
</script>

<template>
  <section class="filters">
    <div>
      <label>Estado</label>
      <select :value="status ?? ''" @change="handleStatusChange">
        <option :value="''">Todos</option>
        <option v-for="s in statusOptions" :key="s" :value="s">
          {{ statusLabels[s] }}
        </option>
      </select>
    </div>

    <div>
      <label>Prioridad</label>
      <select :value="priority ?? ''" @change="handlePriorityChange">
        <option :value="''">Todas</option>
        <option v-for="p in priorityOptions" :key="p" :value="p">
          {{ priorityLabels[p] }}
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
