// Para controlar el tipado y no sea any
import type { Ticket, CreateTicketPayload, TicketStatus } from '~/types/Ticket'
console.log("Módulo useTickets cargado")

export const useTickets = () => {
  console.log("dentro useTickets:")
  const config = useRuntimeConfig()
  console.log(config.public.apiBaseUrl);
  const status = ref<TicketStatus | null>(null)
  const priority = ref<Ticket['priority'] | null>(null)

  const { data, pending, error, refresh } = useFetch<Ticket[]>(`${config.public.apiBaseUrl}/api/tickets/`, {
    query: { status, priority }
  })

  const createTicket = async (payload: CreateTicketPayload): Promise<Ticket> => {
    try {
      const res = await $fetch<Ticket>(`${config.public.apiBaseUrl}/api/tickets/`, {
        method: 'POST',
        body: payload
      })
      await refresh()
      return res
    } catch (err: any) {
      throw err?.data
    }
  }

  const updateStatus = async (id: number, newStatus: TicketStatus): Promise<Ticket> => {
    try {
      const res = await $fetch<Ticket>(`${config.public.apiBaseUrl}/api/tickets/${id}/`, {
        method: 'PATCH',
        body: { status: newStatus }
      })
      await refresh()
      return res
    } catch (err: any) {
      throw err?.data
    }
  }

  return {
    status,
    priority,
    data,
    pending,
    error,
    refresh,
    createTicket,
    updateStatus
  }
}
