export interface Ticket {
  id: number
  title: string
  description?: string
  priority: 'low' | 'medium' | 'high'
  status: 'open' | 'in_progress' | 'closed'
  created_at: string
  updated_at: string
}

export interface CreateTicketPayload {
  title: string
  description?: string
  priority: TicketPriority
  status: TicketStatus
}

export type TicketStatus = Ticket['status']
export type TicketPriority = Ticket['priority']
