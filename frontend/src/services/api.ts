import axios, { AxiosError, AxiosInstance } from 'axios';
import {
  Token,
  ApiError,
  User,
  UserCreate,
  Interview,
  InterviewCreate,
  InterviewUpdate,
} from '../types/api';
import { Role } from '../components/RoleSelector';
import { QuestionType } from '../types/chat';

// Create axios instance with default config
const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
api.interceptors.response.use(
  response => response,
  (error: AxiosError<ApiError>) => {
    // Handle token expiration
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const auth = {
  login: async (username: string, password: string): Promise<Token> => {
    const response = await api.post<Token>('/api/token', {
      username,
      password,
    });
    return response.data;
  },

  register: async (userData: UserCreate): Promise<User> => {
    const response = await api.post<User>('/api/users/', userData);
    return response.data;
  },
};

// Interviews API
export const interviews = {
  getAll: async (): Promise<Interview[]> => {
    const response = await api.get('/interviews');
    return response.data;
  },

  getById: async (id: number): Promise<Interview> => {
    const response = await api.get(`/interviews/${id}`);
    return response.data;
  },

  create: async (data: InterviewCreate): Promise<Interview> => {
    const response = await api.post('/interviews', data);
    return response.data;
  },

  update: async (id: number, data: InterviewUpdate): Promise<Interview> => {
    const response = await api.patch(`/interviews/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/interviews/${id}`);
  },
};

// Files API
export const files = {
  upload: async (interviewId: number, file: File): Promise<File> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('interview_id', interviewId.toString());

    const response = await api.post<File>('/api/files/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

// Role API
export const setUserRole = async (userId: number, role: Role) => {
  const response = await api.post(`/users/${userId}/role`, { role });
  return response.data;
};

// Chat API
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  question_type: QuestionType;
  chat_history: ChatMessage[];
}

export interface ChatResponse {
  answer: string;
  context_used: string[];
  confidence_score: number;
  suggested_topics: string[];
}

export const sendChatMessage = async (
  userId: number,
  request: ChatRequest
): Promise<ChatResponse> => {
  const response = await api.post(`/chat/${userId}`, request);
  return response.data;
};

// Feedback API
export interface Feedback {
  rating: number;
  wasHelpful: boolean;
  comment: string;
}

export const submitFeedback = async (
  chatSessionId: number,
  feedback: Feedback
) => {
  const response = await api.post(`/chat/${chatSessionId}/feedback`, feedback);
  return response.data;
};

// Progress API
export const getUserProgress = async (userId: number) => {
  const response = await api.get(`/users/${userId}/progress`);
  return response.data;
};

export const getRecommendations = async (
  userId: number,
  limit: number = 3
) => {
  const response = await api.get(`/users/${userId}/recommendations`, {
    params: { limit }
  });
  return response.data;
};

export const getStudyStreak = async (userId: number) => {
  const response = await api.get(`/users/${userId}/streak`);
  return response.data;
};

export default api;
