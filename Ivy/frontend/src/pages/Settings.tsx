import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Divider,
  Grid,
  Switch,
  TextField,
  Typography,
  FormControlLabel,
  Alert,
} from '@mui/material';
import { useAuth } from '@/hooks/useAuth';

export default function Settings() {
  const { user } = useAuth();
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const [preferences, setPreferences] = useState({
    emailNotifications: true,
    desktopNotifications: true,
    autoSchedule: false,
    darkMode: false,
  });

  const handleProfileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // TODO: Implement profile update
      setShowSuccessMessage(true);
      setTimeout(() => setShowSuccessMessage(false), 3000);
    } catch (error) {
      console.error('Failed to update profile:', error);
    }
  };

  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // TODO: Implement password update
      setShowSuccessMessage(true);
      setTimeout(() => setShowSuccessMessage(false), 3000);
    } catch (error) {
      console.error('Failed to update password:', error);
    }
  };

  const handlePreferenceChange =
    (key: keyof typeof preferences) => (event: React.ChangeEvent<HTMLInputElement>) => {
      setPreferences(prev => ({
        ...prev,
        [key]: event.target.checked,
      }));
    };

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 4 }}>
        Settings
      </Typography>

      {showSuccessMessage && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Settings updated successfully
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Profile Settings
              </Typography>
              <form onSubmit={handleProfileSubmit}>
                <TextField
                  fullWidth
                  label="Name"
                  value={formData.name}
                  onChange={e => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="Email"
                  type="email"
                  value={formData.email}
                  onChange={e => setFormData(prev => ({ ...prev, email: e.target.value }))}
                  margin="normal"
                />
                <Button type="submit" variant="contained" sx={{ mt: 2 }}>
                  Update Profile
                </Button>
              </form>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Change Password
              </Typography>
              <form onSubmit={handlePasswordSubmit}>
                <TextField
                  fullWidth
                  label="Current Password"
                  type="password"
                  value={formData.currentPassword}
                  onChange={e =>
                    setFormData(prev => ({ ...prev, currentPassword: e.target.value }))
                  }
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="New Password"
                  type="password"
                  value={formData.newPassword}
                  onChange={e =>
                    setFormData(prev => ({ ...prev, newPassword: e.target.value }))
                  }
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="Confirm New Password"
                  type="password"
                  value={formData.confirmPassword}
                  onChange={e =>
                    setFormData(prev => ({ ...prev, confirmPassword: e.target.value }))
                  }
                  margin="normal"
                />
                <Button type="submit" variant="contained" sx={{ mt: 2 }}>
                  Change Password
                </Button>
              </form>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Preferences
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={preferences.emailNotifications}
                      onChange={handlePreferenceChange('emailNotifications')}
                    />
                  }
                  label="Email Notifications"
                />
                <Divider />
                <FormControlLabel
                  control={
                    <Switch
                      checked={preferences.desktopNotifications}
                      onChange={handlePreferenceChange('desktopNotifications')}
                    />
                  }
                  label="Desktop Notifications"
                />
                <Divider />
                <FormControlLabel
                  control={
                    <Switch
                      checked={preferences.autoSchedule}
                      onChange={handlePreferenceChange('autoSchedule')}
                    />
                  }
                  label="Auto-schedule Interviews"
                />
                <Divider />
                <FormControlLabel
                  control={
                    <Switch
                      checked={preferences.darkMode}
                      onChange={handlePreferenceChange('darkMode')}
                    />
                  }
                  label="Dark Mode"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
