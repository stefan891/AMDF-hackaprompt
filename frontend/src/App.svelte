<!-- src/App.svelte -->
<!-- Questo è il componente RADICE: contiene il router e la navbar -->

<script>
// Importa il componente Router dalla libreria
import Router from 'svelte-spa-router';

// Importa la mappa delle route (la creiamo al prossimo step)
import routes from './routes.js';
</script>

<!-- Layout dell'app -->
<main>
<h1>📅 Event Scheduler</h1>
<!--
Il componente Router guarda l'URL e mostra
il componente corrispondente dalla mappa routes.
Es: /#/login → mostra Login.svelte
-->
<Router {routes} />
</main>

<style>
/* Stile globale del contenitore */
main {
max-width: 800px;
margin: 0 auto; /* Centra orizzontalmente */
padding: 1rem;
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

h1 {
text-align: center;
color: #333;
}
</style>