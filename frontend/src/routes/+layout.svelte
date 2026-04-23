
<!-- src/routes/+layout.svelte -->
<nav>
<a href="/" class="logo">📅 Event Scheduler</a>

<div class="nav-links">
<a href="/login">Accedi</a>
<a href="/create" class="nav-btn">Crea Evento</a>
</div>
</nav>

<slot />

<style>
:global(*) {
margin: 0;
padding: 0;
box-sizing: border-box;
}

:global(body) {
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', sans-serif;
color: #374151;
background: white;
-webkit-font-smoothing: antialiased;
}

nav {
display: flex;
justify-content: space-between;
align-items: center;
padding: 1rem 2rem;
border-bottom: 1px solid #e5e7eb;
background: white;
position: sticky;
top: 0;
z-index: 100;
max-width: 1000px;
margin: 0 auto;
}

.logo {
font-size: 1.2rem;
font-weight: 700;
text-decoration: none;
color: #111827;
}

.nav-links {
display: flex;
align-items: center;
gap: 1.5rem;
}

.nav-links a {
text-decoration: none;
color: #6b7280;
font-size: 0.95rem;
font-weight: 500;
transition: color 0.2s;
}

.nav-links a:hover {
color: #111827;
}

.nav-btn {
background: #2563eb;
color: white;
padding: 0.5rem 1.25rem;
border-radius: 8px;
}

.nav-btn:hover {
background: #1d4ed8;
}
</style>