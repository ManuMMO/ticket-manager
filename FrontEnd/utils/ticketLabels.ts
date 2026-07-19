import type { TicketStatus, TicketPriority } from '~/types/Ticket'

// Traducciones de los estados y prioridades de los tickets
export const statusLabels: Record<TicketStatus, string> = {
  open: 'Abierto',
  in_progress: 'En progreso',
  closed: 'Cerrado'
}

export const priorityLabels: Record<TicketPriority, string> = {
  low: 'Baja',
  medium: 'Media',
  high: 'Alta'
}
