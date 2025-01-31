import React from 'react';
import { createRoot } from 'react-dom/client';
import ChatBot from './ChatBot';
import './ChatBot.css';

// Function to mount the chatbox to a specific element
const mountChatbox = (elementId, props = {}) => {
  const container = document.getElementById(elementId);
  if (container) {
    const root = createRoot(container);
    root.render(<ChatBot {...props}/>);
  }
};

// Export mountChatbox so it can be used externally
export { mountChatbox };
