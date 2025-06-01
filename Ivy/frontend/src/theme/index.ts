import { createTheme, alpha } from '@mui/material/styles';

const theme = (mode: 'light' | 'dark') => {
  const isDark = mode === 'dark';

  return createTheme({
    palette: {
      mode,
      primary: {
        main: '#4CAF50',
        light: '#81C784',
        dark: '#388E3C',
      },
      secondary: {
        main: '#66BB6A',
        light: '#A5D6A7',
        dark: '#43A047',
      },
      background: {
        default: isDark ? '#121212' : '#ffffff',
        paper: isDark ? '#1E1E1E' : '#ffffff',
      },
      text: {
        primary: isDark ? '#ffffff' : '#000000',
        secondary: isDark ? alpha('#ffffff', 0.7) : alpha('#000000', 0.7),
      },
    },
    shape: {
      borderRadius: 12,
    },
    typography: {
      fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
      h1: {
        fontWeight: 800,
      },
      h2: {
        fontWeight: 700,
      },
      h3: {
        fontWeight: 700,
      },
      h4: {
        fontWeight: 600,
      },
      h5: {
        fontWeight: 600,
      },
      h6: {
        fontWeight: 600,
      },
    },
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            textTransform: 'none',
            fontWeight: 600,
          },
        },
      },
      MuiCard: {
        styleOverrides: {
          root: {
            backgroundImage: 'none',
            backgroundColor: isDark ? '#1E1E1E' : '#ffffff',
            boxShadow: isDark
              ? '0 0 0 1px rgba(255, 255, 255, 0.12)'
              : '0 1px 3px rgba(0, 0, 0, 0.12)',
          },
        },
      },
      MuiTableCell: {
        styleOverrides: {
          root: {
            borderBottom: `1px solid ${
              isDark ? 'rgba(255, 255, 255, 0.12)' : 'rgba(0, 0, 0, 0.12)'
            }`,
          },
        },
      },
    },
  });
};

export default theme; 