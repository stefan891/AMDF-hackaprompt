import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    proxy: {
      "/auth":        "http://localhost:5000",
      "/events":      "http://localhost:5000",
      "/users":       "http://localhost:5000",
      "/calendar":    "http://localhost:5000",
      "/invitations": "http://localhost:5000",
    },
  },
});