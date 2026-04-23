<!-- src/routes/create/+page.svelte -->
<h2>➕ Crea Nuovo Evento</h2>

<form on:submit|preventDefault={handleSubmit}>
  <label>
    Titolo:
    <input type="text" bind:value={title} placeholder="Es: Riunione di team" />
  </label>

  <label>
    Descrizione:
    <textarea bind:value={description} placeholder="Dettagli opzionali..." rows="3"></textarea>
  </label>

  <h3>Slot Temporali</h3>

  <div class="slot">
    <label>
      Inizio:
      <input type="datetime-local" bind:value={slotStart} />
    </label>
    <label>
      Fine:
      <input type="datetime-local" bind:value={slotEnd} />
    </label>
  </div>

  <button type="submit">Crea Evento</button>
</form>

{#if created}
  <div class="success">
    <p>✅ Evento creato!</p>
    <p>Titolo: <strong>{title}</strong></p>
    <p>Da: {slotStart} — A: {slotEnd}</p>
    <a href="/event/abc123">Vai all'evento →</a>
  </div>
{/if}

<script lang="ts">
  let title = '';
  let description = '';
  let slotStart = '';
  let slotEnd = '';
  let created = false;

  function handleSubmit() {
    if (!title || !slotStart || !slotEnd) {
      alert('Compila almeno titolo, inizio e fine!');
      return;
    }
    // Per ora è solo una demo — non chiama il backend
    created = true;
  }
</script>

<style>
  form {
    max-width: 500px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  label {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    font-weight: bold;
  }

  input, textarea {
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: normal;
  }

  .slot {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 6px;
  }

  button {
    padding: 0.75rem;
    background: #4caf50;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    cursor: pointer;
  }

  button:hover {
    background: #43a047;
  }

  .success {
    margin-top: 1.5rem;
    padding: 1rem;
    background: #e8f5e9;
    border-radius: 8px;
    border: 1px solid #a5d6a7;
  }

  .success a {
    color: #1976d2;
  }
</style>