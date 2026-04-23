<!-- src/routes/user/[id]/+page.svelte -->
<script lang="ts">
  import { page } from '$app/state';

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // UTENTE CORRENTE (simulato — in futuro verrà dallo store/auth)
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  const currentUser = {
    id: 'user-001',
    name: 'Marco Rossi',
    email: 'marco.rossi@email.com',
    picture: '',
    memberSince: 'Gennaio 2025'
  };

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // EVENTI DEMO (in futuro verranno dall'API: GET /users/:id/events)
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  const allEvents = [
    {
      id: 'evt-001',
      title: 'Sprint Planning Q1',
      description: 'Pianificazione sprint per il primo trimestre',
      createdBy: 'user-001',        // ← stesso ID dell'utente = CREATOR
      creatorName: 'Marco Rossi',
      createdAt: '2025-01-15',
      status: 'active',
      totalSlots: 3,
      totalInvited: 5,
      totalResponded: 3,
      bestSlot: 'Lun 21 Gen · 09:00-10:00',
      participants: ['Anna Bianchi', 'Luca Verdi', 'Sara Neri', 'Paolo Gialli', 'Giulia Blu']
    },
    {
      id: 'evt-002',
      title: 'Design Review',
      description: 'Revisione design del nuovo prodotto',
      createdBy: 'user-001',
      creatorName: 'Marco Rossi',
      createdAt: '2025-01-18',
      status: 'active',
      totalSlots: 4,
      totalInvited: 3,
      totalResponded: 1,
      bestSlot: null,
      participants: ['Anna Bianchi', 'Luca Verdi', 'Sara Neri']
    },
    {
      id: 'evt-003',
      title: 'Team Retrospective',
      description: 'Retrospettiva mensile del team',
      createdBy: 'user-001',
      creatorName: 'Marco Rossi',
      createdAt: '2025-01-10',
      status: 'closed',
      totalSlots: 2,
      totalInvited: 6,
      totalResponded: 6,
      bestSlot: 'Ven 17 Gen · 16:00-17:00',
      participants: ['Anna Bianchi', 'Luca Verdi', 'Sara Neri', 'Paolo Gialli', 'Giulia Blu', 'Fabio Arancio']
    },
    {
      id: 'evt-004',
      title: 'Workshop UX',
      description: 'Workshop su metodologie UX research',
      createdBy: 'user-099',         // ← ID diverso = PARTECIPANTE
      creatorName: 'Anna Bianchi',
      createdAt: '2025-01-20',
      status: 'active',
      totalSlots: 3,
      totalInvited: 8,
      totalResponded: 5,
      bestSlot: 'Mer 29 Gen · 10:00-12:00',
      myPreference: 'submitted',     // ha già votato
      participants: ['Marco Rossi', 'Luca Verdi', 'Sara Neri']
    },
    {
      id: 'evt-005',
      title: 'All Hands Meeting',
      description: 'Riunione generale mensile',
      createdBy: 'user-050',
      creatorName: 'Luca Verdi',
      createdAt: '2025-01-22',
      status: 'active',
      totalSlots: 2,
      totalInvited: 15,
      totalResponded: 8,
      bestSlot: null,
      myPreference: 'pending',       // non ha ancora votato
      participants: ['Marco Rossi', 'Anna Bianchi']
    },
    {
      id: 'evt-006',
      title: 'Cena di Team',
      description: 'Cena sociale di fine mese',
      createdBy: 'user-077',
      creatorName: 'Sara Neri',
      createdAt: '2025-01-12',
      status: 'closed',
      totalSlots: 3,
      totalInvited: 10,
      totalResponded: 10,
      bestSlot: 'Sab 25 Gen · 20:00-23:00',
      myPreference: 'submitted',
      participants: ['Marco Rossi', 'Anna Bianchi', 'Luca Verdi']
    }
  ];

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // STATO REATTIVO
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  let activeTab = $state<'created' | 'invited' | 'all'>('all');
  let searchQuery = $state('');
  let statusFilter = $state<'all' | 'active' | 'closed'>('all');
  let linkCopiedId = $state<string | null>(null);

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // CHECK: l'utente è il creator dell'evento?
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  function isCreator(event: typeof allEvents[0]): boolean {
    return event.createdBy === currentUser.id;
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // VALORI DERIVATI (si aggiornano automaticamente)
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  let createdEvents = $derived(allEvents.filter(e => isCreator(e)));
  let invitedEvents = $derived(allEvents.filter(e => !isCreator(e)));

  let filteredEvents = $derived.by(() => {
    let events = allEvents;

    // Filtra per tab
    if (activeTab === 'created') {
      events = events.filter(e => isCreator(e));
    } else if (activeTab === 'invited') {
      events = events.filter(e => !isCreator(e));
    }

    // Filtra per stato
    if (statusFilter !== 'all') {
      events = events.filter(e => e.status === statusFilter);
    }

    // Filtra per ricerca
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      events = events.filter(e =>
        e.title.toLowerCase().includes(q) ||
        e.description.toLowerCase().includes(q) ||
        e.creatorName.toLowerCase().includes(q)
      );
    }

    return events;
  });

  // Statistiche
  let totalCreated = $derived(createdEvents.length);
  let totalInvited = $derived(invitedEvents.length);
  let pendingVotes = $derived(invitedEvents.filter(e => e.myPreference === 'pending' && e.status === 'active').length);
  let activeEvents = $derived(allEvents.filter(e => e.status === 'active').length);

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // AZIONI
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  function copyEventLink(eventId: string) {
    const url = `${window.location.origin}/event/${eventId}`;
    navigator.clipboard.writeText(url);
    linkCopiedId = eventId;
    setTimeout(() => linkCopiedId = null, 2000);
  }

  function formatDate(dateStr: string): string {
    const d = new Date(dateStr);
    return d.toLocaleDateString('it-IT', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  }

  function getResponsePercentage(event: typeof allEvents[0]): number {
    if (event.totalInvited === 0) return 0;
    return Math.round((event.totalResponded / event.totalInvited) * 100);
  }
</script>

<!-- ═══════════════════════════════════ -->
<!--           PROFILO UTENTE           -->
<!-- ═══════════════════════════════════ -->
<section class="profile-header">
  <div class="profile-top">
    <a href="/" class="back-link">← Torna alla home</a>
  </div>

  <div class="profile-info">
    <div class="avatar-large">
      {currentUser.name.charAt(0)}
    </div>
    <div class="profile-details">
      <h1>{currentUser.name}</h1>
      <p class="profile-email">{currentUser.email}</p>
      <p class="profile-since">Membro da {currentUser.memberSince}</p>
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════ -->
<!--           STATISTICHE              -->
<!-- ═══════════════════════════════════ -->
<section class="stats-grid">
  <div class="stat-card">
    <span class="stat-icon">📝</span>
    <span class="stat-number">{totalCreated}</span>
    <span class="stat-label">Eventi Creati</span>
  </div>
  <div class="stat-card">
    <span class="stat-icon">📩</span>
    <span class="stat-number">{totalInvited}</span>
    <span class="stat-label">Inviti Ricevuti</span>
  </div>
  <div class="stat-card accent">
    <span class="stat-icon">⚡</span>
    <span class="stat-number">{activeEvents}</span>
    <span class="stat-label">Eventi Attivi</span>
  </div>
  <div class="stat-card" class:alert={pendingVotes > 0}>
    <span class="stat-icon">🗳️</span>
    <span class="stat-number">{pendingVotes}</span>
    <span class="stat-label">Voti in Attesa</span>
  </div>
</section>

<!-- ═══════════════════════════════════ -->
<!--        BANNER VOTI PENDING         -->
<!-- ═══════════════════════════════════ -->
{#if pendingVotes > 0}
  <section class="pending-banner">
    <span class="pending-icon">🔔</span>
    <div class="pending-text">
      <strong>Hai {pendingVotes} {pendingVotes === 1 ? 'evento' : 'eventi'} in attesa di voto!</strong>
      <p>Esprimi le tue preferenze per aiutare gli organizzatori.</p>
    </div>
    <button class="btn btn-small" onclick={() => { activeTab = 'invited'; statusFilter = 'active'; }}>
      Vedi inviti →
    </button>
  </section>
{/if}

<!-- ═══════════════════════════════════ -->
<!--          TABS + FILTRI             -->
<!-- ═══════════════════════════════════ -->
<section class="controls-section">
  <!-- Tabs -->
  <div class="tabs">
    <button
      class="tab"
      class:active={activeTab === 'all'}
      onclick={() => activeTab = 'all'}
    >
      Tutti ({allEvents.length})
    </button>
    <button
      class="tab"
      class:active={activeTab === 'created'}
      onclick={() => activeTab = 'created'}
    >
      📝 Creati da me ({totalCreated})
    </button>
    <button
      class="tab"
      class:active={activeTab === 'invited'}
      onclick={() => activeTab = 'invited'}
    >
      📩 Invitato ({totalInvited})
    </button>
  </div>

  <!-- Filtri -->
  <div class="filters-row">
    <div class="search-box">
      <span class="search-icon">🔍</span>
      <input
        type="text"
        placeholder="Cerca evento..."
        bind:value={searchQuery}
      />
    </div>
    <div class="status-filter">
      <button
        class="filter-btn"
        class:active={statusFilter === 'all'}
        onclick={() => statusFilter = 'all'}
      >Tutti</button>
      <button
        class="filter-btn"
        class:active={statusFilter === 'active'}
        onclick={() => statusFilter = 'active'}
      >🟢 Attivi</button>
      <button
        class="filter-btn"
        class:active={statusFilter === 'closed'}
        onclick={() => statusFilter = 'closed'}
      >🔴 Chiusi</button>
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════ -->
<!--          LISTA EVENTI              -->
<!-- ═══════════════════════════════════ -->
<section class="events-list">
  {#if filteredEvents.length === 0}
    <div class="empty-state">
      <span class="empty-icon">📭</span>
      <h3>Nessun evento trovato</h3>
      <p>Prova a cambiare i filtri o
        <a href="/create">crea un nuovo evento</a>.
      </p>
    </div>
  {:else}
    {#each filteredEvents as event (event.id)}
      <div class="event-card" class:is-creator={isCreator(event)} class:is-closed={event.status === 'closed'}>
        <!-- Header card -->
        <div class="card-header">
          <div class="card-title-row">
            <h3>{event.title}</h3>
            <div class="card-badges">
              <!-- Badge ruolo -->
              {#if isCreator(event)}
                <span class="badge badge-creator">👑 Creatore</span>
              {:else}
                <span class="badge badge-participant">👤 Partecipante</span>
              {/if}
              <!-- Badge stato -->
              {#if event.status === 'active'}
                <span class="badge badge-active">🟢 Attivo</span>
              {:else}
                <span class="badge badge-closed">🔴 Chiuso</span>
              {/if}
            </div>
          </div>
          <p class="card-description">{event.description}</p>
          <div class="card-meta">
            {#if !isCreator(event)}
              <span>Organizzato da <strong>{event.creatorName}</strong></span>
            {/if}
            <span>📅 {formatDate(event.createdAt)}</span>
            <span>🕐 {event.totalSlots} slot proposti</span>
          </div>
        </div>

        <!-- Barra progresso risposte -->
        <div class="response-section">
          <div class="response-header">
            <span class="response-label">Risposte</span>
            <span class="response-count">{event.totalResponded}/{event.totalInvited}</span>
          </div>
          <div class="response-bar">
            <div
              class="response-fill"
              style="width: {getResponsePercentage(event)}%"
            ></div>
          </div>
          <span class="response-percent">{getResponsePercentage(event)}% ha risposto</span>
        </div>

        <!-- Miglior slot (se disponibile) -->
        {#if event.bestSlot}
          <div class="best-slot-mini">
            <span class="best-label">⭐ Miglior slot:</span>
            <span class="best-value">{event.bestSlot}</span>
          </div>
        {/if}

        <!-- Preferenza personale (solo per invitati) -->
        {#if !isCreator(event) && event.status === 'active'}
          <div class="my-preference" class:pending={event.myPreference === 'pending'}>
            {#if event.myPreference === 'submitted'}
              <span>✅ Hai già espresso le tue preferenze</span>
            {:else}
              <span>⚠️ Non hai ancora votato!</span>
            {/if}
          </div>
        {/if}

        <!-- Partecipanti -->
        <div class="card-participants">
          <span class="participants-label">Partecipanti:</span>
          <div class="participants-avatars">
            {#each event.participants.slice(0, 4) as name, i}
              <span
                class="mini-avatar"
                style="background: hsl({i * 70 + 30}, 65%, 80%)"
                title={name}
              >
                {name.charAt(0)}
              </span>
            {/each}
            {#if event.participants.length > 4}
              <span class="mini-avatar more">
                +{event.participants.length - 4}
              </span>
            {/if}
          </div>
        </div>

        <!-- ═══════════════════════════════════ -->
        <!--    AZIONI — diverse per ruolo       -->
        <!-- ═══════════════════════════════════ -->
        <div class="card-actions">
          {#if isCreator(event)}
            <!-- CREATOR: può modificare, condividere link, vedere overview -->
            <a href="/event/{event.id}" class="btn btn-primary">
              ✏️ Modifica Evento
            </a>
            <a href="/overview/{event.id}" class="btn btn-secondary">
              📊 Vedi Risultati
            </a>
            <button
              class="btn btn-outline"
              onclick={() => copyEventLink(event.id)}
            >
              {#if linkCopiedId === event.id}
                ✅ Link Copiato!
              {:else}
                🔗 Condividi Link
              {/if}
            </button>
          {:else}
            <!-- PARTECIPANTE: può votare/modificare preferenze e vedere overview -->
            {#if event.status === 'active'}
              {#if event.myPreference === 'pending'}
                <a href="/event/{event.id}" class="btn btn-primary pulse">
                  🗳️ Vota Ora
                </a>
              {:else}
                <a href="/event/{event.id}" class="btn btn-secondary">
                  ✏️ Modifica Preferenze
                </a>
              {/if}
            {/if}
            <a href="/overview/{event.id}" class="btn btn-secondary">
              📊 Vedi Overview
            </a>
          {/if}
        </div>
      </div>
    {/each}
  {/if}
</section>

<!-- BOTTONE CREA EVENTO -->
<section class="create-cta">
  <a href="/create" class="btn btn-primary btn-large">
    ➕ Crea Nuovo Evento
  </a>
</section>

<style>
  /* ===================== */
  /*     VARIABILI         */
  /* ===================== */
  :root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --primary-light: #dbeafe;
    --green: #16a34a;
    --green-light: #dcfce7;
    --yellow: #ca8a04;
    --yellow-light: #fef9c3;
    --red: #dc2626;
    --red-light: #fee2e2;
    --orange: #ea580c;
    --orange-light: #fff7ed;
    --purple: #7c3aed;
    --purple-light: #ede9fe;
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
    --shadow: 0 1px 3px rgba(0,0,0,0.08);
    --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
  }

  /* ===================== */
  /*    PROFILO HEADER     */
  /* ===================== */
  .profile-header {
    margin-bottom: 2rem;
  }

  .profile-top {
    margin-bottom: 1.5rem;
  }

  .back-link {
    color: var(--gray-500);
    text-decoration: none;
    font-size: 0.9rem;
  }

  .back-link:hover {
    color: var(--primary);
  }

  .profile-info {
    display: flex;
    align-items: center;
    gap: 1.25rem;
  }

  .avatar-large {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary), var(--purple));
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 700;
    flex-shrink: 0;
  }

  .profile-details h1 {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--gray-900);
    margin: 0;
  }

  .profile-email {
    color: var(--gray-500);
    font-size: 0.9rem;
    margin: 0.15rem 0 0;
  }

  .profile-since {
    color: var(--gray-400);
    font-size: 0.8rem;
    margin: 0.15rem 0 0;
  }

  /* ===================== */
  /*     STATISTICHE       */
  /* ===================== */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .stat-card {
    background: white;
    border: 1px solid var(--gray-200);
    border-radius: var(--radius);
    padding: 1.25rem;
    text-align: center;
    transition: all 0.2s;
  }

  .stat-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
  }

  .stat-card.accent {
    border-color: var(--primary-light);
    background: var(--primary-light);
  }

  .stat-card.alert {
    border-color: var(--orange);
    background: var(--orange-light);
  }

  .stat-icon {
    display: block;
    font-size: 1.5rem;
    margin-bottom: 0.35rem;
  }

  .stat-number {
    display: block;
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--gray-900);
  }

  .stat-card.accent .stat-number { color: var(--primary); }
  .stat-card.alert .stat-number  { color: var(--orange); }

  .stat-label {
    font-size: 0.8rem;
    color: var(--gray-500);
  }

  /* ===================== */
  /*    PENDING BANNER     */
  /* ===================== */
  .pending-banner {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.25rem;
    background: var(--yellow-light);
    border: 1px solid #fde68a;
    border-radius: var(--radius);
    margin-bottom: 1.5rem;
  }

  .pending-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
  }

  .pending-text {
    flex: 1;
  }

  .pending-text strong {
    color: var(--gray-900);
    font-size: 0.95rem;
  }

  .pending-text p {
    color: var(--gray-600);
    font-size: 0.85rem;
    margin: 0.15rem 0 0;
  }

  /* ===================== */
  /*    TABS + FILTRI      */
  /* ===================== */
  .controls-section {
    margin-bottom: 1.5rem;
  }

  .tabs {
    display: flex;
    gap: 0.25rem;
    background: var(--gray-100);
    border-radius: var(--radius-sm);
    padding: 0.25rem;
    margin-bottom: 1rem;
  }

  .tab {
    flex: 1;
    padding: 0.6rem 1rem;
    border: none;
    background: none;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--gray-500);
    cursor: pointer;
    transition: all 0.2s;
  }

  .tab:hover {
    color: var(--gray-700);
  }

  .tab.active {
    background: white;
    color: var(--gray-900);
    box-shadow: var(--shadow);
  }

  .filters-row {
    display: flex;
    gap: 1rem;
    align-items: center;
    flex-wrap: wrap;
  }

  .search-box {
    flex: 1;
    min-width: 200px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: white;
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-sm);
    padding: 0 0.75rem;
  }

  .search-icon {
    font-size: 0.9rem;
    flex-shrink: 0;
  }

  .search-box input {
    flex: 1;
    border: none;
    padding: 0.6rem 0;
    font-size: 0.9rem;
    outline: none;
    background: none;
    color: var(--gray-700);
  }

  .status-filter {
    display: flex;
    gap: 0.25rem;
    background: var(--gray-100);
    border-radius: 6px;
    padding: 0.2rem;
  }

  .filter-btn {
    padding: 0.4rem 0.75rem;
    border: none;
    background: none;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--gray-500);
    cursor: pointer;
    transition: all 0.2s;
  }

  .filter-btn.active {
    background: white;
    color: var(--gray-900);
    box-shadow: var(--shadow);
  }

  /* ===================== */
  /*     EVENT CARDS       */
  /* ===================== */
  .events-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .event-card {
    background: white;
    border: 1px solid var(--gray-200);
    border-radius: var(--radius);
    padding: 1.5rem;
    transition: all 0.2s;
  }

  .event-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-1px);
  }

  .event-card.is-creator {
    border-left: 4px solid var(--primary);
  }

  .event-card.is-closed {
    opacity: 0.75;
  }

  .card-header {
    margin-bottom: 1rem;
  }

  .card-title-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 0.5rem;
    flex-wrap: wrap;
  }

  .card-title-row h3 {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--gray-900);
    margin: 0;
  }

  .card-badges {
    display: flex;
    gap: 0.35rem;
    flex-wrap: wrap;
  }

  .badge {
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    white-space: nowrap;
  }

  .badge-creator    { background: var(--purple-light); color: var(--purple); }
  .badge-participant { background: var(--primary-light); color: var(--primary); }
  .badge-active     { background: var(--green-light); color: var(--green); }
  .badge-closed     { background: var(--red-light); color: var(--red); }

  .card-description {
    color: var(--gray-600);
    font-size: 0.9rem;
    margin: 0 0 0.75rem;
    line-height: 1.5;
  }

  .card-meta {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    font-size: 0.8rem;
    color: var(--gray-400);
  }

  /* ===================== */
  /*   BARRA RISPOSTE      */
  /* ===================== */
  .response-section {
    margin-bottom: 1rem;
    padding: 0.75rem 1rem;
    background: var(--gray-50);
    border-radius: var(--radius-sm);
  }

  .response-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.35rem;
  }

  .response-label {
    font-size: 0.8rem;
    color: var(--gray-500);
    font-weight: 600;
  }

  .response-count {
    font-size: 0.8rem;
    color: var(--gray-700);
    font-weight: 700;
  }

  .response-bar {
    height: 6px;
    background: var(--gray-200);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 0.25rem;
  }

  .response-fill {
    height: 100%;
    background: var(--primary);
    border-radius: 3px;
    transition: width 0.5s ease;
  }

  .response-percent {
    font-size: 0.75rem;
    color: var(--gray-400);
  }

  /* ===================== */
  /*    MIGLIOR SLOT       */
  /* ===================== */
  .best-slot-mini {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: var(--green-light);
    border-radius: 6px;
    margin-bottom: 1rem;
    font-size: 0.85rem;
  }

  .best-label {
    color: var(--green);
    font-weight: 600;
  }

  .best-value {
    color: var(--gray-700);
    font-weight: 500;
  }

  /* ===================== */
  /*   MIA PREFERENZA      */
  /* ===================== */
  .my-preference {
    padding: 0.5rem 0.75rem;
    border-radius: 6px;
    font-size: 0.85rem;
    margin-bottom: 1rem;
    background: var(--green-light);
    color: var(--green);
  }

  .my-preference.pending {
    background: var(--orange-light);
    color: var(--orange);
    font-weight: 600;
  }

  /* ===================== */
  /*     PARTECIPANTI      */
  /* ===================== */
  .card-participants {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .participants-label {
    font-size: 0.8rem;
    color: var(--gray-400);
    white-space: nowrap;
  }

  .participants-avatars {
    display: flex;
    gap: 0;
  }

  .mini-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--gray-700);
    border: 2px solid white;
    margin-left: -6px;
  }

  .mini-avatar:first-child {
    margin-left: 0;
  }

  .mini-avatar.more {
    background: var(--gray-200);
    color: var(--gray-600);
    font-size: 0.65rem;
  }

  /* ===================== */
  /*     AZIONI CARD       */
  /* ===================== */
  .card-actions {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    padding-top: 1rem;
    border-top: 1px solid var(--gray-100);
  }

  /* ===================== */
  /*       BOTTONI         */
  /* ===================== */
  .btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.55rem 1.1rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    text-decoration: none;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }

  .btn-primary {
    background: var(--primary);
    color: white;
  }

  .btn-primary:hover {
    background: var(--primary-dark);
    transform: translateY(-1px);
  }

  .btn-secondary {
    background: var(--gray-100);
    color: var(--gray-700);
  }

  .btn-secondary:hover {
    background: var(--gray-200);
  }

  .btn-outline {
    background: white;
    color: var(--gray-600);
    border: 1px solid var(--gray-200);
  }

  .btn-outline:hover {
    border-color: var(--gray-400);
  }

  .btn-small {
    padding: 0.4rem 0.9rem;
    font-size: 0.8rem;
    background: white;
    border: 1px solid #fde68a;
    color: var(--yellow);
  }

  .btn-large {
    padding: 0.85rem 2rem;
    font-size: 1rem;
  }

  .btn.pulse {
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.4); }
    70% { box-shadow: 0 0 0 8px rgba(37, 99, 235, 0); }
    100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
  }

  /* ===================== */
  /*     EMPTY STATE       */
  /* ===================== */
  .empty-state {
    text-align: center;
    padding: 4rem 2rem;
    background: var(--gray-50);
    border-radius: var(--radius);
    border: 1px dashed var(--gray-300);
  }

  .empty-icon {
    font-size: 3rem;
    display: block;
    margin-bottom: 1rem;
  }

  .empty-state h3 {
    color: var(--gray-700);
    margin: 0 0 0.5rem;
  }

  .empty-state p {
    color: var(--gray-500);
    font-size: 0.9rem;
  }

  .empty-state a {
    color: var(--primary);
  }

  /* ===================== */
  /*     CTA FINALE        */
  /* ===================== */
  .create-cta {
    text-align: center;
    padding: 2rem 0 3rem;
  }

  /* ===================== */
  /*     RESPONSIVE        */
  /* ===================== */
  @media (max-width: 768px) {
    .stats-grid {
      grid-template-columns: repeat(2, 1fr);
    }

    .pending-banner {
      flex-direction: column;
      text-align: center;
    }

    .tabs {
      flex-direction: column;
    }

    .filters-row {
      flex-direction: column;
    }

    .card-title-row {
      flex-direction: column;
    }

    .card-actions {
      flex-direction: column;
    }

    .card-actions .btn {
      width: 100%;
      justify-content: center;
    }
  }
</style>