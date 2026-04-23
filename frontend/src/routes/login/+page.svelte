<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  // ← Replace with your actual Client ID
  const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID 
    ?? 'YOUR_CLIENT_ID.apps.googleusercontent.com';

  let message = 'Non sei ancora loggato.';

  onMount(() => {
    // If already logged in, redirect
    if (localStorage.getItem('token')) {
      goto('/');
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.onload = initGoogle;
    document.head.appendChild(script);
  });

  function initGoogle() {
    google.accounts.id.initialize({
      client_id: GOOGLE_CLIENT_ID,
      callback: handleCredentialResponse,
    });

    google.accounts.id.renderButton(
      document.getElementById('google-btn'),
      {
        theme: 'outline',
        size: 'large',
        text: 'signin_with',
        width: 300,
      }
    );
  }

  async function handleCredentialResponse(response: any) {
    message = '⏳ Verifica in corso...';

    try {
      const res = await fetch('/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: response.credential }),  // ← matches your backend
      });

      const data = await res.json();

      if (res.ok) {
        // Your backend returns { token, user }
        localStorage.setItem('token', data.token);
        message = `✅ Benvenuto, ${data.user.name}!`;
        setTimeout(() => goto('/'), 1000);
      } else {
        message = `❌ ${data.error}`;
      }
    } catch (err) {
      message = '❌ Errore di connessione al server.';
    }
  }
</script>

<h2>🔐 Login</h2>

<div class="login-box">
  <p>Accedi con il tuo account Google per continuare.</p>
  <div id="google-btn"></div>
  <p class="status">{message}</p>
</div>

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

  #google-btn {
    display: flex;
    justify-content: center;
    margin: 1.5rem 0;
  }

  .status {
    color: #666;
    font-style: italic;
    margin-top: 1rem;
  }
</style>