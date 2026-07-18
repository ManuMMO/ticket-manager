<script setup lang="ts">
import type { Ticket, TicketStatus } from '~/types/Ticket'

const props = defineProps<{
  tickets: Ticket[] | null
  pending: boolean
  error: unknown
}>()

const emit = defineEmits<{
  (e: 'updateStatus', id: number, newStatus: TicketStatus): void
}>()

const isEmpty = computed(
  () => !props.pending && !props.error && (!props.tickets || props.tickets.length === 0)
)

const getErrorMessage = (error: unknown) => {
  if (!error) return null
  if (typeof error === 'string') return error
  if (error instanceof Error) return error.message
  return JSON.stringify(error)
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
          <span>Prioridad: {{ t.priority }}</span>
          <span>Status: {{ t.status }}</span>
          <span>Creado: {{ new Date(t.created_at).toLocaleString() }}</span>
        </div>

        <div class="ticket-actions">
          <button
            type="button"
            @click="emit('updateStatus', t.id, 'in_progress')"
            :disabled="t.status === 'closed'"
          >
            Marcar como in_progress
          </button>

          <button
            type="button"
            @click="emit('updateStatus', t.id, 'closed')"
            :disabled="t.status === 'closed'"
          >
            Cerrar
          </button>
        </div>
      </li>
    </ul>
  </section>
</template>
