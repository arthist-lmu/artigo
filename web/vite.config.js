import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import vueDevTools from 'vite-plugin-vue-devtools'
import pluginChecker from 'vite-plugin-checker'

export default defineConfig({
  server: {
    port: 80,
    hmr: true,
    watch: {
      usePolling: true
    }
  },
  build: {
    sourcemap: true
  },
  plugins: [
    vue(),
    vuetify({
      styles: {
        configFile: 'src/styles/settings.scss'
      }
    }),
    vueDevTools(),
    pluginChecker({
      eslint: {
        lintCommand: 'eslint ./src/**/*.{vue,js}'
      },
      stylelint: {
        lintCommand: 'stylelint ./src/**/*.{vue,css,scss}'
      }
    }),
    {
      name: 'full-reload',
      handleHotUpdate({ server }) {
        server.ws.send({ type: 'full-reload' });
        return [];
      }
    }
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
