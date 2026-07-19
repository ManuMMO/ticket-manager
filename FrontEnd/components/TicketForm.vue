<script setup lang="ts">
import { ref } from "vue";
import type { Ticket, TicketStatus, TicketPriority, CreateTicketPayload } from "~/types/Ticket";
import { statusLabels, priorityLabels } from "~/utils/ticketLabels";

// Props para recibir la función de creación de ticket desde el padre
const props = defineProps<{
  createTicket: (payload: CreateTicketPayload) => Promise<Ticket>;
}>();

// Ref para los campos del formulario y el error de negocio
const formTitle = ref("");
const formDescription = ref("");
const formPriority = ref<TicketPriority>("low");
const formStatus = ref<TicketStatus>("open");
const businessError = ref<string | null>(null);

const statusOptions: TicketStatus[] = ["open", "in_progress", "closed"];
const priorityOptions: TicketPriority[] = ["low", "medium", "high"];

// Maneja la creación del ticket y captura errores de negocio
const handleCreate = async () => {
  // Reinicia el error de negocio antes de intentar crear el ticket
  businessError.value = null;

  // Construye el payload para la creación del ticket
  const payload: CreateTicketPayload = {
    title: formTitle.value,
    description: formDescription.value || undefined,
    priority: formPriority.value,
    status: formStatus.value
  };

  try {

    // Llama a la función de creación de ticket proporcionada por el padre
    await props.createTicket(payload);

    // Si la creación es exitosa, reinicia los campos del formulario
    formTitle.value = "";
    formDescription.value = "";
    formPriority.value = "low";
    formStatus.value = "open";
  } catch (err: unknown) {

    // Si ocurre un error, captura el mensaje de error de negocio
    businessError.value =
      typeof err === "string"
        ? err
        : "Error al crear el ticket";
  }
};
</script>

<template>
  <section class="form">
    <h2>Crear nuevo ticket</h2>

    <p v-if="businessError" class="error">{{ businessError }}</p>

    <form @submit.prevent="handleCreate">
      <div>
        <label>Título</label>
        <input v-model="formTitle" required maxlength="120" />
      </div>

      <div>
        <label>Descripción</label>
        <textarea v-model="formDescription" />
      </div>

      <div>
        <label>Prioridad</label>
        <select v-model="formPriority">
          <option v-for="p in priorityOptions" :key="p" :value="p">
            {{ priorityLabels[p] }}
          </option>
        </select>
      </div>

      <div>
        <label>Estado</label>
        <select v-model="formStatus">
          <option v-for="s in statusOptions" :key="s" :value="s">
            {{ statusLabels[s] }}
          </option>
        </select>
      </div>

      <button type="submit">Crear ticket</button>
    </form>
  </section>
</template>

<style scoped>
.form {
  max-width: 480px;
  margin: 2rem auto;
  padding: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.form h2 {
  margin-bottom: 1rem;
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

form div {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

label {
  font-size: 0.9rem;
  font-weight: 600;
}

input,
textarea,
select {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

textarea {
  min-height: 80px;
  resize: vertical;
}

button {
  padding: 0.6rem;
  border: none;
  border-radius: 4px;
  background: #eee;
  cursor: pointer;
}

button:hover {
  background: #ddd;
}

.error {
  margin-bottom: 1rem;
  padding: 0.6rem;
  border: 1px solid #d00;
  border-radius: 4px;
}
</style>