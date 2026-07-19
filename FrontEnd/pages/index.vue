<script setup lang="ts">
import TicketFilters from '~/components/TicketFilters.vue'
import TicketList from '~/components/TicketList.vue'
import TicketForm from '~/components/TicketForm.vue'
import { useTickets } from '~/composables/useTickets'
import type {
  TicketStatus,
  TicketPriority,
  CreateTicketPayload
} from '~/types/Ticket'

// Composable maneja los datos y la lógica de negocio de los tickets
const {
  status,
  priority,
  data,
  pending,
  error,
  refresh,
  createTicket,
  updateStatus
} = useTickets()

// actualiza los filtros y refresca la lista de tickets, en el composable
const handleFilters = (
  newStatus: TicketStatus | null,
  newPriority: TicketPriority | null
) => {
  status.value = newStatus
  priority.value = newPriority
  refresh()
}

// GET - refresco de lista y sus filtros, no reinicia la página, solo pide los datos de nuevo al backend
const handleRefresh = () => refresh()

// POST - crea el ticket, si falla devuelve un error, si no, refresca la lista de tickets
const handleCreateTicket = async (payload: CreateTicketPayload) => {
  return await createTicket(payload)
}

// PATCH - actualiza el estado del ticket, si falla devuelve un error, si no, refresca la lista de tickets
const handleUpdateStatus = async (
  id: number,
  newStatus: TicketStatus
) => {
 await updateStatus(id, newStatus)
}
</script>

<template>
  <main class="page">
    <header class="header">
      <h1>Gestor de incidencias</h1>
      <button type="button" @click="handleRefresh">Refrescar</button>
    </header>

    // Filtros de estado y prioridad, emite evento al padre para actualizar los filtros y refrescar la lista
    <TicketFilters
      :status="status"
      :priority="priority"
      @changeFilters="handleFilters"
    />

    <TicketList
      :tickets="data ?? null"
      :pending="pending"
      :error="error"
      :update-status="handleUpdateStatus"
    />

    <TicketForm
      :create-ticket="handleCreateTicket"
    />
  </main>
</template>

<style scoped>
button {
  padding: .6rem;
  border: none;
  border-radius: 4px;
  background: #eee;
  cursor: pointer;
}
</style>