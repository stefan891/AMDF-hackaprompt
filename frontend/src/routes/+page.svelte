<!-- src/routes/+page.svelte -->
<h1>📅 Event Scheduler</h1>
<p>Benvenuto! Questa è la home page.</p>

<div class="card">
  <h3>Come funziona:</h3>
  <ol>
    <li>Fai il <a href="/login">Login</a> con Google</li>
    <li><a href="/create">Crea un evento</a> con degli slot temporali</li>
    <li>Condividi il link con i partecipanti</li>
    <li>Tutti esprimono le loro preferenze</li>
    <li>Vedi il <a href="/overview/abc123">riepilogo</a> e scegli lo slot migliore</li>
  </ol>
</div>

<style>
  h1 {
    text-align: center;
    margin-bottom: 0.5rem;
  }

  p {
    text-align: center;
    color: #666;
  }

  .card {
    background: #fafafa;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    margin-top: 2rem;
  }

  ol {
    line-height: 2;
  }

  a {
    color: #1976d2;
  }
</style>