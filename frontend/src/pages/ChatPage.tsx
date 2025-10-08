import React, { useState } from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  List,
  ListItem,
  ListItemText,
  Avatar,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Send,
  Psychology,
  Person,
  School,
} from '@mui/icons-material';
import { chatService } from '../services/chatService';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  sources?: Array<{
    id: number;
    content_preview: string;
    video_path: string;
    relevance_score: number;
  }>;
  confidence?: number;
  suggested_followups?: string[];
}

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [courseId, setCourseId] = useState('MATH_101');

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatService.askQuestion({
        query: inputText,
        course_id: courseId,
        user_id: 'student_123',
      });

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.answer,
        sender: 'ai',
        timestamp: new Date(),
        sources: response.sources,
        confidence: response.confidence,
        suggested_followups: response.suggested_followups,
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setError('Failed to get response. Please try again.');
      console.error('Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const handleFollowup = (followup: string) => {
    setInputText(followup);
  };

  return (
    <Box sx={{ height: 'calc(100vh - 200px)', display: 'flex', flexDirection: 'column' }}>
      {/* Course Selector */}
      <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6" gutterBottom>
          📚 Active Course
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          {['MATH_101', 'PHYSICS_101', 'CHEMISTRY_101'].map((course) => (
            <Chip
              key={course}
              label={course}
              color={courseId === course ? 'primary' : 'default'}
              onClick={() => setCourseId(course)}
              icon={<School />}
            />
          ))}
        </Box>
      </Paper>

      {/* Messages */}
      <Paper
        elevation={2}
        sx={{
          flexGrow: 1,
          overflow: 'auto',
          p: 2,
          mb: 2,
          maxHeight: '60vh',
        }}
      >
        {messages.length === 0 ? (
          <Box textAlign="center" sx={{ mt: 4 }}>
            <Psychology sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" color="text.secondary">
              Ask me anything about your course!
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              I can help with math, physics, chemistry, and more.
            </Typography>
          </Box>
        ) : (
          <List>
            {messages.map((message) => (
              <ListItem
                key={message.id}
                sx={{
                  flexDirection: message.sender === 'user' ? 'row-reverse' : 'row',
                  mb: 2,
                }}
              >
                <Avatar
                  sx={{
                    bgcolor: message.sender === 'user' ? 'primary.main' : 'secondary.main',
                    mx: 1,
                  }}
                >
                  {message.sender === 'user' ? <Person /> : <Psychology />}
                </Avatar>
                <Box sx={{ maxWidth: '70%' }}>
                  <Paper
                    elevation={1}
                    sx={{
                      p: 2,
                      bgcolor: message.sender === 'user' ? 'primary.light' : 'grey.100',
                      color: message.sender === 'user' ? 'white' : 'text.primary',
                    }}
                  >
                    <Typography variant="body1">{message.text}</Typography>
                    {message.confidence && (
                      <Chip
                        label={`Confidence: ${(message.confidence * 100).toFixed(1)}%`}
                        size="small"
                        sx={{ mt: 1 }}
                      />
                    )}
                  </Paper>
                  
                  {/* Sources */}
                  {message.sources && message.sources.length > 0 && (
                    <Box sx={{ mt: 1 }}>
                      <Typography variant="caption" color="text.secondary">
                        Sources:
                      </Typography>
                      {message.sources.map((source, index) => (
                        <Chip
                          key={index}
                          label={`${source.video_path} (${(source.relevance_score * 100).toFixed(1)}%)`}
                          size="small"
                          sx={{ mr: 1, mt: 0.5 }}
                        />
                      ))}
                    </Box>
                  )}

                  {/* Follow-up suggestions */}
                  {message.suggested_followups && message.suggested_followups.length > 0 && (
                    <Box sx={{ mt: 1 }}>
                      <Typography variant="caption" color="text.secondary">
                        Suggested follow-ups:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                        {message.suggested_followups.map((followup, index) => (
                          <Chip
                            key={index}
                            label={followup}
                            size="small"
                            variant="outlined"
                            onClick={() => handleFollowup(followup)}
                            sx={{ cursor: 'pointer' }}
                          />
                        ))}
                      </Box>
                    </Box>
                  )}
                </Box>
              </ListItem>
            ))}
            {isLoading && (
              <ListItem>
                <Avatar sx={{ bgcolor: 'secondary.main', mx: 1 }}>
                  <Psychology />
                </Avatar>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <CircularProgress size={20} />
                  <Typography variant="body2" color="text.secondary">
                    AI is thinking...
                  </Typography>
                </Box>
              </ListItem>
            )}
          </List>
        )}
      </Paper>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Input */}
      <Paper elevation={2} sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            multiline
            maxRows={3}
            placeholder="Ask a question about your course..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
          />
          <Button
            variant="contained"
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isLoading}
            sx={{ minWidth: 'auto', px: 2 }}
          >
            <Send />
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default ChatPage;
