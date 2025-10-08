import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  BottomNavigation,
  BottomNavigationAction,
  Paper,
} from '@mui/material';
import {
  Home,
  Chat,
  AdminPanelSettings,
} from '@mui/icons-material';

const Navigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const getCurrentTab = () => {
    switch (location.pathname) {
      case '/':
        return 0;
      case '/chat':
        return 1;
      case '/admin':
        return 2;
      default:
        return 0;
    }
  };

  return (
    <Paper
      sx={{ position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 1000 }}
      elevation={3}
    >
      <BottomNavigation
        value={getCurrentTab()}
        onChange={(event, newValue) => {
          switch (newValue) {
            case 0:
              navigate('/');
              break;
            case 1:
              navigate('/chat');
              break;
            case 2:
              navigate('/admin');
              break;
          }
        }}
        showLabels
      >
        <BottomNavigationAction
          label="Home"
          icon={<Home />}
        />
        <BottomNavigationAction
          label="Chat"
          icon={<Chat />}
        />
        <BottomNavigationAction
          label="Admin"
          icon={<AdminPanelSettings />}
        />
      </BottomNavigation>
    </Paper>
  );
};

export default Navigation;
