import type { Ticket, CreateTicketPayload, TicketStatus , TicketPriority } from "~/types/Ticket";
import type { BackendError } from "~/types/BackendError";

// Tipa el error para que no devuelva any
export function extractErrorMessage(err: unknown): string {
  if (typeof err === "object" && err !== null) {
    const e = err as { data?: BackendError }

    const status = e.data?.status

    if (Array.isArray(status) && status.length > 0) {
      return status[0]!
    }
  }

  return "Error desconocido"
}

export const useTickets = () => {
  // obtener la configuración de runtime para acceder a la URL base de la API
  const config = useRuntimeConfig();

  const status = ref<TicketStatus | null>(null);
  const priority = ref<TicketPriority | null>(null);

  const { data, pending, error, refresh } = useFetch<Ticket[]>(() => {
    const base = `${config.public.apiBaseUrl}/api/tickets/`;
    const params = new URLSearchParams();

    if (status.value) params.append("status", status.value);
    if (priority.value) params.append("priority", priority.value);

    return params.toString() ? `${base}?${params.toString()}` : base;
  });

  const createTicket = async (
    payload: CreateTicketPayload,
  ): Promise<Ticket> => {
    try {
      const res = await $fetch<Ticket>(
        `${config.public.apiBaseUrl}/api/tickets/`,
        {
          method: "POST",
          body: payload,
        },
      );
      await refresh();
      return res;
    } catch (err: unknown) {
      throw extractErrorMessage(err);
    }
  };

  const updateStatus = async (
    id: number,
    newStatus: TicketStatus,
  ): Promise<Ticket> => {
    try {
      const res = await $fetch<Ticket>(
        `${config.public.apiBaseUrl}/api/tickets/${id}/`,
        {
          method: "PATCH",
          body: { status: newStatus },
        },
      );
      await refresh();
      return res;
    } catch (err: unknown) {
      throw extractErrorMessage(err);
    }
  };

  return {
    status,
    priority,
    data,
    pending,
    error,
    refresh,
    createTicket,
    updateStatus,
  };
};
