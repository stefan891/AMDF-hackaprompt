<!-- src/routes/event/[id]/+page.svelte -->
<script lang="ts">
  import { page } from '$app/state';

  const event = {
    title: 'Riunione di Team — Sprint Planning',
    description: 'Pianificazione del prossimo sprint. Discuteremo le priorità, assegneremo i task e definiremo le deadline. Presenza di tutti i membri del team richiesta.',
    createdBy: 'Marco Rossi',
    createdAt: '18 Gennaio 2025',
    participants: ['Marco Rossi', 'Anna Bianchi', 'Luca Verdi', 'Sara Neri', 'Paolo Gialli'],
    responded: 3
  };

  let slots = $state([
    { id: '1', day: 'Lun', date: '21 Gen', start: '09:00', end: '10:00', selected: '' },
    { id: '2', day: 'Lun', date: '21 Gen', start: '14:00', end: '15:00', selected: '' },
    { id: '3', day: 'Mar', date: '22 Gen', start: '10:00', end: '11:00', selected: '' },
    { id: '4', day: 'Mar', date: '22 Gen', start: '16:00', end: '17:00', selected: '' },
    { id: '5', day: 'Mer', date: '23 Gen', start: '11:00', end: '12:00', selected: '' },
  ]);

  let submitted = $state(false);
  let linkCopied = $state(false);

  let answeredCount = $derived(slots.filter(s => s.selected).length);
  let yesCount = $derived(slots.filter(s => s.selected === 'yes').length);
  let maybeCount = $derived(slots.filter(s => s.selected === 'maybe').length);
  let noCount = $derived(slots.filter(s => s.selected === 'no').length);
  let allAnswered = $derived(answeredCount === slots.length);

  function setPreference(slotId: string, value: string) {
    const slot = slots.find(s => s.id === slotId);
    if (slot) {
      slot.selected = slot.selected === value ? '' : value;
    }
  }

  function handleSubmit() {
    const unanswered = slots.filter(s => !s.selected);
    if (unanswered.length > 0) {
      alert(`Seleziona una preferenza per tutti gli slot! (${unanswered.length} mancanti)`);
      return;
    }
    submitted = true;
  }

  function resetVotes() {
    slots.forEach(s => s.selected = '');
    submitted = false;
  }

  function copyLink() {
    const url = `${window.location.origin}/event/${page.params.id}`;
    navigator.clipboard.writeText(url);
    linkCopied = true;
    setTimeout(() => linkCopied = false, 2000);
  }
</script>

<!-- HEADER EVENTO -->
<section class="event-header">
  <div class="header-top">
    <a href="/" class="back-link">← Torna alla home</a>
    <span class="event-id">ID: {page.params.id}</span>
  </div>

  <div class="event-title-section">
    <h1>{event.title}</h1>
    <div class="event-meta">
      <span class="meta-item">
        👤 {event.createdBy}
      </span>
      <span class="meta-item">
        📅 {event.createdAt}
      </span>
      <span class="meta-item">
        👥 {event.participants.length} invitati
      </span>
      <span class="meta-item">
        ✅ {event.responded}/{event.participants.length} hanno risposto
      </span>
    </div>
  </div>

  {#if event.description}
    <div class="event-description">
      <p>{event.description}</p>
    </div>
  {/if}
</section>

<!-- PARTECIPANTI -->
<section class="participants-section">
  <h3>Partecipanti Invitati</h3>
  <div class="participants-list">
    {#each event.participants as name, i}
      <div class="participant-chip">
        <span class="participant-avatar" style="background: hsl({i * 60}, 70%, 85%)">
          {name.charAt(0)}
        </span>
        <span>{name}</span>
      </div>
    {/each}
  </div>
</section>

{#if submitted}
  <!-- CONFERMA INVIO -->
  <section class="success-section">
    <div class="success-icon">🎉</div>
    <h2>Preferenze Inviate!</h2>
    <p class="success-subtitle">Grazie per aver espresso le tue preferenze.</p>

    <div class="success-summary">
      <div class="summary-item yes">
        <span class="summary-count">{yesCount}</span>
        <span class="summary-label">Disponibile</span>
      </div>
      <div class="summary-item maybe">
        <span class="summary-count">{maybeCount}</span>
        <span class="summary-label">Forse</span>
      </div>
      <div class="summary-item no">
        <span class="summary-count">{noCount}</span>
        <span class="summary-label">Non disponibile</span>
      </div>
    </div>

    <div class="success-detail">
      {#each slots as slot}
        <div class="success-slot">
          <span class="success-slot-time">
            {slot.day} {slot.date} · {slot.start}-{slot.end}
          </span>
          <span class="success-slot-vote {slot.selected}">
            {#if slot.selected === 'yes'}✅ Sì
            {:else if slot.selected === 'maybe'}🤔 Forse
            {:else}❌ No
            {/if}
          </span>
        </div>
      {/each}
    </div>

    <div class="success-actions">
      <a href="/overview/{page.params.id}" class="btn btn-primary">
        📊 Vedi Riepilogo
      </a>
      <button class="btn btn-secondary" onclick={resetVotes}>
        ✏️ Modifica Le Tue Preferenze
      </button>
    </div>
  </section>

{:else}
  <!-- SELEZIONE PREFERENZE -->
  <section class="voting-section">
    <div class="voting-header">
      <div>
        <h2>Esprimi le tue Preferenze</h2>
        <p class="voting-subtitle">Per ogni slot, indica la tua disponibilità</p>
      </div>
      <div class="progress-badge" class:complete={allAnswered}>
        {answeredCount}/{slots.length}
      </div>
    </div>

    <!-- Legenda -->
    <div class="legend">
      <span class="legend-item"><span class="legend-dot yes"></span> Disponibile</span>
      <span class="legend-item"><span class="legend-dot maybe"></span> Forse</span>
      <span class="legend-item"><span class="legend-dot no"></span> Non disponibile</span>
    </div>

    <!-- Slot Cards -->
    <div class="slots-container">
      {#each slots as slot (slot.id)}
        <div
          class="slot-card"
          class:answered={slot.selected}
          class:selected-yes={slot.selected === 'yes'}
          class:selected-maybe={slot.selected === 'maybe'}
          class:selected-no={slot.selected === 'no'}
        >
          <div class="slot-info">
            <div class="slot-day-badge">{slot.day}</div>
            <div class="slot-details">
              <span class="slot-date">{slot.date}</span>
              <span class="slot-time">{slot.start} — {slot.end}</span>
            </div>
          </div>

          <div class="preference-buttons">
            <button
              class="pref-btn pref-yes"
              class:active={slot.selected === 'yes'}
              onclick={() => setPreference(slot.id, 'yes')}
              title="Disponibile"
            >
              <span class="pref-icon">✅</span>
              <span class="pref-label">Sì</span>
            </button>

            <button
              class="pref-btn pref-maybe"
              class:active={slot.selected === 'maybe'}
              onclick={() => setPreference(slot.id, 'maybe')}
              title="Forse"
            >
              <span class="pref-icon">🤔</span>
              <span class="pref-label">Forse</span>
            </button>

            <button
              class="pref-btn pref-no"
              class:active={slot.selected === 'no'}
              onclick={() => setPreference(slot.id, 'no')}
              title="Non disponibile"
            >
              <span class="pref-icon">❌</span>
              <span class="pref-label">No</span>
            </button>
          </div>
        </div>
      {/each}
    </div>

    <!-- Barra di invio -->
    <div class="submit-bar" class:ready={allAnswered}>
      <div class="submit-info">
        {#if allAnswered}
          <span class="submit-ready">✅ Tutte le preferenze selezionate!</span>
        {:else}
          <span class="submit-pending">
            {slots.length - answeredCount} slot rimanenti
          </span>
        {/if}
      </div>
      <button
        class="btn btn-primary btn-submit"
        disabled={!allAnswered}
        onclick={handleSubmit}
      >
        Invia Preferenze →
      </button>
    </div>
  </section>
{/if}

<style>
  :root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --primary-light: #dbeafe;
    --green: #16a34a;
    --green-light: #dcfce7;
    --green-border: #86efac;
    --yellow: #ca8a04;
    --yellow-light: #fef9c3;
    --yellow-border: #fde047;
    --red: #dc2626;
    --red-light: #fee2e2;
    --red-border: #fca5a5;
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-300: #d1d5db;
    --gray-400: #9ca3af;
    --gray-500: #6b7280;
    --gray-600: #4b5563;
    --gray-700: #374151;
    --gray-900: #111827;
    --radius: 12px;
    --radius-sm: 8px;
    --shadow: 0 1px 3px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
  }

  .event-header {
    padding: 0 0 2rem;
  }

  .header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  .back-link {
    color: var(--gray-500);
    text-decoration: none;
    font-size: 0.9rem;
    transition: color 0.2s;
  }

  .back-link:hover {
    color: var(--primary);
  }

  .event-id {
    font-family: monospace;
    font-size: 0.8rem;
    color: var(--gray-400);
    background: var(--gray-100);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
  }

  .event-title-section h1 {
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--gray-900);
    margin: 0 0 0.75rem 0;
    line-height: 1.3;
  }

  .event-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .meta-item {
    font-size: 0.85rem;
    color: var(--gray-500);
    display: flex;
    align-items: center;
    gap: 0.3rem;
  }

  .event-description {
    margin-top: 1.25rem;
    padding: 1rem 1.25rem;
    background: var(--gray-50);
    border-left: 3px solid var(--primary);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  }

  .event-description p {
    color: var(--gray-600);
    line-height: 1.6;
    margin: 0;
    font-size: 0.95rem;
  }

  .participants-section {
    margin-bottom: 2rem;
  }

  .participants-section h3 {
    font-size: 0.9rem;
    color: var(--gray-500);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 0.75rem 0;
  }

  .participants-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .participant-chip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.75rem 0.35rem 0.35rem;
    background: white;
    border: 1px solid var(--gray-200);
    border-radius: 50px;
    font-size: 0.85rem;
    color: var(--gray-700);
  }

  .participant-avatar {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.75rem;
    color: var(--gray-700);
  }

  .voting-section {
    margin-bottom: 2rem;
  }

  .voting-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
  }

  .voting-header h2 {
    font-size: 1.35rem;
    color: var(--gray-900);
    margin: 0 0 0.25rem 0;
  }

  .voting-subtitle {
    color: var(--gray-500);
    font-size: 0.9rem;
    margin: 0;
  }

  .progress-badge {
    background: var(--gray-100);
    color: var(--gray-500);
    padding: 0.4rem 1rem;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 700;
    transition: all 0.3s ease;
    white-space: nowrap;
  }

  .progress-badge.complete {
    background: var(--green-light);
    color: var(--green);
  }

  .legend {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 1.25rem;
    padding: 0.75rem 1rem;
    background: var(--gray-50);
    border-radius: var(--radius-sm);
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    color: var(--gray-600);
  }

  .legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }

  .legend-dot.yes   { background: var(--green); }
  .legend-dot.maybe { background: var(--yellow); }
  .legend-dot.no    { background: var(--red); }

  .slots-container {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .slot-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.25rem;
    background: white;
    border: 2px solid var(--gray-200);
    border-radius: var(--radius);
    transition: all 0.2s ease;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .slot-card:hover {
    border-color: var(--gray-300);
    box-shadow: var(--shadow);
  }

  .slot-card.selected-yes {
    border-color: var(--green-border);
    background: var(--green-light);
  }

  .slot-card.selected-maybe {
    border-color: var(--yellow-border);
    background: var(--yellow-light);
  }

  .slot-card.selected-no {
    border-color: var(--red-border);
    background: var(--red-light);
  }

  .slot-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .slot-day-badge {
    background: var(--primary-light);
    color: var(--primary);
    font-weight: 700;
    font-size: 0.8rem;
    padding: 0.4rem 0.6rem;
    border-radius: 6px;
    text-transform: uppercase;
    min-width: 40px;
    text-align: center;
  }

  .slot-details {
    display: flex;
    flex-direction: column;
  }

  .slot-date {
    font-size: 0.8rem;
    color: var(--gray-500);
  }

  .slot-time {
    font-size: 1rem;
    font-weight: 600;
    color: var(--gray-900);
  }

  .preference-buttons {
    display: flex;
    gap: 0.5rem;
  }

  .pref-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.15rem;
    padding: 0.5rem 0.9rem;
    border: 2px solid var(--gray-200);
    border-radius: var(--radius-sm);
    background: white;
    cursor: pointer;
    transition: all 0.15s ease;
    min-width: 65px;
  }

  .pref-btn:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow);
  }

  .pref-icon {
    font-size: 1.2rem;
  }

  .pref-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--gray-500);
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }

  .pref-yes.active {
    background: var(--green-light);
    border-color: var(--green);
  }
  .pref-yes.active .pref-label { color: var(--green); }

  .pref-maybe.active {
    background: var(--yellow-light);
    border-color: var(--yellow);
  }
  .pref-maybe.active .pref-label { color: var(--yellow); }

  .pref-no.active {
    background: var(--red-light);
    border-color: var(--red);
  }
  .pref-no.active .pref-label { color: var(--red); }

  .submit-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1.5rem;
    padding: 1.25rem 1.5rem;
    background: var(--gray-50);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius);
    transition: all 0.3s ease;
  }

  .submit-bar.ready {
    background: var(--green-light);
    border-color: var(--green-border);
  }

  .submit-pending {
    color: var(--gray-500);
    font-size: 0.9rem;
  }

  .submit-ready {
    color: var(--green);
    font-weight: 600;
    font-size: 0.9rem;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 1.5rem;
    border-radius: var(--radius-sm);
    font-size: 0.95rem;
    font-weight: 600;
    text-decoration: none;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .btn-primary {
    background: var(--primary);
    color: white;
  }

  .btn-primary:hover:not(:disabled) {
    background: var(--primary-dark);
    transform: translateY(-1px);
  }

  .btn-primary:disabled {
    background: var(--gray-300);
    cursor: not-allowed;
    transform: none;
  }

  .btn-secondary {
    background: white;
    color: var(--gray-700);
    border: 1px solid var(--gray-200);
  }

  .btn-secondary:hover {
    background: var(--gray-50);
  }

  .btn-submit {
    padding: 0.75rem 2rem;
  }

  .success-section {
    text-align: center;
    padding: 3rem 1.5rem;
    background: var(--gray-50);
    border-radius: var(--radius);
    margin-bottom: 2rem;
  }

  .success-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .success-section h2 {
    font-size: 1.5rem;
    color: var(--gray-900);
    margin: 0 0 0.5rem 0;
  }

  .success-subtitle {
    color: var(--gray-500);
    margin: 0 0 2rem 0;
  }

  .success-summary {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 2rem;
  }

  .summary-item {
    text-align: center;
    padding: 1rem 1.5rem;
    border-radius: var(--radius-sm);
    min-width: 100px;
  }

  .summary-item.yes   { background: var(--green-light); }
  .summary-item.maybe { background: var(--yellow-light); }
  .summary-item.no    { background: var(--red-light); }

  .summary-count {
    display: block;
    font-size: 1.75rem;
    font-weight: 800;
  }

  .summary-item.yes .summary-count   { color: var(--green); }
  .summary-item.maybe .summary-count { color: var(--yellow); }
  .summary-item.no .summary-count    { color: var(--red); }

  .summary-label {
    font-size: 0.8rem;
    color: var(--gray-500);
    margin-top: 0.25rem;
  }

  .success-detail {
    max-width: 400px;
    margin: 0 auto 2rem;
    text-align: left;
  }

  .success-slot {
    display: flex;
    justify-content: space-between;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--gray-200);
    font-size: 0.9rem;
  }

  .success-slot:last-child {
    border-bottom: none;
  }

  .success-slot-time {
    color: var(--gray-600);
  }

  .success-slot-vote {
    font-weight: 600;
  }

  .success-slot-vote.yes   { color: var(--green); }
  .success-slot-vote.maybe { color: var(--yellow); }
  .success-slot-vote.no    { color: var(--red); }

  .success-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .share-section {
    padding: 1.5rem;
    border: 1px dashed var(--gray-300);
    border-radius: var(--radius);
    background: var(--gray-50);
    margin-bottom: 2rem;
  }

  .share-content {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .share-icon {
    font-size: 1.5rem;
    background: var(--primary-light);
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .share-text h3 {
    font-size: 1rem;
    color: var(--gray-900);
    margin: 0 0 0.2rem 0;
  }

  .share-text p {
    font-size: 0.85rem;
    color: var(--gray-500);
    margin: 0;
  }

  .share-input-group {
    display: flex;
    gap: 0.5rem;
  }

  .share-input-group input {
    flex: 1;
    padding: 0.6rem 0.75rem;
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-sm);
    font-size: 0.85rem;
    color: var(--gray-600);
    background: white;
    outline: none;
  }

  .share-input-group input:focus {
    border-color: var(--primary);
  }

  .btn-copy {
    padding: 0.6rem 1.25rem;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: var(--radius-sm);
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 600;
    white-space: nowrap;
    transition: background 0.2s;
  }

  .btn-copy:hover {
    background: var(--primary-dark);
  }

  @media (max-width: 640px) {
    .event-title-section h1 {
      font-size: 1.35rem;
    }

    .event-meta {
      flex-direction: column;
      gap: 0.5rem;
    }

    .slot-card {
      flex-direction: column;
      align-items: flex-start;
    }

    .preference-buttons {
      width: 100%;
      justify-content: space-between;
    }

    .pref-btn {
      flex: 1;
    }

    .submit-bar {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }

    .success-summary {
      flex-direction: column;
      align-items: center;
      gap: 0.75rem;
    }

    .legend {
      flex-direction: column;
      gap: 0.5rem;
    }

    .share-input-group {
      flex-direction: column;
    }
  }
</style>