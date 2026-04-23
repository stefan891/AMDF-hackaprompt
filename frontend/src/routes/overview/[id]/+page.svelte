<!-- src/routes/overview/[id]/+page.svelte -->
<script lang="ts">
  import { page } from '$app/stores';

  // Dati finti per la demo
  const results = [
    { time: 'Lunedì 21 Gen — 09:00-10:00',    yes: 4, maybe: 1, no: 1 },
    { time: 'Martedì 22 Gen — 14:00-15:00',   yes: 2, maybe: 3, no: 1 },
    { time: 'Mercoledì 23 Gen — 11:00-12:00', yes: 5, maybe: 0, no: 1 }
  ];

  const totalVoters = 6;

  // Trova il migliore (più "yes")
  const best = results.reduce((a, b) => (b.yes > a.yes ? b : a));
</script>

<h2>📊 Riepilogo Evento</h2>
<p>ID Evento: <strong>{$page.params.id}</strong></p>

<!-- Statistiche -->
<div class="stats">
  <div class="stat">
    <span class="number">{totalVoters}</span>
    <span class="label">Partecipanti</span>
  </div>
  <div class="stat">
    <span class="number">{results.length}</span>
    <span class="label">Slot proposti</span>
  </div>
</div>

<!-- Miglior slot -->
<div class="best-slot">
  <h3>🎉 Miglior Slot</h3>
  <p><strong>{best.time}</strong></p>
  <p>✅ {best.yes} sì · 🤔 {best.maybe} forse · ❌ {best.no} no</p>
</div>

<!-- Dettaglio per slot -->
<h3>Tutti gli Slot</h3>

{#each results as slot}
  <div class="result-card" class:is-best={slot === best}>
    <div class="result-header">
      <span>{slot.time}</span>
      {#if slot === best}
        <span class="badge">⭐ Migliore</span>
      {/if}
    </div>

    <!-- Barra di progresso -->
    <div class="bar">
      <div class="bar-yes"   style="width: {(slot.yes / totalVoters) * 100}%"></div>
      <div class="bar-maybe" style="width: {(slot.maybe / totalVoters) * 100}%"></div>
      <div class="bar-no"    style="width: {(slot.no / totalVoters) * 100}%"></div>
    </div>

    <div class="votes">
      ✅ {slot.yes} · 🤔 {slot.maybe} · ❌ {slot.no}
    </div>
  </div>
{/each}

<div class="actions">
  <a href="/event/{$page.params.id}">← Torna all'evento</a>
</div>

<style>
  .stats {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
  }

  .stat {
    flex: 1;
    text-align: center;
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 8px;
    border: 1px solid #ddd;
  }

  .number {
    display: block;
    font-size: 2rem;
    font-weight: bold;
    color: #1976d2;
  }

  .label {
    font-size: 0.85rem;
    color: #777;
  }

  .best-slot {
    background: #e8f5e9;
    border: 2px solid #4caf50;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 2rem;
  }

  .result-card {
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 1rem;
    margin-bottom: 0.75rem;
  }

  .result-card.is-best {
    border-color: #4caf50;
    border-width: 2px;
    background: #f1f8e9;
  }

  .result-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    font-weight: bold;
  }

  .badge {
    background: #4caf50;
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.8rem;
  }

  .bar {
    display: flex;
    height: 10px;
    border-radius: 5px;
    overflow: hidden;
    background: #eee;
    margin-bottom: 0.5rem;
  }

  .bar-yes   { background: #4caf50; }
  .bar-maybe { background: #ffc107; }
  .bar-no    { background: #e53935; }

  .votes {
    font-size: 0.9rem;
    color: #555;
  }

  .actions {
    margin-top: 2rem;
  }

  .actions a {
    color: #1976d2;
  }
</style>