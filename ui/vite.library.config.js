import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import path from 'path';
import ViteCssInjectedByJs from 'vite-plugin-css-injected-by-js';

export default defineConfig({
  base: "/",
  plugins: [react(),ViteCssInjectedByJs()],
  define: {
    'process.env': {}, // Provide a mock for process.env in browser
  },
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
  build: {
      outDir: 'dist-library',  
      lib: {
        entry: path.resolve(__dirname, './src/embedbot/index.jsx'), // Entry point for the library
        name: 'ChatBot', // Global variable name for UMD
        fileName: (format) => `chatbot.js`, // Output filename
        formats: ['umd'], // Output format
      },
      rollupOptions: {
        output: {
          assetFileNames: ({ name }) => {
            if (/\.(png|jpg|jpeg|gif|svg)$/.test(name ?? '')) {
              return 'assets/images/[name][extname]'; // Handle images
            }
            return 'assets/[name][extname]';
          },
        },
      },
    }
});
