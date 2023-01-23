import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'




// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  proxy: {
    '/': {
      target: 'https://0aa1-2001-fb1-14a-79d7-acf2-9c79-2de0-a242.ap.ngrok.io',
      changeOrigin: true
    }
  }
})

