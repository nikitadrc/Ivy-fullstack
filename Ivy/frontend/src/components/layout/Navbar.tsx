import React, { useState } from 'react';
import {
  AppBar,
  Avatar,
  Box,
  IconButton,
  Menu,
  MenuItem,
  Toolbar,
  Typography,
  useTheme,
} from '@mui/material';
import {
  Menu as MenuIcon,
  LightMode,
  DarkMode,
  NotificationsOutlined,
  Person,
  Settings,
  Logout,
} from '@mui/icons-material';
import { useAuth } from '@/hooks/useAuth';

interface NavbarProps {
  onSidebarOpen: () => void;
  onThemeToggle: () => void;
  mode: 'light' | 'dark';
}

export default function Navbar({ onSidebarOpen, onThemeToggle, mode }: NavbarProps) {
  const theme = useTheme();
  const { user, logout } = useAuth();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    handleClose();
    logout();
  };

  return (
    <AppBar
      position="sticky"
      sx={{
        bgcolor: 'background.paper',
        color: 'text.primary',
        boxShadow: theme.shadows[1],
      }}
    >
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          edge="start"
          onClick={onSidebarOpen}
          sx={{ mr: 2, display: { sm: 'none' } }}
        >
          <MenuIcon />
        </IconButton>

        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Ivy
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <IconButton color="inherit" onClick={onThemeToggle}>
            {mode === 'dark' ? <LightMode /> : <DarkMode />}
          </IconButton>

          <IconButton color="inherit">
            <NotificationsOutlined />
          </IconButton>

          <IconButton onClick={handleMenu} color="inherit" sx={{ ml: 1 }}>
            <Avatar sx={{ width: 32, height: 32 }} src={user?.avatar} alt={user?.name}>
              {user?.name?.[0] || <Person />}
            </Avatar>
          </IconButton>

          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(anchorEl)}
            onClose={handleClose}
          >
            <MenuItem onClick={handleClose}>
              <Person sx={{ mr: 1 }} /> Profile
            </MenuItem>
            <MenuItem onClick={handleClose}>
              <Settings sx={{ mr: 1 }} /> Settings
            </MenuItem>
            <MenuItem onClick={handleLogout}>
              <Logout sx={{ mr: 1 }} /> Logout
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
