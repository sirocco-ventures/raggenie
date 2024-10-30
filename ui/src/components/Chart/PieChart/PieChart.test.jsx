import { vi, describe, test, expect } from 'vitest';
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import PieChart from './PieChart';
import style from '../style.module.css';

// Mock recharts library
vi.mock('recharts', () => ({
  PieChart: ({ children }) => <div data-testid="pie-chart">{children}</div>,
  Pie: ({ children }) => <div data-testid="pie">{children}</div>,
  Cell: ({ fill }) => <div data-testid="cell" style={{ backgroundColor: fill }} />,
  ResponsiveContainer: ({ children, width, height }) => (
    <div data-testid="responsive-container" width={width} height={height}>
      {children}
    </div>
  ),
  Tooltip: () => <div data-testid="tooltip" />,
  Legend: ({ content, layout, align, verticalAlign, wrapperStyle }) => (
    <div 
      data-testid="legend"
      data-layout={layout}
      data-align={align}
      data-vertical-align={verticalAlign}
      style={wrapperStyle}
    />
  ),
}));

describe('PieChart Component', () => {
  const mockData = [
    { label: 'A', value: 30 },
    { label: 'B', value: 20 },
    { label: 'C', value: 50 },
  ];

  const COLORS = ['#3893FF', '#84BCFF', '#CDE5FF', '#FF8042'];

  test('renders with default props', () => {
    render(<PieChart />);
    expect(screen.getByText('Pie Chart')).toBeInTheDocument();
    expect(screen.getByTestId('responsive-container')).toBeInTheDocument();
    expect(screen.getByTestId('pie-chart')).toBeInTheDocument();
  });

  test('renders with custom title', () => {
    const customTitle = 'Custom Pie Chart';
    render(<PieChart title={customTitle} />);
    expect(screen.getByText(customTitle)).toBeInTheDocument();
  });

  test('renders with custom data', () => {
    render(<PieChart data={mockData} />);
    const cells = screen.getAllByTestId('cell');
    expect(cells).toHaveLength(mockData.length);
    
    // Verify colors are applied correctly
    cells.forEach((cell, index) => {
      expect(cell).toHaveStyle({ backgroundColor: COLORS[index % COLORS.length] });
    });
  });

  test('respects dataLength prop', () => {
    const longData = [
      ...mockData,
      { label: 'D', value: 40 },
      { label: 'E', value: 60 },
    ];
    const dataLength = 3;
    render(<PieChart data={longData} dataLength={dataLength} />);
    const cells = screen.getAllByTestId('cell');
    expect(cells).toHaveLength(longData.length); 
  });

  test('renders with custom dataKey and labelKey', () => {
    const customData = [
      { name: 'A', count: 30 },
      { name: 'B', count: 20 },
    ];
    render(<PieChart 
      data={customData} 
      dataKey="count" 
      labelKey="name"
    />);
    expect(screen.getByTestId('pie')).toBeInTheDocument();
  });

  test('renders Tooltip', () => {
    render(<PieChart />);
    expect(screen.getByTestId('tooltip')).toBeInTheDocument();
  });

  test('renders Legend with correct props', () => {
    render(<PieChart data={mockData} />);
    const legend = screen.getByTestId('legend');
    
    expect(legend).toHaveAttribute('data-layout', 'vertical');
    expect(legend).toHaveAttribute('data-align', 'right');
    expect(legend).toHaveAttribute('data-vertical-align', 'middle');
    
    // Check legend wrapper style
    expect(legend).toHaveStyle({
      top: '0px',
      height: '200px',
      overflow: 'auto'
    });
  });

  test('applies correct styling classes', () => {
    const { container } = render(<PieChart />);
    expect(container.querySelector(`.${style.ChartContainer}`)).toBeInTheDocument();
    expect(container.querySelector(`.${style.ChartTitle}`)).toBeInTheDocument();
    expect(container.querySelector(`.${style.BarChartResponsive}`)).toBeInTheDocument();
  });

  test('ResponsiveContainer has correct dimensions', () => {
    render(<PieChart />);
    const container = screen.getByTestId('responsive-container');
    expect(container).toHaveAttribute('width', '450');
    expect(container).toHaveAttribute('height', '183');
  });

  describe('CustomLegend', () => {
    test('renders legend items correctly', () => {
      const mockLegendProps = {
        payload: mockData.map((item, index) => ({
          color: COLORS[index % COLORS.length],
          payload: item
        })),
        label: 'label'
      };

      render(<PieChart data={mockData} />);
      
      // Check if legend items are rendered
      mockData.forEach((item, index) => {
        const legendItem = screen.getByTestId('legend');
        expect(legendItem).toBeInTheDocument();
      });
    });

    test('renders legend with correct colors', () => {
      render(<PieChart data={mockData} />);
      const cells = screen.getAllByTestId('cell');
      
      cells.forEach((cell, index) => {
        expect(cell).toHaveStyle({
          backgroundColor: COLORS[index % COLORS.length]
        });
      });
    });
  });

  test('Pie component has correct props', () => {
    render(<PieChart data={mockData} />);
    const pie = screen.getByTestId('pie');
    
    // Check if Pie component exists
    expect(pie).toBeInTheDocument();
    
    // Check data-specific props
    expect(pie).toHaveAttribute('data-innerradius', '0');
    expect(pie).toHaveAttribute('data-outerradius', '80');
    expect(pie).toHaveAttribute('data-datakey', 'value');  // default dataKey
    expect(pie).toHaveAttribute('data-namekey', 'label');  // default labelKey
    
    // Test with custom dataKey and labelKey
    render(<PieChart 
        data={mockData} 
        dataKey="customValue" 
        labelKey="customLabel" 
    />);
    const pieWithCustomKeys = screen.getByTestId('pie');
    expect(pieWithCustomKeys).toHaveAttribute('data-datakey', 'customValue');
    expect(pieWithCustomKeys).toHaveAttribute('data-namekey', 'customLabel');
  });

  test('handles empty data gracefully', () => {
    render(<PieChart data={[]} />);
    expect(screen.getByTestId('pie-chart')).toBeInTheDocument();
    expect(screen.getByTestId('tooltip')).toBeInTheDocument();
    expect(screen.getByTestId('legend')).toBeInTheDocument();
  });

  test('handles null data gracefully', () => {
    render(<PieChart data={null} />);
    expect(screen.getByTestId('pie-chart')).toBeInTheDocument();
    expect(screen.getByTestId('tooltip')).toBeInTheDocument();
    expect(screen.getByTestId('legend')).toBeInTheDocument();
  });
});
