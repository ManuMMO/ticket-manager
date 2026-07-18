<script setup lang="ts">
import TicketFilters from '~/components/TicketFilters.vue'
import TicketList from '~/components/TicketList.vue'
import TicketForm from '~/components/TicketForm.vue'
import { useTickets } from '~/composables/useTickets'
import type { TicketStatus, TicketPriority } from '~/types/Ticket'

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

const handleFilters = (newStatus: TicketStatus | null, newPriority: TicketPriority | null) => {
  status.value = newStatus
  priority.value = newPriority
  refresh()
}

const handleRefresh = () => refresh()
</script>

<template>
  <main class="page">
    <header class="header">
      <h1>Gestor de incidencias</h1>
      <button type="button" @click="handleRefresh">Refrescar</button>
    </header>

    <TicketFilters
      :status="status"
      :priority="priority"
      @changeFilters="handleFilters"
    />

    <TicketList
      :tickets="data ?? null"
      :pending="pending"
      :error="error"
      @updateStatus="updateStatus"
    />

    <TicketForm
      @createTicket="createTicket"
    />
  </main>
</template>

<style scoped>
.page {
  max-width: 900px;
  margin: 0 auto;
  padding: 1.5rem;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

button {
  padding: 0.6rem;
  border: none;
  border-radius: 4px;
  background: #eee;
  cursor: pointer;
}
</style>
