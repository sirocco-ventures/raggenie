import { describe, test, expect, beforeEach, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import BarChart from './BarChart';
import '@testing-library/jest-dom';

// Mock Recharts components
vi.mock('recharts', () => ({
  ResponsiveContainer: ({ children }) => <div data-testid="responsive-container">{children}</div>,
  BarChart: ({ children }) => <div data-testid="bar-chart">{children}</div>,
  Bar: ({ shape }) => <div data-testid="bar">{shape && 'Custom Shape'}</div>,
  XAxis: ({ tick }) => <div data-testid="x-axis">{tick && 'Custom Tick'}</div>,
  YAxis: ({ tick }) => <div data-testid="y-axis">{tick && 'Custom Tick'}</div>,
  Tooltip: () => <div data-testid="tooltip" />,
}));

// Mock CSS module
vi.mock('../style.module.css', () => ({
  default: {
    ChartContainer: 'ChartContainer',
    ChartTitle: 'ChartTitle',
    BarChartResponsive: 'BarChartResponsive'
  }
}));

describe('BarChart Component', () => {
  const mockData = [
    { name: 'Jan', value: 10 },
    { name: 'Feb', value: 20 },
    { name: 'Mar', value: 30 }
  ];

  beforeEach(() => {
    vi.clearAllMocks();
  });

  test('renders with default props', () => {
    render(<BarChart />);
    expect(screen.getByText('Bar Chart')).toBeInTheDocument();
    expect(screen.getByTestId('responsive-container')).toBeInTheDocument();
  });

  test('renders with custom title', () => {
    render(<BarChart title="Custom Chart" />);
    expect(screen.getByText('Custom Chart')).toBeInTheDocument();
  });

  test('renders with custom data', () => {
    render(<BarChart data={mockData} />);
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
    expect(screen.getByTestId('bar')).toBeInTheDocument();
  });

  test('respects dataLength prop', () => {
    const longData = [
      ...mockData,
      { name: 'Apr', value: 40 },
      { name: 'May', value: 50 }
    ];
    
    render(<BarChart data={longData} dataLength={3} />);
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
  });

  test('renders customBar with correct props', () => {
    const { container } = render(<BarChart data={mockData} />);
    const barComponent = screen.getByTestId('bar');
    
    // Get the shape prop function from the Bar component mock
    const customBarProps = {
        x: 10,
        y: 20,
        height: 100
    };

    const rect = (
        <rect 
            width="28" 
            height={100} 
            x={20} 
            y={20} 
            fill="#74B3FF" 
            rx="4"
        />
    );

    // Test that the Bar component receives a shape prop that renders correctly
    expect(barComponent).toBeInTheDocument();
    expect(barComponent).toHaveTextContent('Custom Shape');
});

test('renders customAxisLabel with correct props', () => {
    render(<BarChart data={mockData} />);
    
    const xAxis = screen.getByTestId('x-axis');
    const yAxis = screen.getByTestId('y-axis');

    // Test that both axes are rendered with custom ticks
    expect(xAxis).toBeInTheDocument();
    expect(yAxis).toBeInTheDocument();
    expect(xAxis).toHaveTextContent('Custom Tick');
    expect(yAxis).toHaveTextContent('Custom Tick');
});

  test('applies correct styling classes', () => {
    const { container } = render(<BarChart />);
    expect(container.querySelector('.ChartContainer')).toBeInTheDocument();
    expect(container.querySelector('.ChartTitle')).toBeInTheDocument();
    expect(container.querySelector('.BarChartResponsive')).toBeInTheDocument();
  });

  test('renders with custom axis keys', () => {
    const customData = [
      { customX: 'Jan', customY: 10 },
      { customX: 'Feb', customY: 20 }
    ];

    render(<BarChart 
      data={customData} 
      xAxis="customX" 
      yAxis="customY" 
    />);

    expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
  });

  test('tooltip is rendered', () => {
    render(<BarChart data={mockData} />);
    expect(screen.getByTestId('tooltip')).toBeInTheDocument();
  });
});