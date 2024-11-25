import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

export default defineConfig({
  base: "/ui/",
  plugins: [react()],
  resolve: {
        alias: {
          src: "/src",
        },
      },
  server: {
      port: 5000,
      strictPort: true,
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
  },
});
