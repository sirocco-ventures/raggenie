import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import 'react-toastify/dist/ReactToastify.css';
import { BrowserRouter } from 'react-router-dom'
import { ToastContainer } from 'react-toastify';
import "./global.css"

ReactDOM.createRoot(document.getElementById('root')).render(
  // <React.StrictMode>
    <BrowserRouter>
        <App />
        <ToastContainer/>
    </BrowserRouter>
  // </React.StrictMode>,
)
