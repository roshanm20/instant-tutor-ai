import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Chip,
  Paper,
} from '@mui/material';
import {
  School,
  Psychology,
  Speed,
  Language,
  TrendingUp,
  Support,
} from '@mui/icons-material';

const HomePage: React.FC = () => {
  const features = [
    {
      icon: <Speed />,
      title: 'Instant Responses',
      description: 'Get answers in under 2 seconds',
      color: '#4caf50',
    },
    {
      icon: <Psychology />,
      title: 'AI-Powered',
      description: 'Advanced AI tutoring system',
      color: '#2196f3',
    },
    {
      icon: <Language />,
      title: 'Multi-Language',
      description: 'English, Malayalam, Hindi support',
      color: '#ff9800',
    },
    {
      icon: <School />,
      title: 'Kerala Focus',
      description: 'SCERT, CBSE, ICSE curriculum',
      color: '#9c27b0',
    },
  ];

  const stats = [
    { label: 'Response Time', value: '< 2s', color: '#4caf50' },
    { label: 'Accuracy', value: '85%+', color: '#2196f3' },
    { label: 'Languages', value: '3', color: '#ff9800' },
    { label: 'Uptime', value: '95%+', color: '#9c27b0' },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Paper
        elevation={3}
        sx={{
          p: 4,
          mb: 4,
          background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
          color: 'white',
          textAlign: 'center',
        }}
      >
        <Typography variant="h2" component="h1" gutterBottom>
          🚀 Instant Tutor AI
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          AI-Powered Tutoring for Kerala Education
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, mb: 3 }}>
          Replace traditional Q&A forums with instant, intelligent responses
          using advanced AI and vector database technology.
        </Typography>
        <Button
          variant="contained"
          size="large"
          sx={{
            backgroundColor: 'white',
            color: 'primary.main',
            '&:hover': {
              backgroundColor: 'grey.100',
            },
          }}
        >
          Start Learning Now
        </Button>
      </Paper>

      {/* Features Grid */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                },
              }}
            >
              <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                <Box
                  sx={{
                    color: feature.color,
                    fontSize: '3rem',
                    mb: 2,
                  }}
                >
                  {feature.icon}
                </Box>
                <Typography variant="h6" component="h3" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Stats Section */}
      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" component="h2" gutterBottom textAlign="center">
          📊 Performance Metrics
        </Typography>
        <Grid container spacing={2}>
          {stats.map((stat, index) => (
            <Grid item xs={6} sm={3} key={index}>
              <Box textAlign="center">
                <Typography
                  variant="h4"
                  component="div"
                  sx={{ color: stat.color, fontWeight: 'bold' }}
                >
                  {stat.value}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {stat.label}
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Paper>

      {/* Kerala Features */}
      <Paper elevation={2} sx={{ p: 3 }}>
        <Typography variant="h5" component="h2" gutterBottom textAlign="center">
          🇮🇳 Kerala Market Features
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Box>
              <Typography variant="h6" gutterBottom>
                📚 Curriculum Support
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                <Chip label="SCERT" color="primary" />
                <Chip label="CBSE" color="secondary" />
                <Chip label="ICSE" color="default" />
              </Box>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Box>
              <Typography variant="h6" gutterBottom>
                🗣️ Language Support
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                <Chip label="English" color="primary" />
                <Chip label="Malayalam" color="secondary" />
                <Chip label="Hindi" color="default" />
              </Box>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default HomePage;
