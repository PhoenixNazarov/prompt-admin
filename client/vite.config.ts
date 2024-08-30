import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://0.0.0.0:8080',
        secure: false
      },
      '/api/ws': {
        target: 'ws://0.0.0.0:8080',
        ws: true,
      }
    }
  }
})
