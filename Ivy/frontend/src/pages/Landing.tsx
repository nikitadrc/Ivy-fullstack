import React from 'react';
import { Box, Button, Container, Typography, keyframes } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const leafSway = keyframes`
  0% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(5deg);
  }
  100% {
    transform: rotate(0deg);
  }
`;

export default function Landing() {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        bgcolor: 'background.default',
        color: 'text.primary',
        overflow: 'hidden',
      }}
    >
      <Container maxWidth="md">
        <Box
          sx={{
            textAlign: 'center',
            animation: `${fadeIn} 1s ease-out`,
          }}
        >
          <Box
            component={motion.div}
            animate={{
              rotate: [0, 5, 0],
              transition: {
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut"
              }
            }}
            sx={{
              display: 'inline-block',
              mb: 4,
            }}
          >
            <svg
              width="80"
              height="80"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8 0-4.41 3.59-8 8-8s8 3.59 8 8c0 4.41-3.59 8-8 8z"
                fill="#4CAF50"
              />
              <path
                d="M12 6c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm0 10c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z"
                fill="#4CAF50"
              />
            </svg>
          </Box>

          <Typography
            variant="h1"
            component={motion.h1}
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.8 }}
            sx={{
              fontWeight: 800,
              fontSize: { xs: '3rem', md: '4.5rem' },
              background: 'linear-gradient(45deg, #4CAF50 30%, #81C784 90%)',
              backgroundClip: 'text',
              textFillColor: 'transparent',
              mb: 2,
            }}
          >
            Ivy
          </Typography>

          <Typography
            variant="h4"
            component={motion.h4}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            sx={{
              mb: 4,
              color: 'text.secondary',
              fontWeight: 300,
            }}
          >
            Cultivate Your Interview Process
          </Typography>

          <Box
            component={motion.div}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.8 }}
          >
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/login')}
              sx={{
                mr: 2,
                borderRadius: '50px',
                px: 4,
                py: 2,
                fontSize: '1.1rem',
                textTransform: 'none',
                background: 'linear-gradient(45deg, #4CAF50 30%, #81C784 90%)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #388E3C 30%, #66BB6A 90%)',
                },
              }}
            >
              Start Your Journey
            </Button>
            <Button
              variant="outlined"
              size="large"
              onClick={() => navigate('/register')}
              sx={{
                borderRadius: '50px',
                px: 4,
                py: 2,
                fontSize: '1.1rem',
                textTransform: 'none',
                borderColor: '#4CAF50',
                color: '#4CAF50',
                '&:hover': {
                  borderColor: '#388E3C',
                  color: '#388E3C',
                },
              }}
            >
              Join the Community
            </Button>
          </Box>
        </Box>
      </Container>
    </Box>
  );
} 