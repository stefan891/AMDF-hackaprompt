// src/routes.js
// Mappa URL → Componente Svelte
// Il router usa gli HASH (#) per navigare senza ricaricare la pagina.

import Index from './routes/Index.svelte';
import Login from './routes/Login.svelte';
import CreateEvent from './routes/CreateEvent.svelte';
import EventView from './routes/EventView.svelte';
import Overview from './routes/Overview.svelte';

const routes = {
// URL → Componente da mostrare

'/': Index, // Pagina iniziale (redirect)
'/login': Login, // Pagina di login
'/create': CreateEvent, // Creazione evento
'/event/:id': EventView, // Dettaglio evento (:id è un parametro dinamico)
'/overview/:id': Overview // Riepilogo evento
};

// Esempio di navigazione:
// http://localhost:5173/#/login → mostra Login.svelte
// http://localhost:5173/#/event/abc → mostra EventView.svelte con params.id = "abc"

export default routes;