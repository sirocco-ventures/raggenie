import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import App from './App.jsx';

describe('Main component', () => {
    it('renders without crashing', () => {
        const { getByText } = render(
            <BrowserRouter>
                <App />
                <ToastContainer />
            </BrowserRouter>
        );

        // Assuming App component has some text to verify it's rendered
        expect(getByText(/Set Up Your Bot in 3 Easy Steps/i)).toBeInTheDocument();
    });

    it('renders the ToastContainer', () => {
        const { container } = render(
            <BrowserRouter>
                <App />
                <ToastContainer />
            </BrowserRouter>
        );

        // Check if ToastContainer is rendered
        expect(container.querySelector('.Toastify')).toBeInTheDocument();
    });


});

