import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box, AppBar, Toolbar, Typography, Container } from '@mui/material';
import { School, Psychology } from '@mui/icons-material';
import HomePage from './pages/HomePage';
import ChatPage from './pages/ChatPage';
import AdminPage from './pages/AdminPage';
import Navigation from './components/Navigation';

function App() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <AppBar position="static" sx={{ backgroundColor: 'primary.main' }}>
        <Toolbar>
          <School sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Instant Tutor AI
          </Typography>
          <Psychology sx={{ ml: 2 }} />
        </Toolbar>
      </AppBar>

      {/* Navigation */}
      <Navigation />

      {/* Main Content */}
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </Container>
    </Box>
  );
}

export default App;
