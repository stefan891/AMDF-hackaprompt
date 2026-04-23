<!-- src/routes/+layout.svelte -->
<nav>
  <a href="/">🏠 Home</a>
  <a href="/login">🔐 Login</a>
  <a href="/create">➕ Crea Evento</a>
  <a href="/event/abc123">📋 Evento Demo</a>
  <a href="/overview/abc123">📊 Overview Demo</a>
</nav>

<hr />

<!-- Qui dentro viene iniettato il contenuto della pagina corrente -->
<slot />

<style>
  nav {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 8px;
    flex-wrap: wrap;
  }

  nav a {
    text-decoration: none;
    color: #1976d2;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    transition: background 0.2s;
  }

  nav a:hover {
    background: #e3f2fd;
  }

  hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 1rem 0;
  }
</style>