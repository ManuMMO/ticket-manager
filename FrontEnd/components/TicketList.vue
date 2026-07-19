<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Ticket, TicketStatus } from '~/types/Ticket'
import { statusLabels, priorityLabels } from '~/utils/ticketLabels'

// Props para recibir los tickets, estado de carga, error desde el padre y la función para actualizar el estado del ticket
const props = defineProps<{
  tickets: Ticket[] | null
  pending: boolean
  error: unknown
  updateStatus: (
    id: number,
    status: TicketStatus
  ) => Promise<void>
}>()

// Ref para almacenar los errores de cada ticket al actualizar su estado
const ticketErrors = ref<Record<number, string>>({})

// Computed para determinar si la lista de tickets está vacía
const isEmpty = computed(() =>
  !props.pending &&
  !props.error &&
  (!props.tickets || props.tickets.length === 0)
)

// Función para obtener un mensaje de error legible a partir del error recibido
const getErrorMessage = (error: unknown) => {
  if (!error) return null

  if (typeof error === 'string') return error

  if (error instanceof Error) return error.message

  return JSON.stringify(error)
}

// Maneja el cambio de estado de un ticket y actualiza su estado mediante la función proporcionada por el padre
const handleStatusChange = async (
  id: number,
  event: Event
) => {
  const target = event.target as HTMLSelectElement

  ticketErrors.value[id] = ''

  try {
    await props.updateStatus(
      id,
      target.value as TicketStatus
    )
  } catch (err) {
    ticketErrors.value[id] =
      typeof err === 'string'
        ? err
        : 'Error al actualizar el ticket'
  }
}
</script>

<template>
  <section class="feedback">
    <p v-if="pending">Cargando tickets...</p>

    <p v-if="error">Error al cargar: {{ getErrorMessage(error) }}</p>

    <p v-if="isEmpty">No hay tickets.</p>
  </section>

  <section class="list" v-if="tickets && tickets.length">
    <ul>
      <li v-for="t in tickets" :key="t.id" class="ticket">
        <div class="ticket-main">
          <h2>{{ t.title }}</h2>
          <p v-if="t.description">{{ t.description }}</p>
        </div>

        <div class="ticket-meta">
          <span>Prioridad: {{ priorityLabels[t.priority] }}</span>

          <span>Estado: {{ statusLabels[t.status] }}</span>

          <span>Creado: {{ new Date(t.created_at).toLocaleString() }}</span>
        </div>

        <div class="ticket-actions">
          <label>Cambiar estado:</label>

          <select
            :value="t.status"
            @change="(event) => handleStatusChange(t.id, event)"
          >
            <option value="open">
              Abierto
            </option>

            <option value="in_progress">
              En progreso
            </option>

            <option value="closed">
              Cerrado
            </option>
          </select>

          <p v-if="ticketErrors[t.id]" class="error">
            {{ ticketErrors[t.id] }}
          </p>
        </div>
      </li>
    </ul>
  </section>
</template>

<style scoped>
button,
select {
  padding: .6rem;
  border: none;
  border-radius: 4px;
  background: #eee;
  cursor: pointer;
}

.ticket {
  display: grid;
  grid-template-columns: 2fr 2fr 1fr;
  gap: 1.5rem;
  padding: 1rem 0;
  border-bottom: 1px solid #ddd;
  align-items: start;
}

.ticket-main {
  display: flex;
  flex-direction: column;
  gap: .4rem;
}

.ticket-main h2 {
  margin: 0;
}

.ticket-meta {
  display: flex;
  flex-direction: column;
  gap: .4rem;
}

.ticket-actions {
  display: flex;
  flex-direction: column;
  gap: .6rem;
}

.error {
  color: #b00020;
  font-size: .9rem;
}
</style>