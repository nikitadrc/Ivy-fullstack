import React from 'react';
import { Box, Button, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        p: 3,
      }}
    >
      <Typography
        variant="h1"
        sx={{
          fontSize: { xs: '6rem', sm: '8rem' },
          fontWeight: 700,
          color: 'primary.main',
          mb: 2,
        }}
      >
        404
      </Typography>
      <Typography
        variant="h4"
        sx={{
          mb: 2,
          fontWeight: 500,
        }}
      >
        Page Not Found
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4, maxWidth: 480 }}>
        Sorry, we couldn&apos;t find the page you&apos;re looking for. Perhaps you&apos;ve mistyped
        the URL or the page has been moved.
      </Typography>
      <Button
        variant="contained"
        size="large"
        onClick={() => navigate('/dashboard')}
        sx={{ borderRadius: 2 }}
      >
        Go to Dashboard
      </Button>
    </Box>
  );
}
