// Smart Condominium - Punto de entrada de la aplicación
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { es } from 'date-fns/locale';

import App from './App';
import theme from './theme';
import { AuthProvider } from './contexts/AuthContext';
import './index.css';

// Configurar React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutos
    },
  },
});

// Configurar Toaster
const toasterOptions = {
  duration: 4000,
  position: 'top-right',
  style: {
    background: '#333',
    color: '#fff',
    borderRadius: '8px',
    fontSize: '14px',
  },
  success: {
    iconTheme: {
      primary: '#2E7D32',
      secondary: '#fff',
    },
  },
  error: {
    iconTheme: {
      primary: '#C62828',
      secondary: '#fff',
    },
  },
};

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={theme}>
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={es}>
            <CssBaseline />
            <AuthProvider>
              <App />
              <Toaster toastOptions={toasterOptions} />
            </AuthProvider>
          </LocalizationProvider>
        </ThemeProvider>
      </QueryClientProvider>
    </BrowserRouter>
  </React.StrictMode>
);