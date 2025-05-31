import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AnimatePresence } from 'framer-motion';
import { useThemeMode } from '@/hooks/useThemeMode';
import { AuthProvider } from '@/hooks/useAuth';
import theme from '@/theme';

// Pages
import Landing from '@/pages/Landing';
import Login from '@/pages/Login';
import Register from '@/pages/Register';
import Dashboard from '@/pages/Dashboard';
import Calendar from '@/pages/Calendar';
import Analytics from '@/pages/Analytics';
import Candidates from '@/pages/Candidates';
import Settings from '@/pages/Settings';

// Components
import Layout from '@/components/Layout';
import HelpGuide from '@/components/HelpGuide';
import PageTransition from '@/components/PageTransition';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route
          path="/"
          element={
            <PageTransition>
              <Landing />
            </PageTransition>
          }
        />
        <Route
          path="/login"
          element={
            <PageTransition>
              <Login />
            </PageTransition>
          }
        />
        <Route
          path="/register"
          element={
            <PageTransition>
              <Register />
            </PageTransition>
          }
        />
        <Route element={<Layout />}>
          <Route
            path="/dashboard"
            element={
              <PageTransition>
                <Dashboard />
              </PageTransition>
            }
          />
          <Route
            path="/calendar"
            element={
              <PageTransition>
                <Calendar />
              </PageTransition>
            }
          />
          <Route
            path="/analytics"
            element={
              <PageTransition>
                <Analytics />
              </PageTransition>
            }
          />
          <Route
            path="/candidates"
            element={
              <PageTransition>
                <Candidates />
              </PageTransition>
            }
          />
          <Route
            path="/settings"
            element={
              <PageTransition>
                <Settings />
              </PageTransition>
            }
          />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AnimatePresence>
  );
}

function App() {
  const { mode } = useThemeMode();

  return (
    <ThemeProvider theme={theme(mode)}>
      <CssBaseline />
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <AuthProvider>
            <AnimatedRoutes />
            <HelpGuide />
          </AuthProvider>
        </BrowserRouter>
      </QueryClientProvider>
    </ThemeProvider>
  );
}

export default App;
