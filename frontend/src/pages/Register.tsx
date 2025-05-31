import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  TextField,
  Typography,
  Alert,
  IconButton,
  InputAdornment,
  Tooltip,
} from '@mui/material';
import { Visibility, VisibilityOff, Refresh as RefreshIcon } from '@mui/icons-material';
import { Link } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';

export default function Register() {
  const { register, error, loading } = useAuth();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await register(name, email, password);
    } catch (err) {
      // Error is handled by useAuth hook
    }
  };

  const generatePassword = () => {
    const length = 16;
    const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+';
    let newPassword = '';
    
    // Ensure at least one of each required character type
    newPassword += charset.match(/[a-z]/)[0]; // lowercase
    newPassword += charset.match(/[A-Z]/)[0]; // uppercase
    newPassword += charset.match(/[0-9]/)[0]; // number
    newPassword += charset.match(/[!@#$%^&*()_+]/)[0]; // special char
    
    // Fill the rest randomly
    for (let i = newPassword.length; i < length; i++) {
      newPassword += charset.charAt(Math.floor(Math.random() * charset.length));
    }

    // Shuffle the password
    newPassword = newPassword.split('').sort(() => Math.random() - 0.5).join('');
    setPassword(newPassword);
    setShowPassword(true); // Show the generated password
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        bgcolor: 'background.default',
      }}
    >
      <Container maxWidth="sm">
        <Card
          elevation={0}
          sx={{
            borderRadius: 2,
            boxShadow: theme =>
              theme.palette.mode === 'light'
                ? '0 0 40px rgba(0,0,0,0.1)'
                : '0 0 40px rgba(255,255,255,0.05)',
          }}
        >
          <CardContent sx={{ p: 4 }}>
            <Box sx={{ mb: 4, textAlign: 'center' }}>
              <Typography variant="h4" component="h1" gutterBottom>
                Create an account
              </Typography>
              <Typography color="text.secondary">Join Ivy to get started</Typography>
            </Box>

            {error && (
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
            )}

            <form onSubmit={handleSubmit}>
              <TextField
                fullWidth
                label="Full Name"
                value={name}
                onChange={e => setName(e.target.value)}
                margin="normal"
                required
                autoFocus
              />

              <TextField
                fullWidth
                label="Email address"
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                margin="normal"
                required
              />

              <TextField
                fullWidth
                label="Password"
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={e => setPassword(e.target.value)}
                margin="normal"
                required
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <Tooltip title="Generate Strong Password">
                        <IconButton onClick={generatePassword} edge="end" sx={{ mr: 1 }}>
                          <RefreshIcon />
                        </IconButton>
                      </Tooltip>
                      <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />

              <Button
                fullWidth
                size="large"
                type="submit"
                variant="contained"
                disabled={loading}
                sx={{ mt: 3 }}
              >
                {loading ? 'Creating account...' : 'Create account'}
              </Button>
            </form>

            <Box sx={{ mt: 3, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">
                Already have an account?{' '}
                <Link to="/login" style={{ color: 'inherit', fontWeight: 500 }}>
                  Sign in
                </Link>
              </Typography>
            </Box>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}
