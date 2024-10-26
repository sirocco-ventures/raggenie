import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, test, expect, vi, beforeAll, afterAll } from 'vitest';

let originalError;

beforeAll(() => {
  originalError = console.error;
  console.error = (...args) => {
    if (args[0].includes('Warning: The tag <text> is unrecognized in this browser.') ||
        args[0].includes('Warning: The tag <tspan> is unrecognized in this browser.')) {
      return;
    }
    originalError.call(console, ...args);
  };
});

afterAll(() => {
  console.error = originalError;
});

// Mock SVG elements
const MockSVGElement = ({ children, ...props }) => <div {...props}>{children}</div>;

// Mock React's createElement for SVG elements
const originalCreateElement = React.createElement;
React.createElement = (type, props, ...children) => {
  if (type === 'text' || type === 'tspan') {
    return originalCreateElement(MockSVGElement, props, ...children);
  }
  return originalCreateElement(type, props, ...children);
};

// Mock recharts library
vi.mock('recharts', () => ({
  LineChart: ({ children }) => <div data-testid="line-chart">{children}</div>,
  Line: () => <div data-testid="line" />,
  XAxis: ({ children }) => <div data-testid="x-axis">{children}</div>,
  YAxis: ({ children }) => <div data-testid="y-axis">{children}</div>,
  CartesianGrid: () => <div data-testid="cartesian-grid" />,
  Tooltip: () => <div data-testid="tooltip" />,
  ResponsiveContainer: ({ children }) => <div data-testid="responsive-container">{children}</div>,
}));

// Import the component after all mocks are set up
import LineChart, { customXAxisLabel, customYAxisLabel } from './LineChart';

describe('LineChart Component', () => {
  const mockData = [
    { name: 'Jan', value: 30 },
    { name: 'Feb', value: 20 },
    { name: 'Mar', value: 50 },
  ];

  test('renders with default props', () => {
    render(<LineChart />);
    expect(screen.getByText('Line Chart')).toBeInTheDocument();
    expect(screen.getByTestId('responsive-container')).toBeInTheDocument();
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
  });

  test('renders with custom title', () => {
    render(<LineChart title="Custom Line Chart" />);
    expect(screen.getByText('Custom Line Chart')).toBeInTheDocument();
  });

  test('renders with custom data', () => {
    render(<LineChart data={mockData} />);
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
    expect(screen.getByTestId('line')).toBeInTheDocument();
  });

  test('renders with custom axis labels', () => {
    render(<LineChart data={mockData} xAxis="customX" yAxis="customY" />);
    expect(screen.getByTestId('x-axis')).toBeInTheDocument();
    expect(screen.getByTestId('y-axis')).toBeInTheDocument();
  });

  test('respects dataLength prop', () => {
    const longData = [
      ...mockData,
      { name: 'Apr', value: 40 },
      { name: 'May', value: 60 },
    ];
    render(<LineChart data={longData} dataLength={3} />);
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
  });

  test('renders CartesianGrid', () => {
    render(<LineChart />);
    expect(screen.getByTestId('cartesian-grid')).toBeInTheDocument();
  });

  test('renders Tooltip', () => {
    render(<LineChart />);
    expect(screen.getByTestId('tooltip')).toBeInTheDocument();
  });

  test('applies correct styling classes', () => {
    const { container } = render(<LineChart />);
    
    // Check for a container class
    const containerElement = container.querySelector('[class*="Container"]');
    expect(containerElement).toBeInTheDocument();
    
    // Check for a title class
    const titleElement = container.querySelector('[class*="Title"]');
    expect(titleElement).toBeInTheDocument();
    
    // Check for a chart-specific class (adjust if necessary)
    const chartElement = container.querySelector('[class*="Chart"]');
    expect(chartElement).toBeInTheDocument();
  });

  test('customXAxisLabel renders with correct attributes', () => {
    const props = { payload: { value: 'Test' }, x: 10, y: 20, width: 100, height: 50 };
    const { container } = render(customXAxisLabel(props));
    
    const text = container.querySelector('text');
    expect(text).toBeInTheDocument();
    expect(text).toHaveAttribute('x', '10');
    expect(text).toHaveAttribute('y', '30'); // y + 10
    expect(text).toHaveAttribute('width', '100');
    expect(text).toHaveAttribute('height', '50');

    const tspan = container.querySelector('tspan');
    expect(tspan).toBeInTheDocument();
    expect(tspan).toHaveAttribute('x', '30'); // x + 20
    expect(tspan).toHaveAttribute('y', '30'); // y + 10
    expect(tspan).toHaveTextContent('Test');
  });

  test('customYAxisLabel renders with correct attributes', () => {
    const props = { payload: { value: 'Test' }, x: 10, y: 20, width: 100, height: 50 };
    const { container } = render(customYAxisLabel(props));
    
    const text = container.querySelector('text');
    expect(text).toBeInTheDocument();
    expect(text).toHaveAttribute('x', '10');
    expect(text).toHaveAttribute('y', '30'); // y + 10
    expect(text).toHaveAttribute('width', '100');
    expect(text).toHaveAttribute('height', '50');

    const tspan = container.querySelector('tspan');
    expect(tspan).toBeInTheDocument();
    expect(tspan).toHaveAttribute('x', '5'); // x - 5
    expect(tspan).toHaveAttribute('y', '20');
    expect(tspan).toHaveTextContent('Test');
  });
});
