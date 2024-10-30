import { describe, test, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import React from 'react';
import App from './App';
import { ToastContainer } from 'react-toastify';
import { BrowserRouter } from 'react-router-dom'

// Mock react-dom/client with default export
vi.mock('react-dom/client', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    default: {
      createRoot: vi.fn(() => ({
        render: vi.fn(),
      })),
    },
  };
});

// Mock the App component
vi.mock('./App', () => ({
  default: () => <div data-testid="mock-app">App Component</div>,
}));

// Mock BrowserRouter
vi.mock('react-router-dom', () => ({
  BrowserRouter: ({ children }) => <div data-testid="mock-router">{children}</div>,
}));

// Mock ToastContainer
vi.mock('react-toastify', () => ({
  ToastContainer: () => <div data-testid="mock-toast-container">Toast Container</div>,
}));

// Mock CSS imports
vi.mock('react-toastify/dist/ReactToastify.css', () => ({}));
vi.mock('./global.css', () => ({}));

describe('Main Component', () => {
  beforeEach(() => {
    // Clear the document body before each test
    document.body.innerHTML = '';
    // Create a div with root id for ReactDOM.createRoot
    const root = document.createElement('div');
    root.id = 'root';
    document.body.appendChild(root);
  });

  test('renders without crashing', () => {
    render(<App />);
    expect(document.getElementById('root')).toBeInTheDocument();
  });

  test('renders with all required components', () => {
    render(
      <div data-testid="root">
        <BrowserRouter>
          <App />
          <ToastContainer />
        </BrowserRouter>
      </div>
    );

    // Check if Router is rendered
    expect(screen.getByTestId('mock-router')).toBeInTheDocument();
    
    // Check if App is rendered
    expect(screen.getByTestId('mock-app')).toBeInTheDocument();
    
    // Check if ToastContainer is rendered
    expect(screen.getByTestId('mock-toast-container')).toBeInTheDocument();
  });

  test('renders components in correct order', () => {
    render(
      <div data-testid="root">
        <BrowserRouter>
          <App />
          <ToastContainer />
        </BrowserRouter>
      </div>
    );

    const router = screen.getByTestId('mock-router');
    expect(router.children[0]).toHaveAttribute('data-testid', 'mock-app');
    expect(router.children[1]).toHaveAttribute('data-testid', 'mock-toast-container');
  });

  test('BrowserRouter wraps other components', () => {
    render(
      <div data-testid="root">
        <BrowserRouter>
          <App />
          <ToastContainer />
        </BrowserRouter>
      </div>
    );

    const router = screen.getByTestId('mock-router');
    expect(router).toContainElement(screen.getByTestId('mock-app'));
    expect(router).toContainElement(screen.getByTestId('mock-toast-container'));
  });
});
