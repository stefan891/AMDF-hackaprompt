<!-- src/routes/event/[id]/+page.svelte -->
<script lang="ts">
  import { page } from '$app/stores';

  // Dati finti per la demo
  const demoSlots = [
    { id: '1', time: 'Lunedì 21 Gen — 09:00-10:00', selected: '' },
    { id: '2', time: 'Martedì 22 Gen — 14:00-15:00', selected: '' },
    { id: '3', time: 'Mercoledì 23 Gen — 11:00-12:00', selected: '' }
  ];

  let slots = demoSlots;
  let submitted = false;

  function setPreference(slotId: string, value: string) {
    slots = slots.map(s =>
      s.id === slotId ? { ...s, selected: value } : s
    );
  }

  function handleSubmit() {
    const unanswered = slots.filter(s => !s.selected);
    if (unanswered.length > 0) {
      alert(`Rispondi a tutti gli slot! (${unanswered.length} mancanti)`);
      return;
    }
    submitted = true;
  }
</script>

<h2>📋 Dettaglio Evento</h2>
<p>ID Evento: <strong>{$page.params.id}</strong></p>

<div class="event-info">
  <h3>Riunione di Team (demo)</h3>
  <p>Scegli le tue preferenze per ogni slot:</p>
</div>

{#if submitted}
  <div class="success">
    <p>✅ Preferenze inviate!</p>
    <ul>
      {#each slots as slot}
        <li>{slot.time}: <strong>{slot.selected}</strong></li>
      {/each}
    </ul>
    <a href="/overview/{$page.params.id}">Vai al riepilogo →</a>
  </div>
{:else}
  <div class="slots">
    {#each slots as slot}
      <div class="slot-card">
        <span class="slot-time">{slot.time}</span>
        <div class="buttons">
          <button
            class:active={slot.selected === 'yes'}
            class="btn-yes"
            on:click={() => setPreference(slot.id, 'yes')}
          >✅ Sì</button>
          <button
            class:active={slot.selected === 'maybe'}
            class="btn-maybe"
            on:click={() => setPreference(slot.id, 'maybe')}
          >🤔 Forse</button>
          <button
            class:active={slot.selected === 'no'}
            class="btn-no"
            on:click={() => setPreference(slot.id, 'no')}
          >❌ No</button>
        </div>
      </div>
    {/each}
  </div>

  <button class="submit-btn" on:click={handleSubmit}>
    Invia Preferenze
  </button>
{/if}

<style>
  .event-info {
    background: #fafafa;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
  }

  .slots {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .slot-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .buttons {
    display: flex;
    gap: 0.5rem;
  }

  .buttons button {
    padding: 0.4rem 0.8rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    background: white;
    cursor: pointer;
    font-size: 0.85rem;
  }

  .btn-yes.active  { background: #c8e6c9; border-color: #4caf50; }
  .btn-maybe.active { background: #fff9c4; border-color: #fbc02d; }
  .btn-no.active   { background: #ffcdd2; border-color: #e53935; }

  .submit-btn {
    margin-top: 1.5rem;
    padding: 0.75rem 2rem;
    background: #1976d2;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    cursor: pointer;
  }

  .submit-btn:hover { background: #1565c0; }

  .success {
    background: #e8f5e9;
    padding: 1.5rem;
    border-radius: 8px;
    margin-top: 1rem;
  }

  .success a { color: #1976d2; }
</style>