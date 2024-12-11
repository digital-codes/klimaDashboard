import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  test: {
    setupFiles: ['./test/setup.js'], // Run setup before tests
    environment: 'jsdom', // Enable jsdom for document, window, etc.
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src') // Same as Vite config
    }
  }  
});
