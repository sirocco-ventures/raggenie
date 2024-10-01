import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

export default defineConfig({
  base: "/",
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
 });