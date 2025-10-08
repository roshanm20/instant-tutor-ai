import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer demo-token-123',
  },
});

export interface QueryRequest {
  query: string;
  course_id: string;
  user_id: string;
}

export interface QueryResponse {
  answer: string;
  sources: Array<{
    id: number;
    content_preview: string;
    video_path: string;
    timestamp: {
      start: number;
      end: number;
    };
    relevance_score: number;
    topic: string;
  }>;
  confidence: number;
  response_time: number;
  suggested_followups: string[];
}

export interface CourseUploadRequest {
  course_id: string;
  course_title: string;
  video_urls: string[];
  instructor_name?: string;
  language: string;
  difficulty: string;
}

export interface AnalyticsResponse {
  course_id: string;
  total_queries: number;
  avg_response_time_ms: number;
  avg_user_rating: number;
  knowledge_base: {
    total_content_chunks: number;
    last_updated: string;
  };
}

export const chatService = {
  async askQuestion(request: QueryRequest): Promise<QueryResponse> {
    try {
      const response = await api.post('/api/query', request);
      return response.data;
    } catch (error) {
      console.error('Error asking question:', error);
      throw new Error('Failed to get response from AI tutor');
    }
  },

  async uploadCourse(request: CourseUploadRequest) {
    try {
      const response = await api.post('/api/courses/upload', request);
      return response.data;
    } catch (error) {
      console.error('Error uploading course:', error);
      throw new Error('Failed to upload course');
    }
  },

  async getAnalytics(courseId: string): Promise<AnalyticsResponse> {
    try {
      const response = await api.get(`/api/analytics/course/${courseId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting analytics:', error);
      throw new Error('Failed to get analytics');
    }
  },

  async submitFeedback(queryId: number, rating: number, comment?: string) {
    try {
      const response = await api.post('/api/feedback', {
        query_id: queryId,
        rating,
        comment,
      });
      return response.data;
    } catch (error) {
      console.error('Error submitting feedback:', error);
      throw new Error('Failed to submit feedback');
    }
  },

  async getKeralaFeatures() {
    try {
      const response = await api.get('/api/kerala/features');
      return response.data;
    } catch (error) {
      console.error('Error getting Kerala features:', error);
      throw new Error('Failed to get Kerala features');
    }
  },

  async healthCheck() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw new Error('Failed to check system health');
    }
  },
};

export default chatService;
