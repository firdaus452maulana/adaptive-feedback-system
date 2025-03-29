import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    allowedHosts: true,
    cors: false,
    port: 4303,
    proxy: {
      '/api': {
          target: 'https://api-adaptive.firdausmaulana.com',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
      }
  }
  },
})
