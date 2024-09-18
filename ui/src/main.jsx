import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import "./global.css"
import 'react-toastify/dist/ReactToastify.css';
import { BrowserRouter } from 'react-router-dom'
import { ToastContainer } from 'react-toastify';

ReactDOM.createRoot(document.getElementById('root')).render(
  // <React.StrictMode>
    <BrowserRouter>
        <App />
        <ToastContainer/>
    </BrowserRouter>
  // </React.StrictMode>,
)
