import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path';

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
  plugins: [vue()],
  base:"/klima/",
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  }
})
