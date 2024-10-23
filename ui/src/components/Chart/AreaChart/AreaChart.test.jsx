import React from 'react';
import { render } from '@testing-library/react';
import AreaChart from './AreaChart';
import '@testing-library/jest-dom';

describe('AreaChart Component', () => {
    const mockData = [
        { name: 'Jan', value: 30 },
        { name: 'Feb', value: 20 },
        { name: 'Mar', value: 50 },
    ];

    test('renders without crashing', () => {
        const { getByText } = render(<AreaChart data={mockData} />);
        expect(getByText('Area Chart')).toBeInTheDocument();
    });

    test('renders with custom title', () => {
        const customTitle = 'Custom Area Chart';
        const { getByText } = render(<AreaChart title={customTitle} data={mockData} />);
        expect(getByText(customTitle)).toBeInTheDocument();
    });

    test('renders correct number of data points', () => {
        const { container } = render(<AreaChart data={mockData} dataLength={2} />);

        const areas = container.querySelectorAll('.recharts-surface');
        expect(areas.length).toBe(1); // Only one recharts surface

        const xAxisTicks = container.querySelectorAll('.recharts-cartesian-grid-horizontal line');
        expect(xAxisTicks.length).toBe(2); // Only two horizontal grid lines should be rendered
    });

    test('renders with default props', () => {
        const { container } = render(<AreaChart data={mockData} />);
        const chartWrapper = container.querySelector('.recharts-wrapper');
        expect(chartWrapper).not.toBeNull();
        expect(chartWrapper).toBeInTheDocument();
    });
});