import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path';
// monitor markdown for dev mode. not needed in webbuild
import mdMonitorPlugin from './tools/mdMonitorPlugin';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    mdMonitorPlugin(), // Register the custom plugin
    ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  }
})
