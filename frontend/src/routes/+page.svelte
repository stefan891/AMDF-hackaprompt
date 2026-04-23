<!-- src/routes/+page.svelte -->
<script lang="ts">
// Stato per animazione dei numeri (puramente estetico)
let showContent = true;

// Dati per le feature cards
const steps = [
{
icon: '🔐',
title: 'Accedi',
description: 'Fai login con il tuo account Google in un click.'
},
{
icon: '📝',
title: 'Crea Evento',
description: 'Imposta titolo, descrizione e proponi degli slot temporali.'
},
{
icon: '🔗',
title: 'Condividi',
description: 'Invia il link ai partecipanti — nessuna registrazione richiesta.'
},
{
icon: '🗳️',
title: 'Vota',
description: 'Ogni partecipante esprime le sue preferenze: sì, forse o no.'
},
{
icon: '📊',
title: 'Risultati',
description: 'Vedi il riepilogo e trova automaticamente lo slot migliore.'
}
];

// Dati per le statistiche demo
const stats = [
{ value: '5 min', label: 'Per creare un evento' },
{ value: '1 click', label: 'Per votare' },
{ value: '0', label: 'Email necessarie' }
];
</script>

<!-- HERO SECTION -->
<section class="hero">
<div class="hero-badge">✨ Organizza eventi senza stress</div>
<h1>
Trova il momento
<span class="gradient-text">perfetto</span>
per tutti
</h1>
<p class="hero-subtitle">
Event Scheduler ti aiuta a coordinare disponibilità e preferenze
del tuo team in pochi click. Niente più catene di email infinite.
</p>
<div class="hero-buttons">
<a href="/login" class="btn btn-primary">
🚀 Inizia Ora
</a>
</div>
</section>

<!-- STATS BAR -->
<section class="stats-bar">
{#each stats as stat}
<div class="stat-item">
<span class="stat-value">{stat.value}</span>
<span class="stat-label">{stat.label}</span>
</div>
{/each}
</section>

<!-- COME FUNZIONA -->
<section class="how-it-works">
<h2>Come Funziona</h2>
<p class="section-subtitle">5 semplici passi per organizzare il tuo evento</p>

<div class="steps-grid">
{#each steps as step, index}
<div class="step-card">
<div class="step-number">{index + 1}</div>
<div class="step-icon">{step.icon}</div>
<h3>{step.title}</h3>
<p>{step.description}</p>
</div>
{/each}
</div>
</section>

<!-- PREVIEW / MOCKUP -->
<section class="preview-section">
<h2>Semplice e Intuitivo</h2>
<p class="section-subtitle">Interfaccia pulita, risultati immediati</p>

<div class="preview-cards">
<!-- Card: Creazione -->
<div class="preview-card">
<div class="preview-header">
<span class="preview-dot red"></span>
<span class="preview-dot yellow"></span>
<span class="preview-dot green"></span>
<span class="preview-title">Crea Evento</span>
</div>
<div class="preview-body">
<div class="fake-input">📅 Riunione di Team</div>
<div class="fake-slots">
<div class="fake-slot">Lun 21 Gen · 09:00</div>
<div class="fake-slot">Mar 22 Gen · 14:00</div>
<div class="fake-slot">Mer 23 Gen · 11:00</div>
</div>
</div>
</div>

<!-- Card: Votazione -->
<div class="preview-card">
<div class="preview-header">
<span class="preview-dot red"></span>
<span class="preview-dot yellow"></span>
<span class="preview-dot green"></span>
<span class="preview-title">Vota Preferenze</span>
</div>
<div class="preview-body">
<div class="fake-vote-row">
<span>Lun 09:00</span>
<span class="vote-yes">✅ Sì</span>
</div>
<div class="fake-vote-row">
<span>Mar 14:00</span>
<span class="vote-maybe">🤔 Forse</span>
</div>
<div class="fake-vote-row">
<span>Mer 11:00</span>
<span class="vote-yes">✅ Sì</span>
</div>
</div>
</div>

<!-- Card: Risultati -->
<div class="preview-card">
<div class="preview-header">
<span class="preview-dot red"></span>
<span class="preview-dot yellow"></span>
<span class="preview-dot green"></span>
<span class="preview-title">Risultati</span>
</div>
<div class="preview-body">
<div class="fake-result">
<span>Lun 09:00</span>
<div class="fake-bar">
<div class="fake-bar-fill" style="width: 80%"></div>
</div>
<span class="fake-percent">80%</span>
</div>
<div class="fake-result">
<span>Mar 14:00</span>
<div class="fake-bar">
<div class="fake-bar-fill" style="width: 50%"></div>
</div>
<span class="fake-percent">50%</span>
</div>
<div class="fake-result best">
<span>⭐ Mer 11:00</span>
<div class="fake-bar">
<div class="fake-bar-fill winner" style="width: 95%"></div>
</div>
<span class="fake-percent">95%</span>
</div>
</div>
</div>
</div>
</section>

<!-- CALL TO ACTION FINALE -->
<section class="cta-section">
<h2>Pronto a organizzare il tuo primo evento?</h2>
<p>È gratuito, veloce e non richiede installazione.</p>
<a href="/login" class="btn btn-primary btn-large">
Crea il tuo primo evento →
</a>
</section>

<!-- FOOTER -->
<footer>
<p>Fatto con ❤️ dal team AMDF · HackapromptAI 2026</p>
</footer>

<style>
/* ===================== */
/* VARIABILI GLOBALI */
/* ===================== */

:root {
--primary: #2563eb;
--primary-dark: #1d4ed8;
--primary-light: #dbeafe;
--green: #16a34a;
--green-light: #dcfce7;
--yellow: #eab308;
--red: #dc2626;
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-900: #111827;
--radius: 12px;
--shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
--shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1);
}

/* ===================== */
/* HERO SECTION */
/* ===================== */

.hero {
text-align: center;
padding: 4rem 1rem 3rem;
}

.hero-badge {
display: inline-block;
background: var(--primary-light);
color: var(--primary);
padding: 0.4rem 1rem;
border-radius: 50px;
font-size: 0.85rem;
font-weight: 600;
margin-bottom: 1.5rem;
}

.hero h1 {
font-size: 2.75rem;
font-weight: 800;
color: var(--gray-900);
line-height: 1.2;
margin: 0 0 1rem 0;
}

.gradient-text {
background: linear-gradient(135deg, var(--primary), #7c3aed);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
}

.hero-subtitle {
font-size: 1.15rem;
color: var(--gray-500);
max-width: 550px;
margin: 0 auto 2rem;
line-height: 1.6;
}

.hero-buttons {
display: flex;
gap: 1rem;
justify-content: center;
flex-wrap: wrap;
}

/* ===================== */
/* BOTTONI */
/* ===================== */

.btn {
display: inline-flex;
align-items: center;
gap: 0.5rem;
padding: 0.75rem 1.75rem;
border-radius: 8px;
font-size: 1rem;
font-weight: 600;
text-decoration: none;
transition: all 0.2s ease;
cursor: pointer;
}

.btn-primary {
background: var(--primary);
color: white;
box-shadow: 0 2px 4px rgba(37, 99, 235, 0.3);
}

.btn-primary:hover {
background: var(--primary-dark);
transform: translateY(-1px);
box-shadow: 0 4px 8px rgba(37, 99, 235, 0.4);
}

.btn-secondary {
background: white;
color: var(--gray-700);
border: 1px solid var(--gray-200);
}

.btn-secondary:hover {
background: var(--gray-50);
border-color: var(--gray-400);
}

.btn-large {
padding: 1rem 2.5rem;
font-size: 1.1rem;
}

/* ===================== */
/* STATS BAR */
/* ===================== */

.stats-bar {
display: flex;
justify-content: center;
gap: 3rem;
padding: 2rem 1rem;
margin: 1rem 0 3rem;
border-top: 1px solid var(--gray-200);
border-bottom: 1px solid var(--gray-200);
flex-wrap: wrap;
}

.stat-item {
text-align: center;
}

.stat-value {
display: block;
font-size: 1.5rem;
font-weight: 800;
color: var(--primary);
}

.stat-label {
font-size: 0.85rem;
color: var(--gray-500);
}

/* ===================== */
/* COME FUNZIONA */
/* ===================== */

.how-it-works {
padding: 2rem 1rem 3rem;
}

.how-it-works h2 {
text-align: center;
font-size: 2rem;
color: var(--gray-900);
margin: 0 0 0.5rem 0;
}

.section-subtitle {
text-align: center;
color: var(--gray-500);
margin: 0 0 2.5rem 0;
}

.steps-grid {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
gap: 1.5rem;
max-width: 900px;
margin: 0 auto;
}

.step-card {
background: white;
border: 1px solid var(--gray-200);
border-radius: var(--radius);
padding: 1.5rem;
text-align: center;
position: relative;
transition: all 0.2s ease;
}

.step-card:hover {
border-color: var(--primary);
box-shadow: var(--shadow-lg);
transform: translateY(-2px);
}

.step-number {
position: absolute;
top: -12px;
left: 50%;
transform: translateX(-50%);
background: var(--primary);
color: white;
width: 24px;
height: 24px;
border-radius: 50%;
font-size: 0.75rem;
font-weight: 700;
display: flex;
align-items: center;
justify-content: center;
}

.step-icon {
font-size: 2rem;
margin: 0.5rem 0;
}

.step-card h3 {
font-size: 1rem;
color: var(--gray-900);
margin: 0.5rem 0;
}

.step-card p {
font-size: 0.85rem;
color: var(--gray-500);
line-height: 1.5;
margin: 0;
}

/* ===================== */
/* PREVIEW SECTION */
/* ===================== */

.preview-section {
padding: 3rem 1rem;
background: var(--gray-50);
border-radius: var(--radius);
margin: 2rem 0;
}

.preview-section h2 {
text-align: center;
font-size: 2rem;
color: var(--gray-900);
margin: 0 0 0.5rem 0;
}

.preview-cards {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
gap: 1.5rem;
max-width: 900px;
margin: 0 auto;
}

.preview-card {
background: white;
border-radius: var(--radius);
overflow: hidden;
box-shadow: var(--shadow-lg);
border: 1px solid var(--gray-200);
}

.preview-header {
background: var(--gray-100);
padding: 0.6rem 1rem;
display: flex;
align-items: center;
gap: 0.4rem;
border-bottom: 1px solid var(--gray-200);
}

.preview-dot {
width: 10px;
height: 10px;
border-radius: 50%;
}

.preview-dot.red { background: #ef4444; }
.preview-dot.yellow { background: #eab308; }
.preview-dot.green { background: #22c55e; }

.preview-title {
margin-left: 0.5rem;
font-size: 0.8rem;
color: var(--gray-500);
font-weight: 500;
}

.preview-body {
padding: 1rem;
display: flex;
flex-direction: column;
gap: 0.5rem;
}

.fake-input {
padding: 0.6rem 0.75rem;
background: var(--gray-50);
border: 1px solid var(--gray-200);
border-radius: 6px;
font-size: 0.85rem;
color: var(--gray-700);
}

.fake-slots {
display: flex;
flex-direction: column;
gap: 0.35rem;
}

.fake-slot {
padding: 0.5rem 0.75rem;
background: var(--primary-light);
border-radius: 6px;
font-size: 0.8rem;
color: var(--primary);
font-weight: 500;
}

.fake-button {
padding: 0.6rem;
background: var(--primary);
color: white;
border-radius: 6px;
text-align: center;
font-size: 0.85rem;
font-weight: 600;
margin-top: 0.25rem;
}

.fake-vote-row {
display: flex;
justify-content: space-between;
align-items: center;
padding: 0.6rem 0.75rem;
border: 1px solid var(--gray-200);
border-radius: 6px;
font-size: 0.85rem;
}

.vote-yes {
background: var(--green-light);
padding: 0.2rem 0.5rem;
border-radius: 4px;
font-size: 0.8rem;
}

.vote-maybe {
background: #fef9c3;
padding: 0.2rem 0.5rem;
border-radius: 4px;
font-size: 0.8rem;
}

.fake-result {
display: flex;
align-items: center;
gap: 0.5rem;
font-size: 0.8rem;
padding: 0.4rem 0;
}

.fake-result span:first-child {
min-width: 80px;
color: var(--gray-600);
}

.fake-result.best span:first-child {
color: var(--green);
font-weight: 700;
}

.fake-bar {
flex: 1;
height: 8px;
background: var(--gray-100);
border-radius: 4px;
overflow: hidden;
}

.fake-bar-fill {
height: 100%;
background: var(--primary);
border-radius: 4px;
transition: width 1s ease;
}

.fake-bar-fill.winner {
background: var(--green);
}

.fake-percent {
font-weight: 700;
color: var(--gray-700);
min-width: 35px;
text-align: right;
}

/* ===================== */
/* CTA SECTION */
/* ===================== */

.cta-section {
text-align: center;
padding: 4rem 1rem;
}

.cta-section h2 {
font-size: 1.75rem;
color: var(--gray-900);
margin: 0 0 0.5rem 0;
}

.cta-section p {
color: var(--gray-500);
margin: 0 0 2rem 0;
}

/* ===================== */
/* FOOTER */
/* ===================== */

footer {
text-align: center;
padding: 2rem 1rem;
border-top: 1px solid var(--gray-200);
color: var(--gray-400);
font-size: 0.85rem;
}

/* ===================== */
/* RESPONSIVE */
/* ===================== */

@media (max-width: 640px) {
.hero h1 {
font-size: 2rem;
}

.hero-subtitle {
font-size: 1rem;
}

.stats-bar {
gap: 1.5rem;
}

.steps-grid {
grid-template-columns: 1fr 1fr;
}

.preview-cards {
grid-template-columns: 1fr;
}
}
</style>