import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    cors: false,
    port: 2303,
    proxy: {
      '/api': {
          target: 'https://api-adaptive.firdausmaulana.com',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
      }
  }
  },
})
