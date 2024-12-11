import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path';
// monitor markdown for dev mode. not needed in webbuild
import mdMonitorPlugin from './tools/mdMonitorPlugin';

import Sitemap from 'vite-plugin-sitemap'

// https://vitejs.dev/config/
export default defineConfig({
  // new sass prefers moden option
  css: {
    preprocessorOptions: {
      scss: {
        api: 'modern-compiler', // or "modern", "legacy"
      },
    },
  },
  plugins: [
    vue(),
    Sitemap({
      hostname: 'https://dashboard.daten.city',
      readable: true,
      //dynamicRoutes,
    }),
    mdMonitorPlugin(), // Register the custom plugin
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    },
    optimizeDeps: {
      include: ['axe-core']
    }
  }
})
