---
sidebar_position: 2
---

# To run raggenie ui server

### Go to the project ui directory
The raggenie UI is located in a subdirectory of the project. You must navigate to this directory to install the necessary dependencies and run the UI server.
```bash
cd raggenie/ui
```

### Install dependencies
Once in the UI directory, the next step is to install the dependencies needed to run the UI. The dependencies include packages required by the frontend application to function correctly, including UI components, routing, and state management.
```bash
npm install
```
Raggenie uses Node.js for frontend, for more details visit [Prerequesites](../Prerequesites.md)

### Start the server
After installing the dependencies, you can start the development server, which will launch the raggenie UI in your browser.
```bash
npm run dev
```