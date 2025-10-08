import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  LinearProgress,
  Alert,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Upload,
  Analytics,
  School,
  VideoLibrary,
  TrendingUp,
  People,
} from '@mui/icons-material';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`admin-tabpanel-${index}`}
      aria-labelledby={`admin-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const AdminPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [uploadData, setUploadData] = useState({
    courseId: '',
    courseTitle: '',
    instructorName: '',
    language: 'english',
    difficulty: 'intermediate',
  });
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleUpload = async () => {
    setIsUploading(true);
    setUploadProgress(0);

    // Simulate upload progress
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsUploading(false);
          return 100;
        }
        return prev + 10;
      });
    }, 200);

    // Simulate API call
    setTimeout(() => {
      clearInterval(interval);
      setIsUploading(false);
      setUploadProgress(0);
      alert('Course uploaded successfully!');
    }, 2000);
  };

  const analyticsData = {
    totalQueries: 1247,
    avgResponseTime: 1.2,
    userSatisfaction: 4.3,
    totalUsers: 156,
    coursesActive: 12,
    knowledgeBaseSize: 2456,
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        🛠️ Admin Dashboard
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Course Upload" icon={<Upload />} />
          <Tab label="Analytics" icon={<Analytics />} />
          <Tab label="System Status" icon={<TrendingUp />} />
        </Tabs>
      </Box>

      {/* Course Upload Tab */}
      <TabPanel value={tabValue} index={0}>
        <Paper elevation={2} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            📚 Upload New Course
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Course ID"
                value={uploadData.courseId}
                onChange={(e) => setUploadData({ ...uploadData, courseId: e.target.value })}
                placeholder="e.g., MATH_101"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Course Title"
                value={uploadData.courseTitle}
                onChange={(e) => setUploadData({ ...uploadData, courseTitle: e.target.value })}
                placeholder="e.g., Calculus Fundamentals"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Instructor Name"
                value={uploadData.instructorName}
                onChange={(e) => setUploadData({ ...uploadData, instructorName: e.target.value })}
                placeholder="e.g., Dr. Smith"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                select
                label="Language"
                value={uploadData.language}
                onChange={(e) => setUploadData({ ...uploadData, language: e.target.value })}
                SelectProps={{ native: true }}
              >
                <option value="english">English</option>
                <option value="malayalam">Malayalam</option>
                <option value="hindi">Hindi</option>
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <Button
                variant="contained"
                startIcon={<Upload />}
                onClick={handleUpload}
                disabled={isUploading || !uploadData.courseId || !uploadData.courseTitle}
                fullWidth
                size="large"
              >
                {isUploading ? 'Uploading...' : 'Upload Course'}
              </Button>
              {isUploading && (
                <Box sx={{ mt: 2 }}>
                  <LinearProgress variant="determinate" value={uploadProgress} />
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Processing course videos... {uploadProgress}%
                  </Typography>
                </Box>
              )}
            </Grid>
          </Grid>
        </Paper>
      </TabPanel>

      {/* Analytics Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <School sx={{ fontSize: 40, color: 'primary.main', mr: 1 }} />
                  <Typography variant="h4" component="div">
                    {analyticsData.totalQueries}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Total Queries
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <TrendingUp sx={{ fontSize: 40, color: 'success.main', mr: 1 }} />
                  <Typography variant="h4" component="div">
                    {analyticsData.avgResponseTime}s
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Avg Response Time
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <People sx={{ fontSize: 40, color: 'secondary.main', mr: 1 }} />
                  <Typography variant="h4" component="div">
                    {analyticsData.totalUsers}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Active Users
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <VideoLibrary sx={{ fontSize: 40, color: 'warning.main', mr: 1 }} />
                  <Typography variant="h4" component="div">
                    {analyticsData.coursesActive}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Active Courses
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Paper elevation={2} sx={{ p: 3, mt: 3 }}>
          <Typography variant="h6" gutterBottom>
            📊 Performance Metrics
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
              <Box textAlign="center">
                <Typography variant="h3" color="success.main">
                  {analyticsData.userSatisfaction}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  User Satisfaction (5.0)
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Box textAlign="center">
                <Typography variant="h3" color="primary.main">
                  {analyticsData.knowledgeBaseSize}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Knowledge Base Chunks
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Box textAlign="center">
                <Typography variant="h3" color="secondary.main">
                  95%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  System Uptime
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Paper>
      </TabPanel>

      {/* System Status Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                🔧 System Health
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">API Server</Typography>
                  <Chip label="Healthy" color="success" size="small" />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Vector Database</Typography>
                  <Chip label="Connected" color="success" size="small" />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">AI Services</Typography>
                  <Chip label="Active" color="success" size="small" />
                </Box>
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                📈 Recent Activity
              </Typography>
              <Box>
                <Typography variant="body2" color="text.secondary">
                  • 15 queries in the last hour
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • 3 new course uploads today
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • 2 new user registrations
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • System running smoothly
                </Typography>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </TabPanel>
    </Box>
  );
};

export default AdminPage;
