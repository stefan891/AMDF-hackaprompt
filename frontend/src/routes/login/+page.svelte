<!-- src/routes/login/+page.svelte -->
<h2>🔐 Login</h2>

<div class="login-box">
  <p>Accedi con il tuo account Google per continuare.</p>

  <button on:click={handleLogin}>
    🔵 Accedi con Google
  </button>

  <p class="status">{message}</p>
</div>

<script lang="ts">
  let message = 'Non sei ancora loggato.';

  function handleLogin() {
    // Per ora è solo una demo — simula il login
    message = '✅ Login simulato! (In futuro qui ci sarà Google Sign-In)';
  }
</script>

<style>
  .login-box {
    max-width: 400px;
    margin: 2rem auto;
    text-align: center;
    padding: 2rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: #fafafa;
  }

  button {
    padding: 0.75rem 2rem;
    font-size: 1rem;
    background: #1976d2;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    margin: 1rem 0;
  }

  button:hover {
    background: #1565c0;
  }

  .status {
    color: #666;
    font-style: italic;
    margin-top: 1rem;
  }
</style>