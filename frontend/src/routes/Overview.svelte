<!-- src/routes/Overview.svelte
<script>
export let params = {};
</script>

<h2>Riepilogo Evento</h2>
<p>ID Evento: <strong>{params.id}</strong></p>
<a href="#/">← Torna alla home</a> -->

<script lang="ts">
  import { page } from '$app/stores';
</script>

<h2>Riepilogo Evento</h2>
<p>ID Evento: <strong>{$page.params.id}</strong></p>
<a href="/">← Torna alla home</a>